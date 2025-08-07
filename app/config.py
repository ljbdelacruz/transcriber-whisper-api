# app/config.py
# Configuration settings for the application

import os

# Whisper Configuration
UPLOAD_DIR = "uploaded_audio"
MODEL_SIZE = "base"  # Or "small", "medium", "large-v3", etc.

# Llama Configuration
LLAMA_MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGUF"  # More accessible model
LLAMA_MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"  # GGUF quantized version
LLAMA_CONTEXT_WINDOW = 4096  # Context window size
LLAMA_MAX_TOKENS = 1024  # Max tokens to generate
LLAMA_ENABLE = True  # Set to False to disable Llama functionality

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
