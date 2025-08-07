#!/usr/bin/env python
# Test script for Llama model

import os
import logging
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configuration
LLAMA_MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGUF"
LLAMA_MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"
LLAMA_CONTEXT_WINDOW = 4096
LLAMA_MAX_TOKENS = 1024

def test_llama():
    """Test the Llama model with a simple prompt."""
    try:
        # Get model path from cache
        from huggingface_hub import try_to_load_from_cache
        model_path = try_to_load_from_cache(
            repo_id=LLAMA_MODEL_ID,
            filename=LLAMA_MODEL_BASENAME
        )
        logger.info(f"Found model in cache: {model_path}")
        
        # Initialize the model
        logger.info("Initializing Llama model...")
        llama = Llama(
            model_path=model_path,
            n_ctx=LLAMA_CONTEXT_WINDOW,
            verbose=True
        )
        logger.info("Llama model loaded successfully")
        
        # Test with a simple prompt
        prompt = "USER: Hello, can you tell me more about yourself?\nASSISTANT:"
        logger.info(f"Using prompt: {prompt}")
        
        # Generate response
        response = llama.create_completion(
            prompt=prompt,
            max_tokens=LLAMA_MAX_TOKENS,
            temperature=0.7,
            stop=["USER:"]
        )
        
        logger.info(f"Response: {response}")
        if response and "choices" in response and len(response["choices"]) > 0:
            text = response["choices"][0]["text"]
            logger.info(f"Generated text: {text}")
            return text
        else:
            logger.error("No response generated")
            return None
    except Exception as e:
        logger.error(f"Error testing Llama model: {e}")
        raise

if __name__ == "__main__":
    try:
        response = test_llama()
        if response:
            print("\nLlama model test successful!")
            print(f"Response: {response}")
        else:
            print("\nLlama model test failed!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
