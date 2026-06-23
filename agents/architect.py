import json
from utils.state import get_model

class ArchitectAgent:
    def __init__(self):
        self.model = get_model()
        self.system_prompt = """
You are the Lead Software Architect at VibeDeploy.
Your job is to design a clean, professional database schema and define the technology stack for a requested SaaS.

You will receive the product name, description, and core features.
Output a JSON object containing:
1. `stack`: A dictionary defining:
   - `backend`: "FastAPI (Python)"
   - `frontend`: "Next.js (React + Tailwind CSS)"
   - `db`: "SQLite / PostgreSQL"
2. `db_schema`: An array of tables. Each table must have:
   - `table_name`: lowercase name (e.g., "invoices", "users")
   - `description`: What data this table represents
   - `columns`: An array of columns. Each column must contain:
     - `name`: column name
     - `type`: SQL data type (e.g., "INTEGER", "VARCHAR(255)", "BOOLEAN", "TEXT", "TIMESTAMP", "DECIMAL(10, 2)")
     - `primary_key`: boolean
     - `foreign_key`: string (optional, e.g., "users.id", or null)
     - `nullable`: boolean
     - `unique`: boolean
     - `description`: brief explanation of what the column stores

Ensure you design standard necessary tables for a SaaS:
- A `users` table for authentication
- Other tables relevant to the core features (e.g. `invoices`, `clients` for an invoice tracking app)
- Appropriate primary and foreign key references to link the tables.

You MUST respond ONLY with a valid JSON object matching the following structure:
{
  "stack": {
    "backend": "string",
    "frontend": "string",
    "db": "string"
  },
  "db_schema": [
    {
      "table_name": "string",
      "description": "string",
      "columns": [
        {
          "name": "string",
          "type": "string",
          "primary_key": boolean,
          "foreign_key": "string" or null,
          "nullable": boolean,
          "unique": boolean,
          "description": "string"
        }
      ]
    }
  ]
}
Do not add any markdown formatting, explanations, or code fences. Just the raw JSON.
"""

    def run(self, state):
        """
        Executes the Architect agent.
        Inputs: state dictionary containing 'product_name', 'description', 'features'
        Outputs: updated state dictionary containing 'stack' and 'db_schema'
        """
        print(f"[*] Architect Agent: Designing architecture for '{state['product_name']}'")
        
        context = {
            "product_name": state["product_name"],
            "description": state["description"],
            "features": state["features"]
        }
        
        prompt = f"Product Details:\n{json.dumps(context, indent=2)}"
        
        response = self.model.generate_content(
            contents=[self.system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            data = json.loads(response.text.strip())
            state["stack"] = data.get("stack", {
                "backend": "FastAPI (Python)",
                "frontend": "Next.js (React + Tailwind CSS)",
                "db": "SQLite / PostgreSQL"
            })
            state["db_schema"] = data.get("db_schema", [])
            print(f"[+] Architect Agent: Designed {len(state['db_schema'])} tables.")
        except Exception as e:
            print(f"[-] Architect Agent: Error parsing JSON: {e}")
            # Fallback schema
            state["stack"] = {
                "backend": "FastAPI (Python)",
                "frontend": "Next.js (React + Tailwind CSS)",
                "db": "SQLite"
            }
            state["db_schema"] = [
                {
                    "table_name": "users",
                    "description": "Stores user profiles",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "primary_key": True, "nullable": False, "unique": False, "description": "Unique key"},
                        {"name": "email", "type": "VARCHAR(255)", "primary_key": False, "nullable": False, "unique": True, "description": "Login email"},
                        {"name": "hashed_password", "type": "VARCHAR(255)", "primary_key": False, "nullable": False, "unique": False, "description": "Hashed pass"}
                    ]
                }
            ]
            
        return state
