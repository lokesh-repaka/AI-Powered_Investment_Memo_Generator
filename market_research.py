

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MarketResearchAgent:
    """An agent dedicated to performing market research tasks."""
    def __init__(self):
        """Initializes the agent by loading API keys and setting up models."""
        print("--- Initializing Market Research Agent ---")
        load_dotenv()
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
        self.search_tool = GoogleSerperAPIWrapper()
        print("✅ Market Research Agent is ready.")

    def research_topic(self, main_topic: str, sub_topics: list) -> dict:
        """
        Researches a single main topic by iterating through its sub-topics (search queries).

        Args:
            main_topic (str): The high-level topic being researched (e.g., "Competitive Landscape").
            sub_topics (list): A list of specific search queries for that topic.

        Returns:
            dict: A dictionary containing the synthesized analysis for each sub-topic.
        """
        print(f"--- Processing Section: {main_topic} ---")
        topic_results = {}
        for sub_topic_query in sub_topics:
            print(f"   - Researching: {sub_topic_query}")
            
            try:
                search_result = self.search_tool.run(sub_topic_query)
            except Exception as e:
                print(f"      - FAILED to search. Error: {e}")
                search_result = f"Error during search: {e}"

            synthesis_prompt = ChatPromptTemplate.from_template(
                "You are a market analyst. Synthesize a concise analysis for '{topic}' "
                "based *only* on the raw data below.\n\n--- RAW DATA ---\n{data}"
            )
            synthesis_chain = synthesis_prompt | self.llm | StrOutputParser()
            synthesized_analysis = synthesis_chain.invoke({"topic": sub_topic_query, "data": search_result})
            
            # Use the query as the key for the result
            topic_results[sub_topic_query] = synthesized_analysis

        return topic_results