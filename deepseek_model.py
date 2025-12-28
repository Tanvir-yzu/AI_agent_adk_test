import os
from typing import Any, Dict, List, Optional
from google.adk.models import LanguageModel, Message
from openai import OpenAI


class DeepSeekModel(LanguageModel):
    """
    Thin wrapper that makes DeepSeek look like an ADK LanguageModel.
    """
    def __init__(
        self,
        model_id: str = "deepseek-chat",
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com/v1",
        **kwargs: Any,
    ):
        super().__init__(model_id=model_id, **kwargs)
        self.client = OpenAI(
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url=base_url,
        )

    def generate(
        self,
        messages: List[Message],
        *,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        # convert ADK Message list to OpenAI format
        openai_msgs = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=openai_msgs,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return response.choices[0].message.content or ""