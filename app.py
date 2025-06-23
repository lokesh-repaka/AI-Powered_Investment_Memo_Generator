

# Note the import change here
from financial_analyzer import setup_rag_pipeline
from market_research import MarketResearchAgent
from memo_generator import run_phase_3



import streamlit as st
import os
import json
from dotenv import load_dotenv

# Updated imports for the new class-based approach
# from phase1_analyzer import setup_rag_pipeline
# from phase2_market_research import MarketResearchAgent
# from phase3_memo_generator import run_phase_3

# --- Page Configuration ---
st.set_page_config(page_title="Investment Memo AI", page_icon="📈", layout="wide")
load_dotenv()

# --- App Title and Description ---
st.title("📈 AI-Powered Investment Memo Generator")
# st.markdown("This tool automates investment memo creation by analyzing financial documents and market data.")
st.markdown("""
    This application automates the creation of an investment memo by orchestrating three phases:
    1.  **Financial Analysis**: Extracts key data from your uploaded PDF, with caching for speed.
    2.  **Market Research**: Conducts detailed web searches on the company's market landscape.
    3.  **Memo Synthesis**: Combines all data into a professional investment memo.
""")

# st.info("ℹ️ Check your terminal/console for detailed real-time progress logs.")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Inputs")
    company_name = st.text_input("Enter Company Name", placeholder="e.g., Tesla")
    uploaded_file = st.file_uploader("Upload Financial Document (PDF)", type="pdf")
    generate_button = st.button("Generate Investment Memo", type="primary", use_container_width=True)
    # st.warning("⚠️ Ensure your `.env` file contains necessary API keys.")

# --- Main Application Logic ---
if generate_button:
    if not company_name or not uploaded_file:
        st.warning("Please provide both a company name and a PDF file.")
    else:
        # 1. Create company-specific output directory
        safe_company_name = company_name.lower().replace(' ', '_')
        output_dir = os.path.join("company_reports", safe_company_name)
        os.makedirs(output_dir, exist_ok=True)
        # st.success(f"Output folder created/verified at: `{output_dir}`")

        try:
            # === PHASE 1: FINANCIAL DOCUMENT ANALYSIS (WITH GRANULAR SPINNERS) ===
            financial_output_path = os.path.join(output_dir, "financial_analysis_output.json")
            if not os.path.exists(financial_output_path):
                with st.spinner(f"Phase 1: Preparing and indexing document for {company_name}..."):
                    rag_engine = setup_rag_pipeline(uploaded_file, output_dir)
                analysis_sections = {
                    "Detailed Financial Statements": "Summarize the key figures from the financial statements, including revenues, net income, and cash flow.",
                    "Management Discussion and Analysis (MD&A)": "What is management's explanation for the company's financial results and operational performance?",
                    "Business Overview": "Describe the company's core operations, main products or services, and business segments.",
                    "Risk Factors": "List and summarize the most significant business, operational, and regulatory risks.",
                    "Legal Proceedings": "Are there any significant pending lawsuits or regulatory investigations mentioned?",
                    "Executive Compensation and Ownership": "Detail the compensation for top executives and major shareholders.",
                    "Corporate Governance": "Summarize the key aspects of corporate governance, such as board composition.",
                    "Material Contracts and Subsidiaries": "Describe any major agreements, partnerships, or subsidiary structure.",
                    "Properties": "What does the document say about the company's principal properties, facilities, or leases?",
                    "Quarterly Updates": "What are the latest material developments or updated guidance?",
                }
                financial_results = {}
                for section, question in analysis_sections.items():
                    with st.spinner(f"Analyzing '{section}' of {company_name}..."):
                        answer = rag_engine.query(question)
                        financial_results[section] = answer.strip()
                with open(financial_output_path, "w", encoding="utf-8") as f:
                    json.dump(financial_results, f, indent=4)
                st.success("Financial Document Analysis Complete!")
            else:
                st.success("✅ Found cached financial analysis. Skipping")

            # === PHASE 2: MARKET RESEARCH (WITH GRANULAR SPINNERS) ===
            market_output_path = os.path.join(output_dir, f"market_research_{safe_company_name}.json")
            if not os.path.exists(market_output_path):
                research_agent = MarketResearchAgent()
                
                # === THIS IS THE FULL, RESTORED RESEARCH STRUCTURE ===
                research_structure = {
                    "Competitive Landscape": [
                        f"Direct and indirect competitors of {company_name}",
                        f"Market positioning of {company_name}'s main competitors",
                        f"Business models and strategies of competitors to {company_name}",
                        f"Competitive advantages and disadvantages of {company_name}"
                    ],
                    "Market Trends and Dynamics": [
                        f"Current industry trends and growth drivers for the industry {company_name} is in",
                        f"Market size and growth projections for {company_name}'s primary market",
                        f"Emerging technologies and potential disruptions in {company_name}'s industry",
                        f"Regulatory changes affecting {company_name} and its industry"
                    ],
                    "Industry Analysis": [
                        f"Structure and key players in the industry of {company_name}",
                        f"Barriers to entry and competitive moats in {company_name}'s industry",
                        f"Supply chain dynamics for companies like {company_name}",
                        f"Customer behavior and preferences in {company_name}'s market segment"
                    ],
                    "Recent News and Developments": [
                        f"Recent news and major announcements from {company_name} in the last 12 months",
                        f"Significant industry developments and partnerships affecting {company_name}",
                        f"Recent analyst opinions and ratings for {company_name}'s stock",
                        f"Market sentiment and investor perception of {company_name}"
                    ],
                    "Competitive Intelligence": [
                        f"Latest financial performance of {company_name}'s key competitors",
                        f"Recent product launches and innovations from competitors of {company_name}",
                        f"Strategic initiatives and acquisitions by competitors of {company_name}",
                        f"Market share analysis for {company_name} and its main rivals"
                    ]
                }
                # =========================================================

                full_research_results = {}
                for main_topic, sub_topics in research_structure.items():
                    with st.spinner(f"Researching '{main_topic}' of {company_name}..."):
                        topic_results = research_agent.research_topic(main_topic, sub_topics)
                        full_research_results[main_topic] = topic_results
                with open(market_output_path, 'w', encoding='utf-8') as f:
                    json.dump(full_research_results, f, indent=4)
                st.success("✅ Market Research Complete!")
            else:
                st.success("✅ Found cached market research. Skipping")
            
            # === PHASE 3: MEMO GENERATION ===
            with st.spinner("Synthesizing the final investment memo ..."):
                memo_path = run_phase_3(
                    company_name=company_name,
                    market_report_path=market_output_path,
                    financial_data_path=financial_output_path,
                    output_dir=output_dir
                )
            st.success("🎉 All Phases Complete! Investment Memo Generated.")

            # --- Display Final Output and Download Button ---
            st.subheader(f"Download Your Investment Memo for {company_name}")
            
            # --- CHANGED: Now reads and downloads the .md file ---
            with open(memo_path, "rb") as md_file:
                st.download_button(
                    label="Download Memo (Markdown)",
                    data=md_file.read(),
                    file_name=os.path.basename(memo_path),
                    mime="text/markdown" # Correct MIME type for Markdown
                )
            
            # st.info(f"All generated files are saved in the `{output_dir}` folder.")
        except Exception as e:
            st.error(f"An error occurred during the process: {e}")
            import traceback
            traceback.print_exc()

