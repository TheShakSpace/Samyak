#!/bin/bash
# Download Llama 3.3 70B using Ollama (Easiest Method)

echo "======================================"
echo "Downloading Llama Model via Ollama"
echo "======================================"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Installing..."
    echo ""
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    if [ $? -ne 0 ]; then
        echo "⚠ Installation failed. Please install manually:"
        echo "   Visit: https://ollama.com"
        exit 1
    fi
fi

echo "✓ Ollama is installed"
echo ""

# Check disk space
echo "Checking disk space..."
AVAILABLE=$(df -h . | awk 'NR==2 {print $4}' | sed 's/[^0-9.]//g')
echo "Available space: ${AVAILABLE}GB"
echo ""

if (( $(echo "$AVAILABLE < 50" | bc -l 2>/dev/null || echo "0") )); then
    echo "⚠ Warning: Less than 50GB available"
    echo "Model requires ~40GB"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Starting download of Llama 3.3 70B..."
echo "This will download ~40GB and may take 30-60 minutes depending on your connection"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Download model (Ollama will handle it)
echo ""
echo "Downloading llama3.3:70b..."
ollama pull llama3.3:70b

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Download Complete!"
    echo "======================================"
    echo ""
    echo "Model location: ~/.ollama/models"
    echo ""
    echo "Verify download:"
    echo "  ollama list"
    echo ""
    echo "Test the model:"
    echo "  ollama run llama3.3:70b 'Hello, how are you?'"
    echo ""
    echo "Update your .env file:"
    echo "  LLM_PROVIDER=llama"
    echo "  LLAMA_MODEL_PATH=~/.ollama/models"
    echo ""
else
    echo ""
    echo "⚠ Download failed. Please check your internet connection and try again."
    exit 1
fi

