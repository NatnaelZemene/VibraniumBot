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
    Generate a multiple-choice question about Python programming or algorithms. 
    Mix it up: sometimes generate core algorithmic conceptual questions (time complexity, lists, trees), and other times generate tricky Python snippet questions.
    
    If the question requires reading Python code, place the code inside the "context" field wrapped EXACTLY like this to get colorful syntax highlighting in Telegram:
    <pre><code class="language-python">
    def your_code_here():
        pass
    </code></pre>
    
    Format the response STRICTLY as a JSON object with this exact structure and NO markdown wrapping:
    {
        "context": "Any introductory text or colorful HTML code snippet. (Can be an empty string if no code is needed)",
        "question": "The actual question text (e.g. 'What is the output?', 'What is the time complexity?'). PLAIN TEXT ONLY.",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_option_id": 0,
        "explanation": "A concise explanation. PLAIN TEXT ONLY. Use `backticks` for code snippets. DO NOT use HTML tags."
    }
    
    CRITICAL RESTRICTIONS (for Telegram API compatibility):
    1. "question" MUST NOT exceed 290 characters and must be PLAIN TEXT ONLY (no HTML tags).
    2. "options" must contain EXACTLY 4 entries, each under 95 characters (PLAIN TEXT ONLY).
    3. "explanation" MUST NOT exceed 150 characters (Plain text only, absolute NO HTML).
    4. "correct_option_id" must be an integer (0, 1, 2, or 3).
    5. Deliver standard VALID JSON. Do NOT wrap inside ```json or ``` blocks.
    6. Escape all internal quotes properly so the JSON remains valid.
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
