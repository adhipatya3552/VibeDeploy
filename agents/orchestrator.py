import json
from utils.state import get_model

class OrchestratorAgent:
    def __init__(self):
        self.model = get_model()
        self.system_prompt = """
You are the Lead Project Orchestrator at VibeDeploy.
Your job is to take a raw user request for a SaaS or web application and translate it into a structured product specification.

Analyze the user's request and output a JSON object containing:
1. `product_name`: A creative, catchy, and professional SaaS name (if the user didn't specify one).
2. `description`: A clear, professional, and detailed 2-3 sentence overview of what the SaaS does.
3. `features`: An array of 4-6 specific, actionable, and core features that are required to make this SaaS functional (e.g., "User Authentication: secure sign up and login", "Invoice Generation: form to create and customize PDF invoices"). Make sure they are developer-friendly descriptions.

You MUST respond ONLY with a valid JSON object matching the following structure:
{
  "product_name": "string",
  "description": "string",
  "features": ["string", "string", ...]
}
Do not add any markdown formatting, explanation, or code fences. Just the raw JSON.
"""

    def run(self, state):
        """
        Executes the Orchestrator agent.
        Inputs: state dictionary containing 'user_input'
        Outputs: updated state dictionary
        """
        print(f"[*] Orchestrator Agent: Analyzing idea -> '{state['user_input']}'")
        
        prompt = f"User Request: {state['user_input']}"
        
        response = self.model.generate_content(
            contents=[self.system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            data = json.loads(response.text.strip())
            state["product_name"] = data.get("product_name", "MySaaS")
            state["description"] = data.get("description", "A custom SaaS application.")
            state["features"] = data.get("features", [])
            print(f"[+] Orchestrator Agent: Identified Product -> '{state['product_name']}'")
            print(f"[+] Features: {state['features']}")
        except Exception as e:
            print(f"[-] Orchestrator Agent: Error parsing JSON: {e}")
            # Fallback values
            state["product_name"] = "VibeApp"
            state["description"] = state["user_input"]
            state["features"] = ["User Authentication", "Dashboard", "Main functionality"]
            
        return state
