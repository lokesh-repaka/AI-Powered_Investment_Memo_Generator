import os
import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

# --- REMOVED fpdf2 and all PDF-related functions ---

def run_phase_3(company_name: str, market_report_path: str, financial_data_path: str, output_dir: str) -> str:
    """
    Creates the final investment memo and saves it as a Markdown (.md) file.
    This version now checks for a cached .md file before running.
    """
    print("--- Starting Phase 3: Memo Synthesis ---")
    
    # --- CHANGED: Path now points to a .md file ---
    safe_company_name = company_name.lower().replace(' ', '_')
    md_output_path = os.path.join(output_dir, f"investment_memo_{safe_company_name}.md")

    if os.path.exists(md_output_path):
        print(f"✅ Found cached Investment Memo Markdown: '{md_output_path}'.")
        print("   Bypassing memo synthesis.")
        return md_output_path
    
    print(f"⚠️ No cached memo found. Proceeding with synthesis...")

    load_dotenv()
    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-70b-8192", temperature=0.1,rate_limiter=rate_limiter)
    
    with open(market_report_path, 'r', encoding='utf-8') as f: market_data = json.load(f)
    with open(financial_data_path, 'r', encoding='utf-8') as f: financial_data = json.load(f)

    full_text_content = f"# Comprehensive Research for {company_name}\n\n## Market Research\n{json.dumps(market_data, indent=2)}\n\n## Financial Analysis\n{json.dumps(financial_data, indent=2)}"
    docs = [Document(page_content=full_text_content)]
    split_docs = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500).split_documents(docs)

    initial_prompt_template = """You are a Senior Investment Analyst. Draft an investment memo for {company_name} based on the context below. Use the specified structure. If info is missing, state "Analysis requires more data."
**Investment Memo: {company_name}**
**1. Executive Summary & Recommendation:**
**2. Company Overview:**
**3. Market & Industry Analysis:**
**4. Competitive Landscape & Moat:**
**5. Financial Analysis & Valuation:**
**6. Key Risks & Mitigants:**
**7. Catalysts & Recent Developments:**
--- CONTEXT ---
{text}"""
    initial_prompt = PromptTemplate(
        template=initial_prompt_template,
        input_variables=["company_name", "text"]
    )
    
    refine_prompt_template = """You are refining an investment memo for {company_name}. Integrate the new context into the existing draft. The output must be the complete, updated memo.
--- EXISTING DRAFT ---
{existing_answer}
--- NEW CONTEXT ---
{text}"""
    refine_prompt = PromptTemplate(
        template=refine_prompt_template,
        input_variables=["company_name", "existing_answer", "text"]
    )
    
    print("🧠 Synthesizing memo with 'refine' chain...")
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=initial_prompt,
        refine_prompt=refine_prompt,
        verbose=True
    )
    
    result = chain.invoke({
        "input_documents": split_docs,
        "company_name": company_name
    })
    
    final_memo_text = result['output_text']

    # --- CHANGED: Now we just write the text to a .md file ---
    print(f"📄 Saving Markdown memo to: {md_output_path}")
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(final_memo_text)
    
    print("✅ Phase 3 Complete. Final memo generated as Markdown.")
    return md_output_path