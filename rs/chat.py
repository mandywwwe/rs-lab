import os
from typing import Union
from openai import OpenAI

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