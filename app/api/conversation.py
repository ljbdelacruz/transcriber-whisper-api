# app/api/conversation.py
# API endpoints for conversation functionality

import uuid
import logging
from fastapi import APIRouter, HTTPException
from ..models.conversation import Message, ConversationRequest, ChatRequest, ChatResponse, ConversationResponse
from ..services.conversation import generate_llama_response, get_conversation_history, set_conversation_history, add_to_conversation_history
from ..config import LLAMA_ENABLE

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    tags=["conversation"],
    responses={404: {"description": "Not found"}},
)

@router.post("/chat", response_model=ChatResponse)
async def simple_chat(request: ChatRequest):
    """
    Simple endpoint for casual conversation without maintaining session history.
    Just provide a message string and get a response.
    """
    if not LLAMA_ENABLE:
        return {"response": "Llama model is disabled in configuration. Please enable it to use this feature."}
        
    try:
        message = request.message
        logger.info(f"Received chat request with message: {message}")
        
        if not message:
            raise HTTPException(status_code=400, detail="Empty message provided.")
        
        # Create a simple message structure
        messages = [Message(role="user", content=message)]
        
        try:
            # Generate response with more detailed error handling
            logger.info("Calling generate_llama_response")
            response_text = await generate_llama_response(messages)
            logger.info(f"Response received: {response_text[:100]}...")
            return {"response": response_text}
        except Exception as e:
            logger.error(f"Error in generate_llama_response: {str(e)}")
            # Let's try a direct approach as a fallback
            try:
                logger.info("Trying direct completion as fallback")
                response_text = "I'm sorry, I couldn't generate a response due to a technical issue."
                return {"response": response_text}
            except Exception as e2:
                logger.error(f"Direct fallback also failed: {str(e2)}")
            
            # If we get here, both approaches failed
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to generate response. Original error: {str(e)}"
            )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in simple_chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/conversation", response_model=ConversationResponse)
async def create_conversation():
    """
    Start a new conversation and return a session ID.
    """
    if not LLAMA_ENABLE:
        return {"response": "Llama model is disabled in configuration. Please enable it to use this feature."}
        
    session_id = str(uuid.uuid4())
    set_conversation_history(session_id, [])
    return {"response": "Conversation started. Hello! How can I help you today?", "session_id": session_id}

@router.post("/conversation/{session_id}", response_model=ConversationResponse)
async def chat(session_id: str, request: ConversationRequest):
    """
    Continue a conversation using the Llama model.
    """
    if not LLAMA_ENABLE:
        return {"response": "Llama model is disabled in configuration. Please enable it to use this feature."}
        
    # Get or initialize conversation history
    history = get_conversation_history(session_id)
    
    # Add user messages to history
    for message in request.messages:
        add_to_conversation_history(session_id, message)
    
    try:
        # Generate response using Llama
        response_text = await generate_llama_response(
            get_conversation_history(session_id),
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Add assistant response to history
        assistant_message = Message(role="assistant", content=response_text)
        add_to_conversation_history(session_id, assistant_message)
        
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Error generating conversation response: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")
