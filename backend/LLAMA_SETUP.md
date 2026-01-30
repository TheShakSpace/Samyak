# Llama Setup Guide - Using Llama Instead of OpenAI

## Overview

This guide shows how to set up and use Meta's Llama 3.3 70B model instead of OpenAI for the Task Management Agent.

---

## Step 1: Install Llama Stack

```bash
pip install llama-stack -U
```

✅ Already installed!

---

## Step 2: Download Llama Model

### Option A: Using Llama CLI (Recommended)

```bash
# List available models
llama model list

# Download Llama 3.3 70B Instruct
llama model download \
  --source meta \
  --model-id Llama-3.3-70B-Instruct \
  --custom-url "YOUR_CUSTOM_URL_HERE"
```

**Your Custom URL** (valid for 48 hours):
```
https://llama3-3.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoibHR6d2FoZTBxdGcyajBsbzQyODIyeWk5IiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTMubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2ODQyMDM5N319fV19&Signature=KqR08r5R%7EQFuJth6zlQWmyrvDj-4xq6CnzbZ3Avbl7Aq7Nkyyz4UbRFR3nHwCWd7Sf5mNWu7pdTb%7ES9Viz-lqhvybcm8LCNTTpmLlwjnjBRVdr9vfkxykLzJpx9-cUK4%7EH7EWJbCSZBh4b69NkuC4mmQVP16wruRmNrCfjZAEZZe0TFMFRJA10oEMVKbwZyfvgbN2xdBINRE9WTiDPPOYNolPVURYiwpepM64BF54XXCnek13KJNnLrmmryIBWbu%7E68qS1x-w7rToB8xE026vvfLJfU2cwwV6m6Ulj6XXZ1cDv-Nq4QKlwwRaXLOF3XXx0muOaYWxBJTGrmffAKslA__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=1225593299004920
```

### Option B: Manual Download

1. Visit: https://github.com/meta-llama/llama
2. Follow official download instructions
3. Download model files to `~/.llama/models/` or `./models/`

**Note**: Llama 3.3 70B is ~40GB, ensure you have enough disk space!

---

## Step 3: Install llama-cpp-python (For Better Integration)

```bash
# Standard installation
pip install llama-cpp-python

# Or with GPU support (if you have CUDA)
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

---

## Step 4: Configure Environment

### Update .env File

```env
# Use Llama instead of OpenAI
LLM_PROVIDER=llama
LLM_MODEL=llama-3.3-70b-instruct

# Path to downloaded model (auto-detected if not specified)
LLAMA_MODEL_PATH=/path/to/Llama-3.3-70B-Instruct

# Optional: Llama-specific settings
LLAMA_N_CTX=4096
LLAMA_N_THREADS=4
```

---

## Step 5: Update Configuration

The code will automatically use Llama if configured. The adapter in `utils/llama_adapter.py` provides compatibility with the existing code.

---

## Step 6: Test Llama Integration

```bash
# Test basic functionality
python3 cli.py status

# Test agent with Llama
python3 cli.py agent "Show me all high priority tasks"
```

---

## Using Llama with llama-cpp-python (Better Option)

### Step 1: Convert Model to GGUF Format

If your model is not in GGUF format, you may need to convert it. Check the model download - Llama 3.3 models should come in GGUF format.

### Step 2: Create Enhanced Llama Client

```python
# utils/llama_client.py
from llama_cpp import Llama
from config import LLAMA_MODEL_PATH

llm = Llama(
    model_path=LLAMA_MODEL_PATH,
    n_ctx=4096,
    n_threads=4,
    verbose=False
)

# Use it
response = llm(
    "Show me all high priority tasks",
    max_tokens=512,
    temperature=0.7
)
```

---

## Differences: Llama vs OpenAI

### Advantages of Llama

✅ **Free to Use** - No API costs
✅ **Privacy** - Runs locally, data stays on your machine
✅ **No Rate Limits** - Use as much as you want
✅ **Fully Open Source** - Customizable

### Considerations

⚠️ **Hardware Requirements** - 70B model needs significant RAM (~40GB+)
⚠️ **Speed** - Slower than API calls (depends on hardware)
⚠️ **Tool Calling** - Needs manual parsing (no native tool calling like OpenAI)
⚠️ **Model Size** - Large download (~40GB)

### Recommendations

- **For Development**: Use smaller models (7B, 13B) for faster iteration
- **For Production**: Consider API services or cloud inference
- **For Privacy**: Llama is perfect for sensitive data

---

## Performance Tips

### Optimize for Speed

```python
# Use smaller context window
n_ctx=2048  # Instead of 4096

# Use more threads
n_threads=8  # Match your CPU cores

# Use GPU if available
n_gpu_layers=35  # Offload layers to GPU
```

### Optimize for Quality

```python
# Larger context window
n_ctx=8192

# More threads
n_threads=8

# Adjust temperature
temperature=0.7  # Lower = more focused
```

---

## Troubleshooting

### Issue: Model Not Found

**Solution**:
```bash
# Check model path
llama model list

# Verify model location
ls -lh ~/.llama/models/
```

### Issue: Out of Memory

**Solution**:
- Use smaller model (7B or 13B)
- Reduce context window (`n_ctx`)
- Use quantized model (Q4, Q5, Q8)

### Issue: Slow Performance

**Solution**:
- Use GPU acceleration
- Increase thread count
- Use quantized model
- Reduce context window

### Issue: Tool Calling Not Working

**Solution**:
- Llama doesn't have native tool calling
- The adapter provides basic compatibility
- Consider using OpenAI for complex tool calling, or implement manual parsing

---

## Quantized Models (Recommended for Local Use)

Quantized models are smaller and faster:

```bash
# Download quantized version
# Q4 = 4-bit quantization (smallest, fastest)
# Q5 = 5-bit quantization (balanced)
# Q8 = 8-bit quantization (best quality)
```

**Example**: Llama-3.3-70B-Instruct-Q4_0.gguf (~20GB instead of ~40GB)

---

## Testing Checklist

- [ ] Llama CLI installed
- [ ] Model downloaded
- [ ] Model path configured
- [ ] llama-cpp-python installed (optional but recommended)
- [ ] .env updated with LLM_PROVIDER=llama
- [ ] Test basic query: `python3 cli.py agent "test"`
- [ ] Verify no OpenAI dependency errors

---

## Next Steps

1. Download the model using your custom URL
2. Update .env configuration
3. Test with simple queries
4. Compare performance with OpenAI
5. Optimize settings for your hardware

---

## Alternative: Use Llama API (If Available)

Some services provide Llama via API:

```env
LLM_PROVIDER=llama-api
LLAMA_API_ENDPOINT=https://api.example.com/v1/chat
LLAMA_API_KEY=your_key
```

Check services like:
- Groq (fast Llama inference)
- Together.ai (Llama API)
- Replicate (Llama hosting)

---

**Ready to proceed with Llama download?** Use the custom URL provided above!

