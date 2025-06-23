

# import os
# import json
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate

# # --- MAIN FUNCTION TO BE CALLED BY STREAMLIT ---
# def run_phase_3(
#     company_name: str,
#     market_report_path: str,
#     financial_data_path: str,
#     status_updater
# ):
#     """
#     Creates the final investment memo.
#     Args:
#         company_name (str): The name of the company.
#         market_report_path (str): Path to the market research JSON file.
#         financial_data_path (str): Path to the financial analysis JSON file.
#         status_updater: The Streamlit status object to write logs to.
#     Returns:
#         The final investment memo as a string.
#     """
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         raise ValueError("GROQ_API_KEY not found in .env file.")

#     llm = ChatGroq(
#         groq_api_key=groq_api_key,
#         model_name="llama3-70b-8192",
#         temperature=0.1
#     )

#     status_updater.write("📄 Loading and processing source documents...")
#     try:
#         with open(market_report_path, 'r', encoding='utf-8') as f:
#             market_data = json.load(f)
#         with open(financial_data_path, 'r', encoding='utf-8') as f:
#             financial_data = json.load(f)

#         full_text_content = f"# Comprehensive Research for {company_name}\n\n## Market Research\n\n"
#         full_text_content += json.dumps(market_data, indent=2)
#         full_text_content += "\n\n## Financial Analysis from Document\n\n"
#         full_text_content += json.dumps(financial_data, indent=2)

#         all_docs = [Document(page_content=full_text_content)]
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=500)
#         split_docs = text_splitter.split_documents(all_docs)
#         status_updater.write(f"  - Documents processed and split into {len(split_docs)} chunks.")
    
#     except Exception as e:
#         status_updater.write(f"🔴 ERROR loading data: {e}")
#         return f"Error loading data: {e}"

#     initial_prompt_template = f"""You are a Senior Investment Analyst. Your task is to draft a comprehensive investment memo for {company_name}. Based *only* on the context below, begin drafting the memo. If you lack information for a section, state "Analysis requires more data."

#     **Investment Memo: {company_name}**

#     **1. Executive Summary & Recommendation:**

#     **2. Company Overview:**

#     **3. Market & Industry Analysis:**

#     **4. Competitive Landscape & Moat:**
    
#     **5. Financial Analysis & Valuation:**

#     **6. Key Risks & Mitigants:**
    
#     --- START OF CONTEXT ---
#     {{text}}
#     --- END OF CONTEXT ---

#     Begin the memo now.
#     """
#     initial_prompt = PromptTemplate(template=initial_prompt_template, input_variables=["text"])

#     refine_prompt_template = f"""You are a Senior Investment Analyst refining an investment memo for {company_name}. You have the existing draft and new context. Integrate the new information to deepen the analysis and fill in missing sections. The final output must be the complete, updated memo.

#     --- EXISTING DRAFT ---
#     {{existing_answer}}
#     --- END OF EXISTING DRAFT ---

#     --- NEW CONTEXT TO INTEGRATE ---
#     {{text}}
#     --- END OF NEW CONTEXT ---
    
#     Produce the new, refined, and more complete investment memo.
#     """
#     refine_prompt = PromptTemplate(template=refine_prompt_template, input_variables=["existing_answer", "text"])

#     status_updater.write("🧠 Synthesizing investment memo using 'refine' chain...")
#     chain = load_summarize_chain(
#         llm=llm,
#         chain_type="refine",
#         question_prompt=initial_prompt,
#         refine_prompt=refine_prompt,
#         return_intermediate_steps=False,
#     )
    
#     result = chain.invoke({"input_documents": split_docs})
#     status_updater.write("✅ Investment Memo synthesis complete!")
#     return result['output_text']


# phase3_memo_generator.py

# import os
# import json
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate

# def run_phase_3(
#     company_name: str,
#     market_report_path: str,
#     financial_data_path: str,
# ):
#     """Creates the final investment memo."""
#     print("✅ Initializing Synthesis Agent for Phase 3...")
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         raise ValueError("🔴 GROQ_API_KEY not found in .env file.")

#     llm = ChatGroq(
#         groq_api_key=groq_api_key,
#         model_name="llama3-70b-8192",
#         temperature=0.1
#     )
#     print(f"✅ Groq LLM model ready ({llm.model_name}).")

#     print(f"📄 Loading and processing source JSON documents...")
#     try:
#         with open(market_report_path, 'r', encoding='utf-8') as f:
#             market_data = json.load(f)
#         with open(financial_data_path, 'r', encoding='utf-8') as f:
#             financial_data = json.load(f)

#         # Correctly format the detailed, nested market research data
#         full_text_content = f"# Comprehensive Research for {company_name}\n\n"
#         full_text_content += "## Market Research Analysis\n\n"
#         for main_topic, sub_topics in market_data.items():
#             full_text_content += f"### {main_topic}\n\n"
#             for sub_topic_title, analysis_text in sub_topics.items():
#                 full_text_content += f"#### {sub_topic_title}\n{analysis_text}\n\n"

#         full_text_content += "## Financial Document Analysis\n\n"
#         full_text_content += json.dumps(financial_data, indent=2)

#         all_docs = [Document(page_content=full_text_content)]
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=500)
#         split_docs = text_splitter.split_documents(all_docs)

#     except Exception as e:
#         print(f"🔴 ERROR loading data: {e}")
#         return f"Error loading data: {e}"
#     print(f"✅ Documents processed and split into {len(split_docs)} chunks.")

#     # Prompts remain the same, they are robust enough
#     initial_prompt_template = f"""You are a Senior Investment Analyst. Draft an investment memo for {company_name} based on the context below.
#     **Investment Memo: {company_name}**
#     1. Executive Summary & Recommendation:
#     2. Company Overview:
#     3. Market & Industry Analysis:
#     4. Competitive Landscape & Moat:
#     5. Financial Analysis & Valuation:
#     6. Key Risks & Mitigants:
#     --- CONTEXT ---
#     {{text}}
#     --- END CONTEXT ---
#     """
#     initial_prompt = PromptTemplate(template=initial_prompt_template, input_variables=["text"])

#     refine_prompt_template = f"""You are refining an investment memo for {company_name}. You have the existing draft and new context. Integrate the new information to deepen the analysis. The final output must be the complete, updated memo.
#     --- EXISTING DRAFT ---
#     {{existing_answer}}
#     --- END DRAFT ---
#     --- NEW CONTEXT ---
#     {{text}}
#     --- END CONTEXT ---
#     """
#     refine_prompt = PromptTemplate(template=refine_prompt_template, input_variables=["existing_answer", "text"])

#     print("\n🚀 Executing 'refine' chain with Groq...")
#     chain = load_summarize_chain(
#         llm=llm,
#         chain_type="refine",
#         question_prompt=initial_prompt,
#         refine_prompt=refine_prompt,
#         return_intermediate_steps=False,
#     )
    
#     result = chain.invoke({"input_documents": split_docs})
#     print("✅ Investment Memo synthesis complete!")
#     return result['output_text']



# phase3_memo_generator.py

# import os
# import json
# from dotenv import load_dotenv

# # --- Core LangChain imports ---
# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate

# from langchain_core.rate_limiters import InMemoryRateLimiter

# rate_limiter = InMemoryRateLimiter(
#     requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
#     check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
#     max_bucket_size=10,  # Controls the maximum burst size.
# )

# def run_phase_3(
#     company_name: str,
#     market_report_path: str,
#     financial_data_path: str,
# ):
#     """
#     Creates a high-quality investment memo using a 'refine' chain strategy,
#     powered by the high-speed Groq API. This version uses the original, high-quality
#     prompts for professional-grade output.

#     Args:
#         company_name (str): The name of the company.
#         market_report_path (str): Path to the market research JSON file.
#         financial_data_path (str): Path to the financial analysis JSON file.
#     """
#     # --- 1. SETUP: LOAD API KEYS AND CONFIGURE LLM ---
#     print("✅ Initializing Synthesis Agent with high-speed GROQ strategy...")
#     load_dotenv()
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         raise ValueError("🔴 GROQ_API_KEY not found in .env file.")

#     llm = ChatGroq(
#         groq_api_key=groq_api_key,
#         model_name="llama3-70b-8192",
#         temperature=0.1,
#         rate_limiter=rate_limiter
#     )
#     print(f"✅ Groq LLM model ready ({llm.model_name}).")

#     # --- 2. LOAD AND PROCESS DOCUMENTS ---
#     print(f"📄 Loading and processing source JSON documents...")
#     try:
#         with open(market_report_path, 'r', encoding='utf-8') as f:
#             market_data = json.load(f)

#         with open(financial_data_path, 'r', encoding='utf-8') as f:
#             financial_data = json.load(f)

#         # Convert the structured JSON data into a single, well-formatted text string
#         full_text_content = f"# Comprehensive Research for {company_name}\n\n"

#         # Process market research data
#         full_text_content += "## Market Research Analysis\n\n"
#         for main_topic, sub_topics in market_data.items():
#             full_text_content += f"### {main_topic}\n\n"
#             for sub_topic_title, analysis_text in sub_topics.items():
#                 full_text_content += f"#### {sub_topic_title}\n{analysis_text}\n\n"

#         # Process and append financial data from the document
#         full_text_content += "## Financial Document Analysis\n\n"
#         full_text_content += json.dumps(financial_data, indent=2)

#         all_docs = [Document(page_content=full_text_content)]
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
#         split_docs = text_splitter.split_documents(all_docs)

#     except Exception as e:
#         print(f"🔴 ERROR loading data: {e}")
#         return f"Error loading data: {e}"
#     print(f"✅ Documents processed and split into {len(split_docs)} chunks.")

#     # --- 3. PROMPT ENGINEERING (YOUR ORIGINAL, HIGH-QUALITY PROMPTS) ---
#     print("🧠 Using your original, high-quality prompts for the investment memo...")
    
#     # === THIS IS YOUR ORIGINAL INITIAL PROMPT, RESTORED ===
#     initial_prompt_template = f"""
#     You are a Senior Investment Analyst at a top-tier hedge fund. Your task is to draft the initial version of a comprehensive investment memo for {company_name}.
    
#     An investment memo is a critical tool for disciplined thinking. It must provide a clear, evidence-based rationale for an investment decision. Your tone should be analytical, critical, and objective.

#     You have been given the first piece of research context. Based *only* on this context, begin drafting the memo using the structure below. If you lack information for a section, state "Analysis requires more data." Do not invent information.

#     **Investment Memo: {company_name}**

#     **1. Executive Summary & Recommendation:**
#     *Provide a brief overview of the thesis and a clear recommendation (e.g., BUY, HOLD, SELL). Start with "Analysis requires more data."*

#     **2. Company Overview:**
#     *What does the company do? What is its business model?*

#     **3. Market & Industry Analysis:**
#     *What are the key market trends, growth drivers, and market size?*

#     **4. Competitive Landscape & Moat:**
#     *Who are the main competitors? What is {company_name}'s sustainable competitive advantage (its 'moat')?*
    
#     **5. Financial Analysis & Valuation:**
#     *Summarize key financial metrics and analyst ratings.*

#     **6. Key Risks & Mitigants:**
#     *What are the primary risks (competitive, regulatory, technological) facing the company?*
    
#     **7. Catalysts & Recent Developments:**
#     *What recent news or product launches could significantly impact the company's valuation?*
    
#     --- START OF FIRST CONTEXT CHUNK ---
#     {{text}}
#     --- END OF FIRST CONTEXT CHUNK ---

#     Begin the memo now, adhering strictly to the provided structure and using only the information from the context chunk.
#     """
#     initial_prompt = PromptTemplate(template=initial_prompt_template, input_variables=["text"])

#     # === THIS IS YOUR ORIGINAL REFINE PROMPT, RESTORED ===
#     refine_prompt_template = f"""
#     You are a Senior Investment Analyst at a top-tier hedge fund, tasked with refining an investment memo for {company_name}.

#     You have the existing draft and a new piece of research context. Your goal is to **integrate** the new information to deepen the analysis, strengthen the arguments, and fill in missing sections. Do not just append the new text. Synthesize it into the existing structure.

#     - **Critically evaluate:** Does the new context support or challenge the existing draft?
#     - **Strengthen the thesis:** Use the new information to make the investment rationale more robust.
#     - **Maintain structure:** The final output must be the complete, updated memo, not just the changes.

#     Based *only* on the provided context, produce the new, refined, and more complete investment memo.

#     --- EXISTING DRAFT ---
#     {{existing_answer}}
#     --- END OF EXISTING DRAFT ---

#     --- NEW CONTEXT TO INTEGRATE ---
#     {{text}}
#     --- END OF NEW CONTEXT ---
    
#     Now, produce the new, refined, and more complete investment memo.
#     """
#     refine_prompt = PromptTemplate(template=refine_prompt_template, input_variables=["existing_answer", "text"])
    
#     print("✅ Prompts are defined and ready.")

#     # --- 4. CREATE AND RUN THE 'REFINE' CHAIN ---
#     print("\n🚀 Executing 'refine' chain with Groq...")
#     chain = load_summarize_chain(
#         llm=llm,
#         chain_type="refine",
#         question_prompt=initial_prompt,
#         refine_prompt=refine_prompt,
#         return_intermediate_steps=False,
#         # Set verbose=True to see chain activity in the terminal
#         verbose=True 
        
#     )
    
#     result = chain.invoke({"input_documents": split_docs})

#     print("=" * 60)
#     print("✅ Investment Memo synthesis complete!")

#     # The function now returns the final memo text directly
#     return result['output_text']



# # phase3_memo_generator.py

# import os
# import json
# from dotenv import load_dotenv
# from fpdf import FPDF

# from langchain_groq import ChatGroq
# from langchain.chains.summarize import load_summarize_chain
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate

# class PDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, 'Investment Memo', 0, 1, 'C')
#         self.ln(10)

#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# def create_pdf_from_text(text: str, filename: str, company_name: str):
#     """Creates a PDF document from the memo text."""
#     pdf = PDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 18)
#     pdf.cell(0, 10, f"Investment Memo: {company_name}", 0, 1, 'L')
#     pdf.ln(5)

#     for line in text.split('\n'):
#         if line.startswith('**') and line.endswith('**'):
#             # Main Section Title (e.g., **1. Executive Summary & Recommendation:**)
#             pdf.set_font('Arial', 'B', 14)
#             pdf.multi_cell(0, 8, line.strip('* '), 0, 'L')
#             pdf.ln(2)
#         elif line.startswith('*'):
#             # Body text or bullet point
#             pdf.set_font('Arial', '', 11)
#             pdf.multi_cell(0, 6, "  • " + line.strip('* '), 0, 'L')
#         else:
#             # Regular paragraph
#             pdf.set_font('Arial', '', 11)
#             pdf.multi_cell(0, 6, line, 0, 'L')
        
#     pdf.output(filename)
#     print(f"📄 PDF memo created at: {filename}")




# # (The PDF class and create_pdf_from_text function are above this and are correct)

# def run_phase_3(company_name: str, market_report_path: str, financial_data_path: str, output_dir: str) -> str:
#     """
#     Creates the final investment memo and saves it as a PDF.
#     This version now checks for a cached PDF before running.
#     """
#     print("--- Starting Phase 3: Memo Synthesis ---")
    
#     # --- START OF NEW CACHING LOGIC ---
#     safe_company_name = company_name.lower().replace(' ', '_')
#     pdf_output_path = os.path.join(output_dir, f"investment_memo_{safe_company_name}.pdf")

#     if os.path.exists(pdf_output_path):
#         print(f"✅ Found cached Investment Memo PDF: '{pdf_output_path}'.")
#         print("   Bypassing memo synthesis.")
#         return pdf_output_path
    
#     print(f"⚠️ No cached memo found. Proceeding with synthesis...")
#     # --- END OF NEW CACHING LOGIC ---

#     load_dotenv()
#     llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-70b-8192", temperature=0.1)
    
#     with open(market_report_path, 'r', encoding='utf-8') as f: market_data = json.load(f)
#     with open(financial_data_path, 'r', encoding='utf-8') as f: financial_data = json.load(f)

#     full_text_content = f"# Comprehensive Research for {company_name}\n\n## Market Research\n{json.dumps(market_data, indent=2)}\n\n## Financial Analysis\n{json.dumps(financial_data, indent=2)}"
#     docs = [Document(page_content=full_text_content)]
#     split_docs = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=500).split_documents(docs)

#     initial_prompt_template = """You are a Senior Investment Analyst. Draft an investment memo for {company_name} based on the context below. Use the specified structure. If info is missing, state "Analysis requires more data."
# **Investment Memo: {company_name}**
# **1. Executive Summary & Recommendation:**
# **2. Company Overview:**
# **3. Market & Industry Analysis:**
# **4. Competitive Landscape & Moat:**
# **5. Financial Analysis & Valuation:**
# **6. Key Risks & Mitigants:**
# **7. Catalysts & Recent Developments:**
# --- CONTEXT ---
# {text}"""
#     initial_prompt = PromptTemplate(
#         template=initial_prompt_template,
#         input_variables=["company_name", "text"]
#     )
    
#     refine_prompt_template = """You are refining an investment memo for {company_name}. Integrate the new context into the existing draft. The output must be the complete, updated memo.
# --- EXISTING DRAFT ---
# {existing_answer}
# --- NEW CONTEXT ---
# {text}"""
#     refine_prompt = PromptTemplate(
#         template=refine_prompt_template,
#         input_variables=["company_name", "existing_answer", "text"]
#     )
    
#     print("🧠 Synthesizing memo with 'refine' chain...")
#     chain = load_summarize_chain(
#         llm=llm,
#         chain_type="refine",
#         question_prompt=initial_prompt,
#         refine_prompt=refine_prompt,
#         verbose=True
#     )
    
#     result = chain.invoke({
#         "input_documents": split_docs,
#         "company_name": company_name
#     })
    
#     final_memo_text = result['output_text']

#     # The PDF path is already defined at the top of the function
#     create_pdf_from_text(final_memo_text, pdf_output_path, company_name)
    
#     print("✅ Phase 3 Complete. Final memo generated as PDF.")
#     return pdf_output_path



# memo_generator.py




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