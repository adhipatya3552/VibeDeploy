import json
from utils.state import get_model

class BackendAgent:
    def __init__(self):
        self.model = get_model()
        self.system_prompt = """
You are the Lead Backend Developer at VibeDeploy.
Your job is to write a complete, clean, and functional FastAPI backend in Python based on the designed database schema and features.

You will receive:
- Product name
- Core features
- Tech stack
- Database schema (tables, columns, types, relations)

You MUST generate the following files:
1. `main.py`: Entry point. Creates tables (using models.Base.metadata.create_all), configures FastAPI app, includes routers, CORS middleware.
2. `database.py`: SQLAlchemy database configuration. Defines Base, engine, SessionLocal, and a get_db() dependency using SQLite (sqlite:///./app.db).
3. `models.py`: SQLAlchemy database models. Convert the schema tables and columns into SQLAlchemy columns, foreign keys, and relationships.
4. `schemas.py`: Pydantic models for request input, response output, and validation.
5. `routes.py`: FastAPI routes with standard CRUD operations (GET, POST, PUT, DELETE) for all primary tables, plus mock user registration and login endpoints with a simple authentication pattern.
6. `requirements.txt`: Python package requirements (fastapi, uvicorn, sqlalchemy, pydantic, passlib, etc.).

CRITICAL RULES:
- Write FULL, working, valid Python code. DO NOT write shortcuts, placeholders, or comments like '# TODO: implement here'. Every route must have real logic.
- SQLite is the default database for quick local testing.
- Make sure import statements in all files match and are correct (e.g. `from database import engine, Base, SessionLocal`, `import models`, `import schemas`).

Output a JSON object containing:
{
  "files": {
    "main.py": "string (content of main.py)",
    "database.py": "string (content of database.py)",
    "models.py": "string (content of models.py)",
    "schemas.py": "string (content of schemas.py)",
    "routes.py": "string (content of routes.py)",
    "requirements.txt": "string (content of requirements.txt)"
  }
}
Do not add any markdown formatting, explanations, or code fences. Just the raw JSON.
"""

    def run(self, state):
        """
        Executes the Backend Agent.
        Inputs: state dictionary containing 'product_name', 'features', 'stack', 'db_schema'
        Outputs: updated state dictionary containing 'backend_code'
        """
        print(f"[*] Backend Agent: Generating FastAPI code for '{state['product_name']}'")
        
        context = {
            "product_name": state["product_name"],
            "features": state["features"],
            "stack": state["stack"],
            "db_schema": state["db_schema"]
        }
        
        prompt = f"System Architecture Specs:\n{json.dumps(context, indent=2)}"
        
        response = self.model.generate_content(
            contents=[self.system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            data = json.loads(response.text.strip())
            state["backend_code"] = data.get("files", {})
            print(f"[+] Backend Agent: Generated {len(state['backend_code'])} files.")
        except Exception as e:
            print(f"[-] Backend Agent: Error parsing JSON: {e}")
            # Fallback code
            state["backend_code"] = {
                "main.py": "# Error generating main.py\nfrom fastapi import FastAPI\napp = FastAPI()\n",
                "requirements.txt": "fastapi\nuvicorn\n"
            }
            
        return state
