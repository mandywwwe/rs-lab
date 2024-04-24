from pydantic import BaseModel
from jinja2 import Template

from .message import Message

class Round(BaseModel):
    name: str
    messages: list[Message] = []

class Config(BaseModel):
    version: str
    rounds: list[Round] = []
    metadata: dict | None = None
    
    def initial_messages(self, round_index:int, metadata:dict={}) -> list[Message]:
        result:list[Message] = []
        for message in self.rounds[round_index].messages:
            template = Template(message.content)
            content = template.render(metadata)
            result.append(Message(role=message.role, content=content))
        return result