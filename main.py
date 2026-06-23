import os
import sys
import shutil
from utils.state import fresh_state
from utils.zipper import create_zip
from agents.orchestrator import OrchestratorAgent
from agents.architect import ArchitectAgent
from agents.backend import BackendAgent
from agents.frontend import FrontendAgent
from agents.marketing import MarketingAgent

def main():
    print("=" * 60)
    print(" VibeDeploy CLI Pipeline ".center(60, "="))
    print("=" * 60)
    
    # Check for GEMINI_API_KEY
    if not os.getenv("GEMINI_API_KEY"):
        print("[!] Warning: GEMINI_API_KEY environment variable is not set.")
        print("Please check your .env file or export the variable before running.")
        sys.exit(1)
        
    # Get user prompt
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = input("Enter your SaaS idea: ")
        
    if not user_prompt.strip():
        print("[-] Error: Prompt cannot be empty.")
        sys.exit(1)
        
    # Initialize state
    state = fresh_state()
    state["user_input"] = user_prompt
    
    # Initialize agents
    orchestrator = OrchestratorAgent()
    architect = ArchitectAgent()
    backend = BackendAgent()
    frontend = FrontendAgent()
    marketing = MarketingAgent()
    
    # Run the pipeline
    print("\n[Step 1/5] Running Orchestrator Agent...")
    state = orchestrator.run(state)
    
    print("\n[Step 2/5] Running Architect Agent...")
    state = architect.run(state)
    
    print("\n[Step 3/5] Running Backend Agent...")
    state = backend.run(state)
    
    print("\n[Step 4/5] Running Frontend Agent...")
    state = frontend.run(state)
    
    print("\n[Step 5/5] Running Marketing Agent...")
    state = marketing.run(state)
    
    # Packaging code
    product_slug = state["product_name"].lower().replace(" ", "_")
    output_dir = os.path.join("output", product_slug)
    
    print(f"\n[*] Packaging code to '{output_dir}/'...")
    
    # Clear directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save backend files
    backend_dir = os.path.join(output_dir, "backend")
    os.makedirs(backend_dir, exist_ok=True)
    for filename, content in state["backend_code"].items():
        with open(os.path.join(backend_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)
            
    # Save frontend files
    frontend_dir = os.path.join(output_dir, "frontend")
    os.makedirs(frontend_dir, exist_ok=True)
    for filename, content in state["frontend_code"].items():
        # Ensure directories exist for frontend files (e.g., pages/index.jsx, components/Auth.jsx)
        full_filepath = os.path.join(frontend_dir, filename)
        os.makedirs(os.path.dirname(full_filepath), exist_ok=True)
        with open(full_filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    # Save README.md to output folder
    readme_path = os.path.join(output_dir, "README.md")
    readme_content = state["marketing_copy"].get("readme")
    if not readme_content:
        readme_content = f"# {state['product_name']}\n\n{state['description']}\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Create ZIP archive
    zip_bytes = create_zip(
        backend_files=state["backend_code"],
        frontend_files=state["frontend_code"],
        product_name=state["product_name"],
        description=state["description"],
        marketing_copy=state["marketing_copy"]
    )
    
    zip_path = os.path.join("output", f"{product_slug}.zip")
    with open(zip_path, "wb") as f:
        f.write(zip_bytes)
        
    print(f"\n[+] Success! Complete workspace generated:")
    print(f"  - Source files directory: {output_dir}")
    print(f"  - Downloadable ZIP: {zip_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
