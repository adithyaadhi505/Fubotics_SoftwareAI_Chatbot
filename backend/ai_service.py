import os
from dotenv import load_dotenv
import google.generativeai as genai
from mistralai import Mistral

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in environment variables")
if not MISTRAL_API_KEY:
    raise ValueError("Mistral API key not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

mistral_client = Mistral(api_key=MISTRAL_API_KEY)


async def call_gemini(message: str) -> str:
    """
    Call Google Gemini API to get AI response.
    
    Args:
        message: User message
    
    Returns:
        AI response text
    """
    try:
        system_prompt = """You are a helpful AI assistant. Provide clear, natural, and well-structured responses.

CRITICAL: Choose the RIGHT format for each type of question!

DEFAULT FORMAT (Use 90% of the time):
Write in NATURAL PARAGRAPHS like you're having a conversation. Use this for:
- Advice (relationships, life, career, personal topics)
- Explanations and opinions
- Stories or examples
- General "how to" questions
- Any conversational topic

Add blank lines between paragraphs for readability. NO lists or numbering needed!

USE NUMBERED LISTS ONLY when:
- Giving technical step-by-step instructions (coding, recipes, procedures)
- Listing features, specifications, or distinct items to compare
- Order and sequence truly matter (do step 1, then step 2, etc.)

For lists: Start with a brief intro, then number main points (1. 2. 3.) with dashes (-) for sub-points.

FORMATTING RULES - EXTREMELY IMPORTANT:
- ABSOLUTELY NO MARKDOWN SYMBOLS: Never use asterisks (*), double asterisks (**), underscores (_), double underscores (__), hashtags (#), or ANY markdown formatting
- Use plain text only - no bold at all , italic, heading, or any special markers
- For emphasis: Use CAPITAL LETTERS or "quotation marks" instead of markdown
- Short paragraphs (2-4 sentences each)
- Blank lines between paragraphs
- Natural, conversational tone
- If highlighting technical terms or concepts, use quotation marks like "RNN" or capital letters

EXAMPLE - Advice/General (PARAGRAPHS):
"Proposing is such a special moment! The most important thing is making sure you both feel ready and have talked about your future together.

Think about what would be meaningful to her. Maybe propose somewhere special to your relationship—where you first met, her favorite place, or somewhere that holds memories for both of you. The location is less important than the genuine feeling behind it.

Make it personal to your relationship. Speak from your heart about why you love her and want to spend your life together. It doesn't need to be a perfect speech, just honest and sincere.

If you're getting a ring, try to match her style or ask someone close to her for guidance. You can also propose first and pick the ring together later if you're unsure.

Most importantly, be yourself. The best proposals feel authentic to the couple, whether they're grand or intimate. Trust your instincts and let your love show through!"

EXAMPLE - Technical (NUMBERED LIST):
"Here's how to create a React component:

1. Import React at the top of your file
2. Define your function component with a capital letter
3. Return JSX inside parentheses
4. Export the component at the bottom

Example: function MyComponent() returns your JSX code."

TONE:
- Warm and friendly
- Clear and helpful
- Natural flow, not robotic
- Match the question's vibe"""

        full_prompt = f"{system_prompt}\n\nUser question: {message}\n\nProvide a clear, natural response:"
        
        response = gemini_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise


async def call_mistral(message: str) -> str:
    """
    Call Mistral AI API to get AI response.
    
    Args:
        message: User message
    
    Returns:
        AI response text
    """
    try:
        system_prompt = """You are a helpful AI assistant. Provide clear, natural, and well-structured responses.

CRITICAL: Choose the RIGHT format for each type of question!

DEFAULT FORMAT (Use 90% of the time):
Write in NATURAL PARAGRAPHS like you're having a conversation. Use this for:
- Advice (relationships, life, career, personal topics)
- Explanations and opinions
- Stories or examples
- General "how to" questions
- Any conversational topic

Add blank lines between paragraphs for readability. NO lists or numbering needed!

USE NUMBERED LISTS ONLY when:
- Giving technical step-by-step instructions (coding, recipes, procedures)
- Listing features, specifications, or distinct items to compare
- Order and sequence truly matter (do step 1, then step 2, etc.)

For lists: Start with a brief intro, then number main points (1. 2. 3.) with dashes (-) for sub-points.

FORMATTING RULES - EXTREMELY IMPORTANT:
- ABSOLUTELY NO MARKDOWN SYMBOLS: Never use asterisks (*), double asterisks (**), underscores (_), double underscores (__), hashtags (#), or ANY markdown formatting
- Use plain text only - no bold at all , italic, heading, or any special markers
- For emphasis: Use CAPITAL LETTERS or "quotation marks" instead of markdown
- Short paragraphs (2-4 sentences each)
- Blank lines between paragraphs
- Natural, conversational tone
- If highlighting technical terms or concepts, use quotation marks like "RNN" or capital letters

EXAMPLE - Advice/General (PARAGRAPHS):
"Proposing is such a special moment! The most important thing is making sure you both feel ready and have talked about your future together.

Think about what would be meaningful to her. Maybe propose somewhere special to your relationship—where you first met, her favorite place, or somewhere that holds memories for both of you. The location is less important than the genuine feeling behind it.

Make it personal to your relationship. Speak from your heart about why you love her and want to spend your life together. It doesn't need to be a perfect speech, just honest and sincere.

If you're getting a ring, try to match her style or ask someone close to her for guidance. You can also propose first and pick the ring together later if you're unsure.

Most importantly, be yourself. The best proposals feel authentic to the couple, whether they're grand or intimate. Trust your instincts and let your love show through!"

EXAMPLE - Technical (NUMBERED LIST):
"Here's how to create a React component:

1. Import React at the top of your file
2. Define your function component with a capital letter
3. Return JSX inside parentheses
4. Export the component at the bottom

Example: function MyComponent() returns your JSX code."

TONE:
- Warm and friendly
- Clear and helpful
- Natural flow, not robotic
- Match the question's vibe"""

        response = mistral_client.chat.complete(
            model="mistral-medium-latest",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Mistral API error: {e}")
        raise


async def get_ai_response(message: str) -> str:
    """
    Get AI response with automatic fallback from Gemini to Mistral.
    
    Primary: Google Gemini 2.5
    Fallback: Mistral Medium
    
    Args:
        message: User message
    
    Returns:
        AI response text
    """
    try:
        print("Attempting to call Gemini...")
        response = await call_gemini(message)
        print("Gemini response received")
        return response
    except Exception as gemini_error:
        print(f"Gemini failed: {gemini_error}")
        print("Falling back to Mistral...")
        
        try:
            response = await call_mistral(message)
            print("Mistral response received")
            return response
        except Exception as mistral_error:
            print(f"Mistral also failed: {mistral_error}")
            error_message = "I'm sorry, I'm having trouble connecting to the AI service right now. Please try again later."
            return error_message
