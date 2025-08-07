# app/main.py
# Main application file

import logging
from fastapi import FastAPI
from .api import transcription, conversation, health
from .services.model_loader import load_models

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Whisper and Llama API",
    description="API for transcribing audio files using OpenAI's Whisper model and providing casual conversation using Meta's Llama 2 model.",
    version="1.0.0",
)

# Include routers
app.include_router(transcription.router)
app.include_router(conversation.router)
app.include_router(health.router)

@app.on_event("startup")
async def startup_event():
    """
    Load models on startup
    """
    logger.info("Loading models...")
    models_status = load_models()
    logger.info(f"Models loaded: {models_status}")
