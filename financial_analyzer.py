import os
import faiss
import json
import re
import numpy as np
from pypdf import PdfReader
import hashlib
import pickle
import tempfile
from typing import Dict

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Models are loaded once when the module is imported
print("Initializing models for Phase 1...")
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant", temperature=0)
embeddings_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
print("Phase 1 models loaded.")

class RAGFusionPipeline:
    def __init__(self, output_dir: str):
        self._chunks = []
        self._index = None
        self._generation_model = llm
        self._embeddings_model_instance = embeddings_model
        self.output_dir = output_dir

    def load_or_create_index(self, file_content: bytes):
        file_hash = hashlib.sha256(file_content).hexdigest()
        index_path = os.path.join(self.output_dir, f"doc_cache_{file_hash}.faiss")
        chunks_path = os.path.join(self.output_dir, f"doc_cache_{file_hash}.pkl")

        if os.path.exists(index_path) and os.path.exists(chunks_path):
            print(f"✅ Loading cached index from: {self.output_dir}")
            self._index = faiss.read_index(index_path)
            with open(chunks_path, "rb") as f:
                self._chunks = pickle.load(f)
            return

        print("⚠️ No index cache found. Building new index from scratch...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_content)
            temp_pdf_path = tmp.name
        
        try:
            content = self._load_file(temp_pdf_path)
            self._chunks = self._chunk_text(content)
            if not self._chunks: raise ValueError("No content could be chunked.")
            self._embed_and_index_chunks()
            
            print(f"💾 Saving new index to cache in: {self.output_dir}")
            faiss.write_index(self._index, index_path)
            with open(chunks_path, "wb") as f:
                pickle.dump(self._chunks, f)
        finally:
            os.unlink(temp_pdf_path)

    def _load_file(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        return "".join(page.extract_text() or "" for page in reader.pages)

    def _chunk_text(self, text: str, chunk_size=1000, chunk_overlap=150) -> list:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - chunk_overlap
        return chunks

    def _embed_and_index_chunks(self):
        print(f"✨ Embedding {len(self._chunks)} chunks...")
        batch_size = 32
        all_embeddings = [
            self._embeddings_model_instance.embed_documents(self._chunks[i:i+batch_size])
            for i in range(0, len(self._chunks), batch_size)
        ]
        embeddings_np = np.array([item for sublist in all_embeddings for item in sublist], dtype='float32')
        self._index = faiss.IndexFlatL2(embeddings_np.shape[1])
        self._index.add(embeddings_np)
        print("✅ RAG index is ready.")

    def query(self, question: str) -> str:
        # This function now only performs a single query. The loop is gone.
        prompt = f"Generate 3 alternative search queries for the question: \"{question}\""
        response = self._generation_model.invoke(prompt)
        generated_queries = [re.sub(r'^\s*[\d\.\-]\s*', '', q).strip() for q in response.content.strip().split('\n') if q.strip()]
        
        all_queries = [question] + generated_queries
        all_retrieved_chunks = []
        for q in all_queries:
            query_embedding = self._embeddings_model_instance.embed_query(q)
            _, indices = self._index.search(np.array([query_embedding], dtype='float32'), 5)
            all_retrieved_chunks.append([self._chunks[i] for i in indices[0]])

        fused_scores = {}
        for doc_list in all_retrieved_chunks:
            for rank, doc in enumerate(doc_list):
                if doc not in fused_scores: fused_scores[doc] = 0
                fused_scores[doc] += 1 / (rank + 60)
        reranked_chunks = sorted(fused_scores.keys(), key=fused_scores.get, reverse=True)
        
        top_k_context = "\n\n---\n\n".join(reranked_chunks[:5])
        final_prompt = f"You are a skilled financial analyst AI. Based on the context below, answer the question.\nContext:\n---\n{top_k_context}\n---\nQuestion: {question}\nAnswer:"
        return self._generation_model.invoke(final_prompt).content


def setup_rag_pipeline(uploaded_file, output_dir: str) -> RAGFusionPipeline:
    """
    Sets up the RAG pipeline by creating or loading the index.
    Returns the ready-to-use RAG engine.
    """
    print("--- Setting up RAG Pipeline for Phase 1 ---")
    rag_engine = RAGFusionPipeline(output_dir=output_dir)
    rag_engine.load_or_create_index(file_content=uploaded_file.getvalue())
    return rag_engine