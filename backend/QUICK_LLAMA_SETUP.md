# Quick Llama Setup Guide

## ✅ Step 1: Install Llama Stack (Already Done!)

```bash
pip3 install llama-stack -U
```

✅ Installed!

---

## ⬇️ Step 2: Download Llama Model

### Option A: Use the Download Script

```bash
cd task_management_agent
./download_llama.sh
```

### Option B: Manual Download

```bash
# Try llama CLI
llama model download \
  --source meta \
  --model-id Llama-3.3-70B-Instruct \
  --custom-url "YOUR_CUSTOM_URL_HERE"
```

**Your Custom URL** (valid for 48 hours):
```
https://llama3-3.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoibHR6d2FoZTBxdGcyajBsbzQyODIyeWk5IiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTMubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2ODQyMDM5N319fV19&Signature=KqR08r5R%7EQFuJth6zlQWmyrvDj-4xq6CnzbZ3Avbl7Aq7Nkyyz4UbRFR3nHwCWd7Sf5mNWu7pdTb%7ES9Viz-lqhvybcm8LCNTTpmLlwjnjBRVdr9vfkxykLzJpx9-cUK4%7EH7EWJbCSZBh4b69NkuC4mmQVP16wruRmNrCfjZAEZZe0TFMFRJA10oEMVKbwZyfvgbN2xdBINRE9WTiDPPOYNolPVURYiwpepM64BF54XXCnek13KJNnLrmmryIBWbu%7E68qS1x-w7rToB8xE026vvfLJfU2cwwV6m6Ulj6XXZ1cDv-Nq4QKlwwRaXLOF3XXx0muOaYWxBJTGrmffAKslA__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=1225593299004920
```

**Important**: Model is ~40GB. Ensure you have:
- ✅ 40GB+ free disk space
- ✅ Stable internet connection
- ✅ Time (download may take 30+ minutes)

---

## ⚙️ Step 3: Configure Environment

### Create/Update .env File

```bash
cp .env.example .env
```

Then edit `.env` and set:

```env
# Use Llama instead of OpenAI
LLM_PROVIDER=llama

# Path to your downloaded model
LLAMA_MODEL_PATH=/path/to/Llama-3.3-70B-Instruct
```

**Note**: If you don't set `LLAMA_MODEL_PATH`, the system will try to auto-detect it.

---

## 🧪 Step 4: Test Llama Integration

```bash
# Check system status
python3 cli.py status

# Should show: LLM: ✓ (if model found)

# Test agent with Llama
python3 cli.py agent "Show me all high priority tasks"
```

---

## 🔧 Alternative: Use llama-cpp-python (Recommended)

For better integration and performance:

```bash
# Install
pip3 install llama-cpp-python

# Download quantized model (smaller, faster)
# Visit: https://huggingface.co/models?search=llama-3.3-70b-gguf
# Download Q4 or Q5 quantized version (~20GB instead of 40GB)
```

Then update `.env`:
```env
LLM_PROVIDER=llama
LLAMA_MODEL_PATH=./models/llama-3.3-70b-instruct-q4_0.gguf
```

---

## 📝 Quick Reference

### Switch Between OpenAI and Llama

**Use OpenAI**:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
```

**Use Llama**:
```env
LLM_PROVIDER=llama
LLAMA_MODEL_PATH=/path/to/model
```

### Check Current Configuration

```bash
python3 cli.py status
```

---

## ❓ Troubleshooting

### Model Not Found

```bash
# Check model path
ls -lh /path/to/model

# Or let it auto-detect
# Remove LLAMA_MODEL_PATH from .env
```

### Out of Memory

Use smaller quantized model:
- Q4_0 (~20GB, fast)
- Q5_0 (~22GB, balanced)
- Q8_0 (~40GB, best quality)

### Slow Performance

1. Use quantized model (Q4 or Q5)
2. Install llama-cpp-python
3. Use GPU if available
4. Reduce context window in config

---

## 🎯 What's Different?

- ✅ **No API key needed** - Runs locally
- ✅ **Free** - No usage costs
- ✅ **Private** - Data stays on your machine
- ⚠️ **Needs hardware** - 40GB+ RAM recommended
- ⚠️ **Slower** - Depends on your hardware

---

**Ready?** Run `./download_llama.sh` to start!

