# app/services/model_loader.py
# Service for loading and managing AI models

import logging
import whisper
from huggingface_hub import hf_hub_download, try_to_load_from_cache
from llama_cpp import Llama
from app.config import MODEL_SIZE, LLAMA_MODEL_ID, LLAMA_MODEL_BASENAME, LLAMA_CONTEXT_WINDOW, LLAMA_ENABLE

# Setup logging
logger = logging.getLogger(__name__)

# Global model instances
whisper_model = None
llama_model = None

def load_models():
    """
    Load both Whisper and Llama models
    """
    global whisper_model, llama_model
    
    # Load Whisper model
    try:
        logger.info(f"Loading Whisper model: {MODEL_SIZE}...")
        whisper_model = whisper.load_model(MODEL_SIZE)
        logger.info(f"Whisper model '{MODEL_SIZE}' loaded successfully.")
    except Exception as e:
        logger.critical(f"Failed to load Whisper model: {e}")
        # Continue even if Whisper model fails to load
    
    # Load Llama model if enabled
    if LLAMA_ENABLE:
        try:
            logger.info(f"Loading Llama model: {LLAMA_MODEL_ID}...")
            
            # First try to get the model from the cache
            try:
                model_path = try_to_load_from_cache(
                    repo_id=LLAMA_MODEL_ID,
                    filename=LLAMA_MODEL_BASENAME
                )
                logger.info(f"Found model in cache: {model_path}")
            except Exception:
                # If not in cache, download it
                logger.info(f"Downloading model from Hugging Face: {LLAMA_MODEL_ID}/{LLAMA_MODEL_BASENAME}")
                model_path = hf_hub_download(
                    repo_id=LLAMA_MODEL_ID,
                    filename=LLAMA_MODEL_BASENAME,
                    resume_download=True
                )
                logger.info(f"Model downloaded to: {model_path}")
            
            # Initialize the model
            logger.info("Initializing Llama model...")
            llama_model = Llama(
                model_path=model_path,
                n_ctx=LLAMA_CONTEXT_WINDOW,
                n_gpu_layers=-1,  # Auto-detect GPU layers (-1) or set to 0 for CPU only
                verbose=True  # Enable verbose logging
            )
            logger.info(f"Llama model loaded successfully.")
        except Exception as e:
            logger.critical(f"Failed to load Llama model: {e}")
            # Continue even if Llama model fails to load
    else:
        logger.info("Llama model loading disabled by configuration.")
        llama_model = None
    
    return {
        "whisper": whisper_model is not None,
        "llama": llama_model is not None
    }

def get_whisper_model():
    """
    Get the loaded Whisper model
    """
    return whisper_model

def get_llama_model():
    """
    Get the loaded Llama model
    """
    return llama_model

def get_models_status():
    """
    Get the status of all loaded models
    """
    llama_status = {
        "enabled": LLAMA_ENABLE,
        "loaded": llama_model is not None,
        "model_id": LLAMA_MODEL_ID if LLAMA_ENABLE else None
    }
    
    return {
        "whisper": {"loaded": whisper_model is not None, "model_size": MODEL_SIZE},
        "llama": llama_status
    }
