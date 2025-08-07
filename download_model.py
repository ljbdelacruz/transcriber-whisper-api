#!/usr/bin/env python
# Script to pre-download the Llama model

import os
import logging
from huggingface_hub import hf_hub_download

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configuration
LLAMA_MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGUF"
LLAMA_MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"

def download_model():
    """Download the Llama model from Hugging Face."""
    try:
        logger.info(f"Downloading model from Hugging Face: {LLAMA_MODEL_ID}/{LLAMA_MODEL_BASENAME}")
        model_path = hf_hub_download(
            repo_id=LLAMA_MODEL_ID,
            filename=LLAMA_MODEL_BASENAME,
            resume_download=True
        )
        logger.info(f"Model downloaded successfully to: {model_path}")
        logger.info(f"Model file size: {os.path.getsize(model_path) / (1024 * 1024):.2f} MB")
        return model_path
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise

if __name__ == "__main__":
    try:
        model_path = download_model()
        print(f"\nModel downloaded successfully to: {model_path}")
        print(f"You can now start your application, and it will use this pre-downloaded model.")
    except Exception as e:
        print(f"\nFailed to download model: {e}")
