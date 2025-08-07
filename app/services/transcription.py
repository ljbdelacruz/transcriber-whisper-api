# app/services/transcription.py
# Service for audio transcription

import os
import asyncio
import logging
from .model_loader import get_whisper_model

# Setup logging
logger = logging.getLogger(__name__)

# In-memory storage for transcription results (for polling)
transcription_results = {}

async def transcribe_audio_task(audio_path: str, result_callback: callable):
    """
    Asynchronously performs the transcription and calls a callback with the result.
    This is designed to run in a background task, allowing the main API to respond quickly.
    """
    try:
        whisper_model = get_whisper_model()
        if whisper_model is None:
            raise RuntimeError("Whisper model not loaded.")

        logger.info(f"Starting transcription for {audio_path}...")
        # Whisper's transcribe method is synchronous, so run it in a thread pool
        # to not block the FastAPI event loop. asyncio.to_thread is perfect for this.
        result = await asyncio.to_thread(whisper_model.transcribe, audio_path)
        transcription_text = result["text"]
        logger.info(f"Transcription complete for {audio_path}.")
        result_callback({"status": "completed", "transcription": transcription_text})
    except Exception as e:
        logger.error(f"Transcription failed for {audio_path}: {e}")
        result_callback({"status": "failed", "error": str(e)})
    finally:
        # Clean up the temporary audio file after transcription, regardless of success/failure
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Cleaned up temporary file: {audio_path}")

def get_transcription_result(task_id: str):
    """
    Get the transcription result for a task
    """
    return transcription_results.get(task_id)

def set_transcription_result(task_id: str, result: dict):
    """
    Set the transcription result for a task
    """
    transcription_results[task_id] = result
