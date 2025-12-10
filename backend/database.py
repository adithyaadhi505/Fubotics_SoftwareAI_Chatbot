import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def insert_message(role: str, content: str, email: str):
    """
    Insert a new message into the database.
    
    Args:
        role: Either 'user' or 'assistant'
        content: The message content
        email: User email address
    
    Returns:
        The inserted message data
    """
    try:
        response = supabase.table("messages").insert({
            "role": role,
            "content": content,
            "email": email
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error inserting message: {e}")
        raise


async def get_messages_by_email(email: str):
    """
    Fetch all messages for a specific email ordered by creation time.
    
    Args:
        email: User email address
    
    Returns:
        List of messages for this email
    """
    try:
        response = supabase.table("messages").select("*").eq("email", email).order("created_at", desc=False).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching messages: {e}")
        raise


async def test_connection():
    """
    Test the database connection.
    
    Returns:
        True if connection is successful
    """
    try:
        response = supabase.table("messages").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
