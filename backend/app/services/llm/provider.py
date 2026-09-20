"""
MoneyFollows - LLM Provider Abstraction
Supports OpenAI, OpenRouter, and Google AI.
"""

import json
import httpx
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type
from pydantic import BaseModel

from app.config import settings

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> str:
        pass

    async def generate_json(
        self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.0
    ) -> Dict[str, Any]:
        """Generate and parse JSON response."""
        response = await self.generate(prompt, system_prompt, temperature)
        # Clean response - remove markdown code fences if present
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}. Response: {cleaned[:200]}")
            # Retry with correction prompt
            retry_prompt = f"""The following text should be valid JSON but has errors. 
Fix it and return ONLY valid JSON, no explanations:

{cleaned[:2000]}"""
            retry_response = await self.generate(retry_prompt, temperature=0.0)
            retry_cleaned = retry_response.strip()
            if retry_cleaned.startswith("```json"):
                retry_cleaned = retry_cleaned[7:]
            elif retry_cleaned.startswith("```"):
                retry_cleaned = retry_cleaned[3:]
            if retry_cleaned.endswith("```"):
                retry_cleaned = retry_cleaned[:-3]
            return json.loads(retry_cleaned.strip())


class OpenAICompatibleProvider(BaseLLMProvider):
    """Provider for OpenAI-compatible APIs (OpenAI, OpenRouter)."""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                
                # OpenRouter specific headers
                if "openrouter" in self.base_url:
                    headers["HTTP-Referer"] = settings.frontend_url
                    headers["X-Title"] = "MoneyFollows"

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 4000,
                }

                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"LLM API error: {e.response.status_code} - {e.response.text[:200]}")
            raise
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise


class GoogleAIProvider(BaseLLMProvider):
    """Provider for Google AI (Gemini) API."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> str:
        try:
            async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
                parts = []
                if system_prompt:
                    parts.append({"text": f"{system_prompt}\n\n{prompt}"})
                else:
                    parts.append({"text": prompt})

                payload = {
                    "contents": [{"parts": parts}],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": 4000,
                    },
                }

                resp = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            logger.error(f"Google AI generation failed: {e}")
            raise


def get_llm_provider() -> BaseLLMProvider:
    """Factory function to get the configured LLM provider."""
    provider = settings.llm_provider.lower()
    
    if provider == "openai":
        api_key = settings.openai_api_key
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        return OpenAICompatibleProvider(
            api_key=api_key,
            base_url="https://api.openai.com/v1",
            model=settings.llm_model,
        )
    elif provider == "openrouter":
        api_key = settings.openrouter_api_key
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not configured")
        return OpenAICompatibleProvider(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=settings.llm_model,
        )
    elif provider == "google":
        api_key = settings.google_api_key
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not configured")
        return GoogleAIProvider(
            api_key=api_key,
            model=settings.llm_model,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Supported: openai, openrouter, google")
