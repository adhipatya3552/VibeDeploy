import streamlit as st
import os
import json
from utils.state import fresh_state, get_model
from utils.zipper import create_zip
from agents.orchestrator import OrchestratorAgent
from agents.architect import ArchitectAgent
from agents.backend import BackendAgent
from agents.frontend import FrontendAgent
from agents.marketing import MarketingAgent

# Configure Page
st.set_page_config(
    page_title="VibeDeploy - SaaS Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (Dark Theme & Glassmorphism)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply modern font */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0b0c10;
    color: #c5c6c7;
}

/* Streamlit container adjustments */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Glassmorphism Title Card */
.title-card {
    background: linear-gradient(135deg, rgba(31, 38, 135, 0.15) 0%, rgba(255, 255, 255, 0.03) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.title-card h1 {
    background: linear-gradient(90deg, #a855f7 0%, #ec4899 50%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.05em;
}

.title-card p {
    font-size: 1.2rem;
    color: #9ca3af;
    max-width: 700px;
    margin: 0 auto;
}

/* Cards style */
.glass-card {
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
}

.badge {
    background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 0.5rem;
}

/* Pricing Card Grid */
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.pricing-card {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.pricing-card:hover {
    transform: translateY(-5px);
    border-color: rgba(168, 85, 247, 0.4);
    box-shadow: 0 10px 30px rgba(168, 85, 247, 0.1);
}

.pricing-card.premium-tier {
    background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(236, 72, 153, 0.02) 100%);
    border: 1px solid rgba(168, 85, 247, 0.3);
}

.price-text {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f3f4f6;
    margin: 1rem 0;
}

/* Center the main generate button */
div[data-testid="stMainBlockContainer"] > div > div > div.stButton > button {
    display: block;
    margin: 0 auto;
}

/* Custom glowing button style */
div.stButton > button {
    background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    transition: all 0.2s ease !important;
    width: auto !important;
    min-width: 280px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background-color: #12131c;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Header & Configuration
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h2 style='background: linear-gradient(90deg, #a855f7 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;'>⚡ VibeDeploy</h2>
    <p style='color: #6b7280; font-size: 0.9rem;'>AI Multi-Agent SaaS Architect</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🤖 Model Selection")

GEMINI_MODELS = {
    # ── FREE TIER ──────────────────────────────────────────────────
    "🆕 Gemini 3.5 Flash (Free · Newest)":        "gemini-3.5-flash",
    "✅ Gemini 3.1 Flash Lite (Free · Default)":  "gemini-3.1-flash-lite",
    "🔬 Gemini 3 Flash Preview (Free)":           "gemini-3-flash-preview",
    "⚡ Gemini 2.5 Flash (Free)":                 "gemini-2.5-flash",
    "🪶 Gemini 2.5 Flash Lite (Free · Lightest)": "gemini-2.5-flash-lite",
    # ── PAID TIER ──────────────────────────────────────────────────
    "💎 Gemini 2.5 Pro (Paid)":                   "gemini-2.5-pro",
    "🏆 Gemini 3.1 Pro Preview (Paid)":           "gemini-3.1-pro-preview",
}

selected_model_label = st.sidebar.selectbox(
    "Choose Gemini Model",
    options=list(GEMINI_MODELS.keys()),
    index=1,   # default: Gemini 3.1 Flash Lite
    help="🆓 Free models work on any Google AI API key.\n💰 Paid models require a billing-enabled key."
)

selected_model_id = GEMINI_MODELS[selected_model_label]
os.environ["VIBEDEPLOY_MODEL"] = selected_model_id

is_paid = "Paid" in selected_model_label
tier_badge = "💰 Paid model — billing required" if is_paid else "🆓 Free tier model"
st.sidebar.caption(f"{tier_badge}  \nModel ID: `{selected_model_id}`")
st.sidebar.markdown("---")


st.sidebar.markdown("""
### Capstone Concept Map
VibeDeploy demonstrates:
* **Natural Language UI** (Vibe Coding)
* **Multi-Agent Collaboration**
* **Shared State Memory**
* **JSON Code Synthesis**
* **Direct File Packaging**
""")

# Main Landing Page View
st.markdown("""
<div class="title-card">
    <div class="badge">KAGLE VIBE CODING HACKATHON</div>
    <h1>VibeDeploy</h1>
    <p>Describe your software idea in simple English, and our team of five specialized AI agents will design the schema, write the FastAPI backend, develop the Next.js React frontend, and build a downloadable, ready-to-run ZIP archive.</p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State for results
if "generation_state" not in st.session_state:
    st.session_state["generation_state"] = None

# Input Box
default_prompt = "I want a SaaS where freelancers can track their clients, issue professional invoices, record payments, and view monthly earnings charts."
user_input = st.text_area(
    "What SaaS idea would you like to build today?",
    value=default_prompt,
    height=100,
    help="Type your idea. Be specific about features, tables, or design preferences if you have any."
)

_, btn_col, _ = st.columns([3, 2, 3])
with btn_col:
    generate_btn = st.button("🚀 Generate SaaS Platform", use_container_width=True)

# Executing Pipeline
if generate_btn:
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please ensure GEMINI_API_KEY is configured in your environment or secrets.")
    else:
        # Steps indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1. State setup
        state = fresh_state()
        state["user_input"] = user_input
        
        try:
            # Step 1: Orchestrator
            status_text.markdown("### 🧠 [1/5] Orchestrating Project Spec...")
            progress_bar.progress(10)
            orchestrator = OrchestratorAgent()
            state = orchestrator.run(state)
            
            # Step 2: Architect
            status_text.markdown("### 📐 [2/5] Designing DB Schema & Stack...")
            progress_bar.progress(30)
            architect = ArchitectAgent()
            state = architect.run(state)
            
            # Step 3: Backend
            status_text.markdown("### ⚙️ [3/5] Coding FastAPI Backend...")
            progress_bar.progress(50)
            backend = BackendAgent()
            state = backend.run(state)
            
            # Step 4: Frontend
            status_text.markdown("### 🎨 [4/5] Designing Next.js Tailwind UI...")
            progress_bar.progress(70)
            frontend = FrontendAgent()
            state = frontend.run(state)
            
            # Step 5: Marketing
            status_text.markdown("### 📈 [5/5] Generating Marketing Strategy & Pricing Tiers...")
            progress_bar.progress(90)
            marketing = MarketingAgent()
            state = marketing.run(state)
            
            progress_bar.progress(100)
            status_text.success("### 🎉 Success! Workspace generated successfully.")
            
            # Save results into Streamlit session state
            st.session_state["generation_state"] = state
            
        except Exception as e:
            st.error(f"Error executing agent pipeline: {e}")

# Render Results
if st.session_state["generation_state"] is not None:
    state = st.session_state["generation_state"]
    
    st.markdown("---")
    st.markdown(f"## 📦 Generated SaaS Workspace: **{state['product_name']}**")
    
    # Action Banner: Download Zip
    zip_bytes = create_zip(
        backend_files=state["backend_code"],
        frontend_files=state["frontend_code"],
        product_name=state["product_name"],
        description=state["description"],
        marketing_copy=state["marketing_copy"]
    )
    
    st.download_button(
        label=f"💾 Download {state['product_name']} Workspace (.ZIP)",
        data=zip_bytes,
        file_name=f"{state['product_name'].lower().replace(' ', '_')}_workspace.zip",
        mime="application/zip",
        key="zip_download"
    )
    
    # Split UI into tabs
    tab_overview, tab_backend, tab_frontend, tab_marketing = st.tabs([
        "📋 Overview & Database",
        "⚙️ FastAPI Backend Code",
        "🎨 React Frontend Components",
        "📈 Marketing Strategy"
    ])
    
    # 1. Overview & DB Schema Tab
    with tab_overview:
        col_desc, col_stack = st.columns([2, 1])
        with col_desc:
            st.markdown("### Product Description")
            st.info(state["description"])
            
            st.markdown("### Core Feature Set")
            for feat in state["features"]:
                st.markdown(f"- {feat}")
                
        with col_stack:
            st.markdown("### Architecture Stack")
            st.markdown(f"**Backend:** `{state['stack'].get('backend', 'FastAPI')}`")
            st.markdown(f"**Frontend:** `{state['stack'].get('frontend', 'Next.js')}`")
            st.markdown(f"**Database:** `{state['stack'].get('db', 'SQLite')}`")
            
        st.markdown("### Relational Database Schema")
        for table in state["db_schema"]:
            with st.expander(f"Table: {table.get('table_name')} — *{table.get('description')}*", expanded=True):
                # Build columns table
                columns_data = []
                for col in table.get("columns", []):
                    primary = "🔑 PK" if col.get("primary_key") else ""
                    foreign = f"🔗 FK ({col.get('foreign_key')})" if col.get("foreign_key") else ""
                    unique = "✔️ Unique" if col.get("unique") else ""
                    nullable = "Null" if col.get("nullable") else "Not Null"
                    
                    columns_data.append({
                        "Column": col.get("name"),
                        "Type": col.get("type"),
                        "Constraint": f"{primary} {foreign} {unique}".strip() or "None",
                        "Nullable": nullable,
                        "Description": col.get("description")
                    })
                st.table(columns_data)

    # 2. FastAPI Backend Code Tab
    with tab_backend:
        st.markdown("### Generated FastAPI Source Code")
        backend_files = state["backend_code"]
        if backend_files:
            file_to_view = st.selectbox("Select Backend File to View", list(backend_files.keys()))
            if file_to_view:
                st.code(backend_files[file_to_view], language="python")
        else:
            st.warning("No backend code generated.")

    # 3. Next.js React Frontend Tab
    with tab_frontend:
        st.markdown("### Generated Next.js React Components")
        frontend_files = state["frontend_code"]
        if frontend_files:
            file_to_view_fe = st.selectbox("Select Frontend File to View", list(frontend_files.keys()))
            if file_to_view_fe:
                extension = "json" if file_to_view_fe.endswith(".json") else "javascript"
                st.code(frontend_files[file_to_view_fe], language=extension)
        else:
            st.warning("No frontend code generated.")

    # 4. Marketing Tab
    with tab_marketing:
        copy = state["marketing_copy"]
        
        # Hero Headline preview
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Landing Page Preview</div>
            <h2 style="font-size: 2.2rem; font-weight: 700; color: #f3f4f6; margin-bottom: 0.5rem;">{copy.get('hero_headline', '')}</h2>
            <p style="font-size: 1.1rem; color: #9ca3af; max-width: 600px; margin: 0 auto 1.5rem;">{copy.get('hero_subheadline', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Strategic Value Propositions")
        for bullet in copy.get("copywriting_bullets", []):
            st.markdown(f"🚀 **{bullet}**")
            
        st.markdown("---")
        st.markdown("### Pricing Strategy & Subscription Tiers")
        
        # Create HTML Grid for Pricing Tiers
        pricing_cards_html = ""
        tiers = copy.get("pricing_tiers", [])
        for i, tier in enumerate(tiers):
            is_premium = "premium-tier" if i == 1 else ""  # Mark Pro (middle tier) as premium/featured
            badge_html = "<div style='color: #a855f7; font-weight: 600; font-size: 0.75rem; text-transform: uppercase;'>★ Most Popular</div>" if i == 1 else ""
            
            features_list_html = "".join(f"<li style='margin-bottom: 0.5rem; text-align: left; font-size: 0.9rem;'>✓ {f}</li>" for f in tier.get("features", []))
            
            pricing_cards_html += (
                f'<div class="pricing-card {is_premium}">'
                f'{badge_html}'
                f'<h3 style="font-size: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; color: #f3f4f6;">{tier.get("name")}</h3>'
                f'<p style="color: #9ca3af; font-size: 0.85rem; min-height: 40px;">{tier.get("target")}</p>'
                f'<div class="price-text">{tier.get("price")}</div>'
                f'<hr style="border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;" />'
                f'<ul style="list-style: none; padding: 0; margin: 0;">'
                f'{features_list_html}'
                f'</ul>'
                f'</div>'
            )
            
        st.html(f'<div class="pricing-grid">{pricing_cards_html}</div>')
