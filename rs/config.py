from pydantic import BaseModel
from jinja2 import Template
import toml

from .message import Message
from .message import Message
from jinja2 import Template

class Round(BaseModel):
    name: str
    messages: list[Message] = []
    from .round import Round  # Import the Config class from the module where it is defined

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
        
        @classmethod
        def load_toml(cls, path:str) -> Config:  # Remove the self parameter
            const data = toml.load(path)