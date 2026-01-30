import re
import json
import base64
from typing import Tuple, Optional
from pathlib import Path

def encode_image_b64(image_path: str) -> Tuple[str, str]:
    """
    Encode an image file to base64 for LLM vision API.
    
    Args:
        image_path: Path to image file
    
    Returns:
        Tuple of (media_type, base64_string)
    """
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
            b64_string = base64.b64encode(image_data).decode("utf-8")
            media_type = "image/png" if image_path.endswith(".png") else "image/jpeg"
            return media_type, b64_string
    except Exception as e:
        raise ValueError(f"Failed to encode image: {e}")

def extract_feedback_and_code(content: str) -> Tuple[str, str]:
    """
    Extract feedback JSON and refined code from LLM response.
    
    Args:
        content: LLM response content
    
    Returns:
        Tuple of (feedback_text, refined_code)
    """
    lines = content.strip().splitlines()
    json_line = lines[0].strip() if lines else ""
    
    feedback = ""
    try:
        obj = json.loads(json_line)
        feedback = str(obj.get("feedback", "")).strip()
    except Exception:
        m_json = re.search(r"\{.*?\}", content, flags=re.DOTALL)
        if m_json:
            try:
                obj = json.loads(m_json.group(0))
                feedback = str(obj.get("feedback", "")).strip()
            except:
                feedback = "Feedback parsing failed"
    
    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content, re.DOTALL | re.IGNORECASE)
    refined_code = m_code.group(1).strip() if m_code else ""
    
    if refined_code and not refined_code.startswith("<execute_python>"):
        refined_code = f"<execute_python>\n{refined_code}\n</execute_python>"
    
    return feedback, refined_code

def reflect_on_chart(
    chart_path: str,
    instruction: str,
    original_code: str,
    model: str = "openai:gpt-4o",
    output_path: str = "chart_v2.png"
) -> Tuple[str, str]:
    """
    Reflect on a chart image and generate improved code.
    
    Args:
        chart_path: Path to the chart image to reflect on
        instruction: Original user instruction
        original_code: Original code that generated the chart
        model: LLM model to use for reflection
        output_path: Path for the improved chart
    
    Returns:
        Tuple of (feedback, refined_code)
    """
    try:
        import aisuite as ai
        client = ai.Client()
    except ImportError:
        return (
            "Reflection requires aisuite (Python 3.10+)",
            f"""<execute_python>
# Reflection not available - requires Python 3.10+ and aisuite
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.text(0.5, 0.5, 'Reflection requires Python 3.10+', ha='center', va='center')
plt.title('Chart Reflection Unavailable')
plt.savefig('{output_path}', dpi=300, bbox_inches='tight')
plt.close()
</execute_python>"""
        )
    
    try:
        media_type, b64_image = encode_image_b64(chart_path)
    except Exception as e:
        return (
            f"Failed to encode image: {e}",
            original_code
        )
    
    prompt = f"""You are a data visualization expert.
Your task: critique the attached chart and the original code against the given instruction,
then return improved matplotlib code.

Original code (for context):
{original_code}

OUTPUT FORMAT (STRICT):
1) First line: a valid JSON object with ONLY the "feedback" field.
Example: {{"feedback": "The legend is unclear and the axis labels overlap."}}

2) After a newline, output ONLY the refined Python code wrapped in:
<execute_python>
...
</execute_python>

3) Import all necessary libraries in the code. Don't assume any imports from the original code.

HARD CONSTRAINTS:
- Do NOT include Markdown, backticks, or any extra prose outside the two parts above.
- Use pandas/matplotlib only (no seaborn).
- Save to '{output_path}' with dpi=300.
- Always call plt.close() at the end (no plt.show()).
- Include all necessary import statements.

Instruction:
{instruction}
"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a data visualization expert who critiques charts and improves them."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{b64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.3,
        )
        
        content = response.choices[0].message.content or ""
        feedback, refined_code = extract_feedback_and_code(content)
        
        return feedback, refined_code
    except Exception as e:
        return (
            f"Reflection failed: {e}",
            original_code
        )

