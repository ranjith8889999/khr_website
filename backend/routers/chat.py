"""
AI chat endpoint:     POST /api/chat
Test email endpoint:  POST /api/test-email
"""

import os
import pathlib
import traceback

from fastapi import APIRouter, HTTPException, BackgroundTasks
from groq import Groq

from ..schemas import ChatRequest, TestEmailRequest
from ..email_utils import send_test_email

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

# Initialise Groq client once at module load (env already loaded by app.py)
groq_client = None
try:
    _key = os.getenv('GROQ_API_KEY')
    if _key:
        groq_client = Groq(api_key=_key)
    else:
        print("WARNING: GROQ_API_KEY not set. AI chat will be unavailable.")
except Exception as _e:
    print(f"WARNING: Failed to initialise Groq client: {_e}")


@router.post('/api/chat')
async def chat(data: ChatRequest):
    if groq_client is None:
        raise HTTPException(
            status_code=503,
            detail='AI service not configured. Please contact administrator.',
        )

    user_message = data.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail='Message is required')

    kb_path = BASE_DIR / 'khr_knowledge_base.txt'
    try:
        knowledge_base = kb_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        knowledge_base = "Knowledge base not available."

    system_prompt = f"""You are an AI assistant specifically designed to answer questions about Kolan Hanmanth Reddy, a political leader from Telangana, India.

CRITICAL RESTRICTION - MUST FOLLOW:
⚠️ ABSOLUTE MAXIMUM: 300 WORDS PER RESPONSE - NO EXCEPTIONS! Count your words and STOP at 300 words maximum. This is mandatory.

IMPORTANT RULES:
1. ONLY answer questions related to Kolan Hanmanth Reddy, his work, vision, political career, constituency, initiatives, or related topics
2. If a question is NOT related to Kolan Hanmanth Reddy, politely respond with a friendly message like: "I'm specialized in providing information about Kolan Hanmanth Reddy and his work. Please feel free to ask me anything about his political career, vision, initiatives, or constituency work!"
3. Be friendly, professional, conversational, and informative
4. Provide accurate information ONLY from the knowledge base below
5. If information is not in the knowledge base, acknowledge that you don't have that specific detail but offer related information if available
6. Use natural, conversational language - avoid being too formal or robotic
7. For questions about his political journey/timeline/career, provide detailed chronological information from the knowledge base but stay within 300 words
8. FORMAT RESPONSES IN BULLET POINTS for easy reading:
   - Start with a brief intro sentence if needed
   - Use bullet points (•) for main information
   - Use sub-bullets or numbered lists for detailed timelines
   - Keep each bullet point concise and clear

COMPLETE KNOWLEDGE BASE ABOUT KOLAN HANMANTH REDDY:

{knowledge_base}

Remember: Use ONLY the information from the knowledge base above. Be accurate, helpful, and conversational. If someone asks about his political journey, provide the detailed timeline with years and positions held.
"""

    messages = [{'role': 'system', 'content': system_prompt}]
    if data.history:
        messages.extend(data.history[-20:])
    messages.append({'role': 'user', 'content': user_message})

    try:
        completion = groq_client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=messages,
            temperature=0.7,
            max_tokens=350,
            top_p=0.9,
            stream=False,
        )
        response_content = completion.choices[0].message.content.strip()
        return {'success': True, 'response': response_content}
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(
            status_code=500,
            detail='AI service temporarily unavailable. Please try again.',
        )


@router.post('/api/test-email')
async def test_email(data: TestEmailRequest):
    """Send a test email synchronously so the caller knows immediately if it worked."""
    recipient = data.email or os.getenv('MAIL_USERNAME', '')
    if not recipient:
        raise HTTPException(status_code=400, detail='No recipient email provided')
    try:
        await send_test_email(recipient)
        return {'success': True, 'message': f'Test email sent successfully to {recipient}'}
    except Exception as e:
        error_details = traceback.format_exc()
        print("EMAIL ERROR:\n", error_details)
        raise HTTPException(
            status_code=500,
            detail={'message': f'Failed to send email: {str(e)}', 'details': error_details},
        )
