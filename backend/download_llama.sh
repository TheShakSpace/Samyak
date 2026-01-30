#!/bin/bash
# Script to download Llama 3.3 70B model

echo "======================================"
echo "Llama 3.3 70B Model Download"
echo "======================================"
echo ""

# Your custom URL (valid for 48 hours)
CUSTOM_URL="https://llama3-3.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoibHR6d2FoZTBxdGcyajBsbzQyODIyeWk5IiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTMubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2ODQyMDM5N319fV19&Signature=KqR08r5R%7EQFuJth6zlQWmyrvDj-4xq6CnzbZ3Avbl7Aq7Nkyyz4UbRFR3nHwCWd7Sf5mNWu7pdTb%7ES9Viz-lqhvybcm8LCNTTpmLlwjnjBRVdr9vfkxykLzJpx9-cUK4%7EH7EWJbCSZBh4b69NkuC4mmQVP16wruRmNrCfjZAEZZe0TFMFRJA10oEMVKbwZyfvgbN2xdBINRE9WTiDPPOYNolPVURYiwpepM64BF54XXCnek13KJNnLrmmryIBWbu%7E68qS1x-w7rToB8xE026vvfLJfU2cwwV6m6Ulj6XXZ1cDv-Nq4QKlwwRaXLOF3XXx0muOaYWxBJTGrmffAKslA__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=1225593299004920"

echo "Step 1: Checking llama-stack installation..."
python3 -c "import llama_stack" 2>/dev/null && echo "✓ llama-stack installed" || echo "✗ llama-stack not found. Install with: pip3 install llama-stack"

echo ""
echo "Step 2: Downloading Llama 3.3 70B Instruct model..."
echo "Note: This will download ~40GB. Ensure you have enough disk space!"
echo ""

# Try to use llama CLI if available
if command -v llama &> /dev/null; then
    echo "Using llama CLI..."
    llama model download \
      --source meta \
      --model-id Llama-3.3-70B-Instruct \
      --custom-url "$CUSTOM_URL"
elif python3 -m llama &> /dev/null; then
    echo "Using python -m llama..."
    python3 -m llama model download \
      --source meta \
      --model-id Llama-3.3-70B-Instruct \
      --custom-url "$CUSTOM_URL"
else
    echo "⚠ Llama CLI not found in PATH."
    echo ""
    echo "Manual download options:"
    echo "1. Visit: https://github.com/meta-llama/llama"
    echo "2. Follow the download instructions"
    echo "3. Download to: ~/.llama/models/ or ./models/"
    echo ""
    echo "Or install llama-cpp-python for easier integration:"
    echo "  pip3 install llama-cpp-python"
    echo ""
    echo "Then download quantized models from Hugging Face:"
    echo "  https://huggingface.co/models?search=llama-3.3-70b"
fi

echo ""
echo "======================================"
echo "Next Steps:"
echo "======================================"
echo "1. After download, update .env:"
echo "   LLM_PROVIDER=llama"
echo "   LLAMA_MODEL_PATH=/path/to/model"
echo ""
echo "2. Test with:"
echo "   python3 cli.py agent 'test'"
echo ""
echo "See LLAMA_SETUP.md for detailed instructions"

