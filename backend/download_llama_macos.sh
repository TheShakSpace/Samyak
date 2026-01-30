#!/bin/bash
# Download Llama 3.3 70B using Ollama on macOS

echo "======================================"
echo "Llama Model Download for macOS"
echo "======================================"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed."
    echo ""
    echo "Installing Ollama for macOS..."
    echo ""
    echo "Option 1: Download from website (Recommended)"
    echo "  Visit: https://ollama.com/download/mac"
    echo "  Download and install the .dmg file"
    echo ""
    echo "Option 2: Install via Homebrew"
    echo "  brew install ollama"
    echo ""
    echo "Option 3: Direct download"
    echo "  curl -L https://ollama.com/download/mac -o ollama-install.pkg"
    echo "  open ollama-install.pkg"
    echo ""
    read -p "Press Enter after installing Ollama, or Ctrl+C to cancel..."
    
    # Verify installation
    if ! command -v ollama &> /dev/null; then
        echo "⚠ Ollama still not found. Please install it first."
        echo "   Visit: https://ollama.com/download/mac"
        exit 1
    fi
fi

echo "✓ Ollama is installed"
echo ""

# Check if Ollama service is running
if ! ollama list &> /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Check disk space
echo "Checking disk space..."
df -h . | head -2
echo ""

echo "Starting download of Llama 3.3 70B..."
echo "This will download ~40GB and may take 30-60 minutes"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Download model
echo ""
echo "Downloading llama3.3:70b..."
echo "This may take a while. Please be patient..."
echo ""

ollama pull llama3.3:70b

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Download Complete!"
    echo "======================================"
    echo ""
    echo "Model downloaded successfully!"
    echo ""
    echo "Verify download:"
    ollama list
    echo ""
    echo "Model location: ~/.ollama/models"
    echo ""
    echo "Test the model:"
    echo "  ollama run llama3.3:70b 'Hello'"
    echo ""
    echo "Your model is ready to use!"
else
    echo ""
    echo "⚠ Download failed. Please check:"
    echo "  1. Internet connection"
    echo "  2. Disk space (need ~40GB free)"
    echo "  3. Ollama service is running"
    exit 1
fi

