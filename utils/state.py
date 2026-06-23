import os
import time
from dotenv import load_dotenv
from google import genai

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, "..", ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

class GenAIClientWrapper:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def generate_content(self, contents, generation_config=None):
        """
        Maintains backward compatibility with google-genai generate_content structure.
        """
        config_dict = {}
        if generation_config:
            if "response_mime_type" in generation_config:
                config_dict["response_mime_type"] = generation_config["response_mime_type"]
                
        retries = 6
        delay = 8
        for i in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config_dict if config_dict else None
                )
                return response
            except Exception as e:
                err_str = str(e)
                if any(x in err_str for x in ["429", "503", "Quota exceeded", "ResourceExhausted", "UNAVAILABLE"]):
                    print(f"[*] API Rate Limit / High Demand hit: {err_str}. Sleeping for {delay}s before retrying... (Attempt {i+1}/{retries})")
                    time.sleep(delay)
                    delay = min(delay * 2, 60)
                else:
                    raise e
        
        # Final fallback try
        return self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config_dict if config_dict else None
        )

def get_model(model_name: str = None):
    resolved = model_name or os.environ.get("VIBEDEPLOY_MODEL") or MODEL
    return GenAIClientWrapper(client, resolved)

def fresh_state():
    return {
        "user_input": "",
        "product_name": "",
        "description": "",
        "features": [],
        "stack": {},
        "db_schema": [],
        "backend_code": {},
        "frontend_code": {},
        "marketing_copy": {}
    }