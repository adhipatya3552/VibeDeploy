import json
from utils.state import get_model

class FrontendAgent:
    def __init__(self):
        self.model = get_model()
        self.system_prompt = """
You are the Lead Frontend Developer at VibeDeploy.
Your job is to design a stunning, responsive, and complete React/Next.js frontend using Tailwind CSS based on the backend routes and database schema.

You will receive:
- Product name
- Core features
- Database schema (tables, columns, types, relations)

You MUST generate the following files:
1. `pages/index.jsx` (or similar Next.js page): The main dashboard view. Show summary metrics, interactive listings of data from your schema tables, and forms to add/modify items. Use React state to make the table dynamically editable and simulate backend integration.
2. `components/Navbar.jsx`: A high-quality navigation bar featuring the product name, links to key views, and a mock profile dropdown.
3. `components/Metrics.jsx`: A component displaying key metric cards (e.g. Total Income, Outstanding, Active Clients) with vibrant colors and icons.
4. `components/Auth.jsx`: A modern login/registration screen card featuring glassmorphism elements, error handling, and clean visual inputs.
5. `package.json`: A standard package.json file containing standard Next.js dependencies (next, react, react-dom, lucide-react, tailwindcss, etc.).
6. `tailwind.config.js`: Tailwind configuration file.

CRITICAL RULES:
- Write FULL, valid React (JSX) code. Do NOT write placeholders, placeholders like '// TODO' must be avoided. Use real inline Tailwind CSS styles.
- Since we want to WOW the judges with visual excellence: use subtle gradients, modern dark mode design, clean margins, card structures, and soft shadows.
- Make all cards translucent glass containers: use `bg-slate-900/40 backdrop-blur-xl border border-white/[0.06] shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]`.
- Buttons must use gradients with shadow glows: `bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 shadow-[0_4px_15px_rgba(99,102,241,0.3)] transition-all`.
- Avoid long, ugly numeric IDs in tables. Truncate them or format them as clean short codes (e.g., `#INV-1002`, `#SUB-329` depending on the table context).
- Style status badges as capsules with a small colored indicator dot inside (e.g. glowing emerald dot for paid/active, amber for pending/paused).
- Include initials avatars for clients/users (e.g. "Acme Corp" -> "AC" circle).
- Import 'next/head' in page files and load the Google Font 'Outfit'. In `tailwind.config.js`, configure `Outfit` as the primary `sans` font family.
- Simulate api integration using React `useState` and `useEffect` so that the app works in the browser out-of-the-box even without a running database, while displaying hooks that indicate how they call the FastAPI backend endpoints (e.g., fetch('/api/invoices')). All interactive buttons and forms must modify local React state and work seamlessly.

Output a JSON object containing:
{
  "files": {
    "pages/index.jsx": "string (content of pages/index.jsx)",
    "components/Navbar.jsx": "string (content of components/Navbar.jsx)",
    "components/Metrics.jsx": "string (content of components/Metrics.jsx)",
    "components/Auth.jsx": "string (content of components/Auth.jsx)",
    "package.json": "string (content of package.json)",
    "tailwind.config.js": "string (content of tailwind.config.js)"
  }
}
Do not add any markdown formatting, explanations, or code fences. Just the raw JSON.
"""

    def run(self, state):
        """
        Executes the Frontend Agent.
        Inputs: state dictionary containing 'product_name', 'features', 'db_schema'
        Outputs: updated state dictionary containing 'frontend_code'
        """
        print(f"[*] Frontend Agent: Generating Next.js + Tailwind CSS UI for '{state['product_name']}'")
        
        context = {
            "product_name": state["product_name"],
            "features": state["features"],
            "db_schema": state["db_schema"]
        }
        
        prompt = f"Frontend User Experience Specifications:\n{json.dumps(context, indent=2)}"
        
        response = self.model.generate_content(
            contents=[self.system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            data = json.loads(response.text.strip())
            state["frontend_code"] = data.get("files", {})
            print(f"[+] Frontend Agent: Generated {len(state['frontend_code'])} files.")
        except Exception as e:
            print(f"[-] Frontend Agent: Error parsing JSON: {e}")
            # Fallback code
            state["frontend_code"] = {
                "pages/index.jsx": "// Error generating pages/index.jsx\nimport React from 'react';\nexport default function Home() { return <div>Home</div> }\n",
                "package.json": "{ \"dependencies\": { \"next\": \"latest\", \"react\": \"latest\" } }"
            }
            
        return state
