# 🤖 AI-Powered Investment Memo Generator
<img width="1416" alt="image" src="https://github.com/user-attachments/assets/6982f30d-9db0-4a94-9b10-75569f995cf1" />



This is a comprehensive Streamlit application that automates the generation of a detailed investment memo for a publicly traded company. It orchestrates a multi-phase process involving document analysis, web research, and AI-powered synthesis to produce a structured report.

The application is designed to be efficient, with built-in caching for all major steps. All generated artifacts (document indexes, research data, and final memos) are saved in a persistent, company-specific folder for future reference.

## 🚀 Features

-   **Multi-Phase Analysis:**
    1.  **Financial Document Analysis (Phase 1):** Ingests a company's financial report (e.g., a 10-K) in PDF format. It uses a RAG (Retrieval-Augmented Generation) pipeline with a FAISS vector store to extract and summarize key sections like MD&A, Risk Factors, and more.
    2.  **Market Research (Phase 2):** Performs automated web searches using the Serper API to gather up-to-date information on the company's competitive landscape, market trends, and recent news.
    3.  **Memo Synthesis (Phase 3):** Combines the structured data from the first two phases and uses a powerful Large Language Model (via Groq) to draft a coherent, professional investment memo.
-   **Interactive Web UI:** Built with Streamlit for a clean, user-friendly interface.
-   **Intelligent Caching:** All generated outputs—document indexes, research JSON, and the final memo—are cached. Subsequent runs for the same company are nearly instantaneous.
-   **Organized Output:** All artifacts are saved in a structured folder system: `company_reports/[company_name]/`.
-   **Granular Progress Tracking:** The UI provides real-time feedback with spinners for each specific task, while detailed logs are printed to the console.

## ⚙️ Tech Stack

-   **Backend:** Python
-   **UI Framework:** Streamlit
-   **AI Orchestration:** LangChain
-   **Large Language Models (LLM):** Llama 3 via Groq API
-   **Embedding Model:** `BAAI/bge-small-en-v1.5` via Hugging Face
-   **Vector Store:** FAISS (Facebook AI Similarity Search)
-   **Web Search:** Google Serper API
-   **Document Loading:** PyPDF

---

## 🛠️ Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.9 or higher
-   `pip` (Python package installer)

### 2. Clone the Repository (or Download the Files)

If you are using Git, clone the repository. Otherwise, ensure all project files are in a single directory.

```bash
git clone https://github.com/lokesh-repaka/AI-Powered_Investment_Memo_Generator.git
cd AI-Powered_Investment_Memo_Generator
```

### 3. Create a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

All required Python packages are listed in the `requirements.txt` file. Install them with a single command:

```bash
pip install -r requirements.txt
```

### 5. Set Up API Keys

The application requires API keys for Groq (for the LLM) and Serper (for web search).

1.  Create a file named `.env` in the root of your project directory.
2.  Add your API keys to this file in the following format:

    ```env
    GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    SERPER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

3.  Obtain your keys here:
    -   **Groq:** [Groq Console](https://console.groq.com/keys)
    -   **Serper:** [Serper.dev](https://serper.dev/)

---

## ▶️ How to Run the Application

With the setup complete, running the application is simple.

1.  Make sure your virtual environment is activated.
2.  Open your terminal in the project's root directory.
3.  Run the following Streamlit command:

    ```bash
    streamlit run app.py
    ```

4.  Your default web browser will open with the application running, typically at `http://localhost:8501`.

## 📖 How to Use the App

1.  **Enter Company Name:** In the sidebar, type the full name of the company you want to analyze (e.g., "NVIDIA Corporation").
2.  **Upload Document:** Click "Browse files" and upload the company's latest annual report or financial statement in PDF format.
3.  **Generate Memo:** Click the "Generate Investment Memo" button.
4.  **Monitor Progress:**
    -   The main screen will show spinners for each specific analysis step.
    -   Your terminal will display detailed, real-time logs of the backend processes.
5.  **Download:** Once all phases are complete, a download button will appear, allowing you to save the final investment memo as a Markdown (`.md`) file.

## 📂 Project Structure

```
.
├── company_reports/      # Auto-generated: Stores all outputs
│   └── tesla/
│       ├── doc_cache_...     # Cached FAISS index and chunks
│       ├── financial_analysis_output.json
│       ├── investment_memo_tesla.md
│       └── market_research_tesla.json
│
├── .env                  # Your secret API keys (MUST BE KEPT PRIVATE)
├── .venv/                # Your Python virtual environment
├── app.py                # The main Streamlit application file
├── phase1_analyzer.py    # Logic for financial document analysis
├── phase2_market_research.py # Logic for web-based market research
├── phase3_memo_generator.py # Logic for generating the final memo
├── README.md             # This file
└── requirements.txt      # List of Python packages to install
```
