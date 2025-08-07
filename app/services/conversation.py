# app/services/conversation.py
# Service for conversation with Llama model

import asyncio
import logging
from .model_loader import get_llama_model
from ..models.conversation import Message
from ..config import LLAMA_ENABLE, LLAMA_MAX_TOKENS

# Setup logging
logger = logging.getLogger(__name__)

# In-memory storage for conversation history
conversation_history = {}

async def generate_llama_response(messages, max_tokens=LLAMA_MAX_TOKENS, temperature=0.7):
    """
    Generate a response using the Llama model based on conversation history.
    """
    llama_model = get_llama_model()
    
    if llama_model is None:
        if not LLAMA_ENABLE:
            return "Llama model is disabled in configuration. Please enable it to use this feature."
        else:
            raise RuntimeError("Llama model not loaded. Check server logs for details.")
    
    try:
        # Format messages into a simple prompt format that works with Llama 2
        prompt = ""
        for msg in messages:
            if msg.role == "user":
                prompt += f"USER: {msg.content}\n"
            else:
                prompt += f"ASSISTANT: {msg.content}\n"
        
        # Add the final assistant prompt
        prompt += "ASSISTANT:"
        
        logger.info(f"Using prompt: {prompt[:100]}...")
        
        # Generate response using the completion method (which works with our test)
        response = await asyncio.to_thread(
            llama_model.create_completion,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["USER:"]
        )
        
        logger.info(f"Response generated successfully: {str(response)[:200]}...")
        
        # Extract the text from the response
        if response and "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["text"]
        else:
            logger.warning("No text found in response")
            return "I'm sorry, I couldn't generate a response."
            
    except Exception as e:
        logger.error(f"Error during response generation: {e}")
        raise RuntimeError(f"Failed to generate response: {str(e)}")

def get_conversation_history(session_id: str):
    """
    Get the conversation history for a session
    """
    return conversation_history.get(session_id, [])

def set_conversation_history(session_id: str, history: list):
    """
    Set the conversation history for a session
    """
    conversation_history[session_id] = history

def add_to_conversation_history(session_id: str, message: Message):
    """
    Add a message to the conversation history
    """
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    conversation_history[session_id].append(message)
    
    # Limit conversation history to prevent context window overflow
    if len(conversation_history[session_id]) > 20:  # Arbitrary limit
        conversation_history[session_id] = conversation_history[session_id][-20:]
