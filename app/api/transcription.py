# app/api/transcription.py
# API endpoints for transcription functionality

import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import aiofiles
from ..models.transcription import TranscriptionStatus
from ..services.transcription import transcribe_audio_task, get_transcription_result, set_transcription_result
from ..config import UPLOAD_DIR

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/transcribe",
    tags=["transcription"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=TranscriptionStatus)
async def upload_and_transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Uploads an audio file and initiates transcription.
    Returns a unique ID to poll for the transcription result.
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only audio files are allowed."
        )

    file_extension = os.path.splitext(file.filename)[1]
    # Generate a unique filename to avoid collisions
    unique_id = str(uuid.uuid4())
    temp_audio_path = os.path.join(UPLOAD_DIR, f"{unique_id}{file_extension}")

    try:
        # Save the uploaded file asynchronously
        async with aiofiles.open(temp_audio_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024): # Read in 1MB chunks
                await out_file.write(content)
        logger.info(f"Received and saved file: {temp_audio_path}")

        # Initialize status for polling
        set_transcription_result(unique_id, {"status": "processing"})

        # Define a callback function to update the global results dict
        def update_result_callback(result_data):
            set_transcription_result(unique_id, result_data)

        # Add the transcription task to background
        background_tasks.add_task(transcribe_audio_task, temp_audio_path, update_result_callback)

        return {"id": unique_id, "status": "processing"}

    except Exception as e:
        logger.error(f"Error handling file upload or initiating transcription: {e}")
        # Clean up if an error occurs before the background task starts
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

@router.get("/status/{task_id}", response_model=TranscriptionStatus)
async def get_transcription_status(task_id: str):
    """
    Checks the status of a transcription task by its ID.
    Returns the transcription text if completed.
    """
    result = get_transcription_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Transcription task not found.")
    return TranscriptionStatus(id=task_id, **result)
