import os
import json
import logging
from google import genai

logger = logging.getLogger(__name__)

def generate_question():
    """Converse with Gemini to fetch a new programming question with a retry mechanism."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in environment variables.")
        return None

    client = genai.Client(api_key=api_key)
    model_id = 'gemini-2.5-flash'
    
    prompt = """
    You are a highly-skilled Python programming educator.
    Generate a tricky, advanced multiple-choice question about Python programming.
    Include short code snippets in the question if possible, but keep it concise.
    Focus on concepts such as decorators, closures, advanced list comprehensions, time complexity, or subtle language quirks.
    
    Format the response STRICTLY as a JSON object with this exact structure and NO markdown wrapping:
    {
        "question": "The text of the question? Use HTML <code> or <pre> tags for Python code.",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_option_id": 0,
        "explanation": "A concise explanation. Use HTML <code> tags for code snippets."
    }
    
    CRITICAL RESTRICTIONS (for Telegram API compatibility):
    1. "question" MUST NOT exceed 290 characters (excluding HTML tags).
    2. Each string inside the "options" array MUST NOT exceed 95 characters (PLAIN TEXT ONLY, NO HTML).
    3. "explanation" MUST NOT exceed 195 characters (excluding HTML tags).
    4. "options" must contain EXACTLY 4 entries.
    5. "correct_option_id" must be an integer (0, 1, 2, or 3).
    6. Deliver standard VALID JSON. Do NOT wrap inside ```json or ``` blocks.
    7. Use standard HTML tags (<code>, <b>, <i>, <pre>) for formatting in 'question' and 'explanation'. DO NOT use markdown backticks!
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Generating question... (Attempt {attempt + 1}/{max_retries})")
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
            )
            text = response.text.strip()
            
            # Clean up potential markdown code blocks
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            question_data = json.loads(text.strip())
            
            # Basic validation
            if "question" in question_data and len(question_data.get("options", [])) == 4:
                return question_data
            else:
                logger.warning(f"Invalid format received from Gemini: {question_data}")
                
        except json.JSONDecodeError as je:
            logger.warning(f"JSON decode failed on attempt {attempt + 1}: {je}\nRaw output: {text}")
        except Exception as e:
            logger.error(f"Failed to generate question from Gemini AI on attempt {attempt + 1}: {e}", exc_info=True)
            
    logger.error("All attempts to generate a question failed.")
    return None
