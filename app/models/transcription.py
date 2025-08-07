# app/models/transcription.py
# Models for transcription functionality

from pydantic import BaseModel
from typing import Optional

class TranscriptionStatus(BaseModel):
    id: str
    status: str
    transcription: Optional[str] = None
    error: Optional[str] = None
