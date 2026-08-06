import openai
import anthropic
from typing import List, Optional
from app.core.config import settings


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBED_MODEL

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]


class ChatService:
    """Service for chat completion using OpenAI or Anthropic."""

    def __init__(self):
        self.provider = settings.AI_PROVIDER
        
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_CHAT_MODEL
        elif self.provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key is required when using Anthropic provider")
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = settings.ANTHROPIC_CHAT_MODEL
        else:
            raise ValueError(f"Invalid AI provider: {self.provider}")

    def chat(self, messages: List[dict], temperature: float = 0.1) -> str:
        """Send chat messages and get response."""
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        elif self.provider == "anthropic":
            # Convert OpenAI format to Anthropic format
            system_message = ""
            anthropic_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    anthropic_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system_message,
                messages=anthropic_messages,
                temperature=temperature
            )
            return response.content[0].text
