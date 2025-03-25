import json
import os
import xml.etree.ElementTree as ET
import re
from autogen import AssistantAgent
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama

# Load environment variables
load_dotenv()

def convert_numeric_words(value):
    """Convert common numeric words into digits where applicable."""
    num_dict = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "thousand": "000"
    }
    return " ".join([num_dict.get(word, word) for word in value.lower().split()])

class AdvancedComparisonAgent:
    def __init__(self):
        """Initialize the agent with either Groq or Ollama based on availability."""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.use_groq = bool(self.groq_api_key)
        
        if self.use_groq:
            print("Using Grok LLM...")
            self.llm_config = {
                'config_list': [{'model': os.getenv("GROK_MODEL", "llama-3.3-70b-versatile"), 'api_key': self.groq_api_key, 'api_type': "groq"}]
            }
        else:
            print("Using Ollama (local model)...")
            self.ollama_model = Ollama(
                model=os.getenv("OLLAMA_MODEL", "tinyllama:latest"),
                base_url=f"http://{os.getenv('OLLAMA_IP', 'localhost')}:11434"
            )

        self.matching_agent = AssistantAgent(
            name="matching_agent",
            system_message=(
                "Compare fields from two different forms (JSON, XML, or HTML). "
                "Identify if fields match or have equivalent meanings based on synonyms or relative terms. "
                "Return a structured response highlighting matches and mismatches."
            ),
            llm_config=self.llm_config if self.use_groq else None,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    @staticmethod
    def normalize_text(text):
        """Normalize text by converting to lowercase and removing special characters."""
        return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower()).strip()

    def extract_fields_from_json(self, json_data):
        """Extract key-value pairs from a JSON form."""
        return {self.normalize_text(k): self.normalize_text(str(v)) for k, v in json_data.items()}

    def extract_fields_from_text(self, text_data):
        """Extract key-value pairs from structured text data."""
        extracted = {}
        for line in text_data.strip().split("\n"):
            match = re.match(r"^(.*?):\s*(.*)$", line.strip())
            if match:
                key, value = match.groups()
                extracted[key.strip()] = convert_numeric_words(value.strip())
        return extracted

    def extract_fields_from_xml(self, xml_data):
        """Extract key-value pairs from an XML form."""
        extracted = {}
        try:
            root = ET.fromstring(xml_data)
            for elem in root.iter():
                if elem.text and elem.tag:
                    extracted[self.normalize_text(elem.tag)] = self.normalize_text(elem.text)
        except ET.ParseError:
            print("Error: Invalid XML format")
        return extracted

    def compare_fields(self, form1, form2):
        """Use either Groq or Ollama to compare two forms."""
        prompt = (
            "Compare the following two forms and determine if their fields match based on synonyms, "
            "relative meaning, or common variations. Identify mismatches and suggest corrections.\n\n"
            
            #Added on 25 March 2025- Remove if does not work
            "For Base Amount, amut is excluding 13% HST. For Monthly recurring price, the value is including 13% HST. Calculate and check\n"
            
            "Form 1: {form1}\n"
            "Form 2: {form2}\n\n"
            "Return the output in a structured table format with the following columns:\n"
            "- Field Name\n"
            "- Match Status (Correct / Incorrect)\n"
            "- Suggested Correction / Reason\n"
            "Provide a clear and concise response."
        ).format(form1=form1, form2=form2)
        
        print("Generated Prompt:\n", prompt)
        
        if self.use_groq:
            response = self.matching_agent.generate_reply(messages=[{"role": "user", "content": prompt}])
            return response.get("content", "Comparison failed!") if isinstance(response, dict) else str(response)
        else:
            return self.ollama_model.complete(prompt).text.strip()
