import os
import json
import logging
from google import genai

logger = logging.getLogger(__name__)

def generate_question():
    """Converse with Gemini to fetch a new programming question."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in environment variables.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        # We use a capable model, gemini-2.5-flash is universally supported in the new SDK
        model_id = 'gemini-2.5-flash'
        
        prompt = """
        You are a highly-skilled Python programming educator.
        Generate an interesting, single multiple-choice question about beginner algorithms in Python.
        Focus on concepts such as sorting, searching, array manipulation, recursion, or string operations.
        
        Format the response STRICTLY as a JSON object with this exact structure and NO markdown wrapping:
        {
            "question": "The text of the question?",
            "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
            "correct_option_id": 0,
            "explanation": "A short, 1-2 sentence explanation of why this option is correct."
        }
        
        Requirements:
        1. Keep the JSON payload perfectly valid.
        2. Ensure "options" contains exactly 4 entries.
        3. "correct_option_id" must be a number (0, 1, 2, or 3) representing the index of the correct string in the "options" array.
        4. No markdown formatting like ```json or code blocks around the response. Only Valid raw JSON text.
        """
        
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
        )
        text = response.text.strip()
        
        # In case the model still outputs markdown code blocks, gently clean it
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
        
    except Exception as e:
        logger.error(f"Failed to generate question from Gemini AI: {e}", exc_info=True)
        return None
