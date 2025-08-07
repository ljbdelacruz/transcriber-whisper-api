# app/models/conversation.py
# Models for conversation functionality

from pydantic import BaseModel
from typing import Optional, List
from ..config import LLAMA_MAX_TOKENS

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ConversationRequest(BaseModel):
    messages: List[Message]
    max_tokens: Optional[int] = LLAMA_MAX_TOKENS
    temperature: Optional[float] = 0.7

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ConversationResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
