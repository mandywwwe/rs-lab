import os
from typing import Union
from openai import OpenAI

from openai import AzureOpenAI

from .message import Message

def chat(messages:list[Message], on_message: Union[callable, None] = None) -> Message:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL_NAME"),
        messages=messages,
        stream=True,
        temperature=float(os.environ.get("OPENAI_TEMPERATURE"))
    )

    generated = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            delta = chunk.choices[0].delta.content
            if (on_message is not None):
                on_message(chunk.choices[0].delta.content)
            generated += delta
    return Message(role="assistant", content=generated)

def chat_with_azure(messages:list[Message], on_message: Union[callable, None] = None) -> Message:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2023-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    stream = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL_NAME"),
        messages=messages,
        stream=True,
        temperature=float(os.environ.get("OPENAI_TEMPERATURE")),
        max_tokens=4000
    )

    generated = ""
    for chunk in stream:
        if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
            delta = chunk.choices[0].delta.content
            if (on_message is not None):
                on_message(chunk.choices[0].delta.content)
            generated += delta

    return Message(role="assistant", content=generated)