from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import insert_message, get_messages_by_email
from ai_service import get_ai_response

app = FastAPI(title="AI Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-chatbot-frontend.onrender.com",
        "https://*.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageInput(BaseModel):
    content: str
    email: str


class Message(BaseModel):
    id: str
    role: str
    content: str
    email: str
    created_at: datetime


class MessagesResponse(BaseModel):
    messages: List[Message]
    status: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Chat API",
        "version": "1.0.0",
        "endpoints": {
            "get_messages": "/api/messages",
            "send_message": "/api/messages (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/messages", response_model=List[Message])
async def get_messages(email: str):
    """
    Get all chat messages for a specific email from the database.
    
    Args:
        email: User email address
    
    Returns:
        List of messages for this email ordered by creation time
    """
    try:
        if not email or not email.strip():
            raise HTTPException(status_code=400, detail="Email is required")
        
        messages = await get_messages_by_email(email.strip().lower())
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")


@app.post("/api/messages")
async def send_message(message_input: MessageInput):
    """
    Send a user message and get AI response.
    
    Process:
    1. Save user message to database with email
    2. Call AI service (with fallback)
    3. Save AI response to database with same email
    4. Return both messages
    
    Args:
        message_input: User message content and email
    
    Returns:
        User message and AI response
    """
    try:
        if not message_input.content or not message_input.content.strip():
            raise HTTPException(status_code=400, detail="Message content cannot be empty")
        
        if not message_input.email or not message_input.email.strip():
            raise HTTPException(status_code=400, detail="Email is required")
        
        email = message_input.email.strip().lower()
        
        user_message = await insert_message("user", message_input.content, email)
        
        ai_response_text = await get_ai_response(message_input.content)
        
        ai_message = await insert_message("assistant", ai_response_text, email)
        
        return {
            "user_message": user_message,
            "ai_message": ai_message,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
