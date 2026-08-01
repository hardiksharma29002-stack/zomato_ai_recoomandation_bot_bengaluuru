import json
import os
import re
from typing import Optional, Dict, Any
from groq import Groq
from openai import OpenAI
from src.config import settings

def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

class LLMClient:
    def __init__(self):
        self.provider = settings.llm_provider
        self.groq_client = None
        self.openai_client = None
        
        if self.provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
            self.groq_client = Groq(api_key=settings.groq_api_key)
        elif self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "ollama":
            # Ollama provides an OpenAI-compatible API
            self.openai_client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama" # required but ignored by ollama
            )
        else:
            raise NotImplementedError(f"Provider {self.provider} not fully implemented yet.")

    def generate_json(self, prompt: str, model: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Generate JSON response from LLM given a prompt.
        """
        if self.provider == "groq":
            if not model:
                model = "llama-3.1-8b-instant"
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=model,
                    response_format={"type": "json_object"},
                )
                response_content = chat_completion.choices[0].message.content
                return json.loads(_clean_json(response_content))
            except Exception as e:
                print(f"Error during LLM generation (Groq): {e}")
                return None
                
        elif self.provider == "openai":
            if not model:
                model = "gpt-3.5-turbo-1106" # model supporting json mode
            try:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"Error during LLM generation (OpenAI): {e}")
                return None
                
        elif self.provider == "ollama":
            if not model:
                model = "llama3" # default local model
            try:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"Error during LLM generation (Ollama): {e}")
                return None
                
        return None
