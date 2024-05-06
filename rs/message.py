import re
from typing import Literal
from pydantic import BaseModel

message_pattern = re.compile(r"^(.+)\:[ \s]*(.+)*$")

class Message(BaseModel):
    role: Literal["system", "assistant", "user"]
    content: str   

    def dict(self) -> dict:
        current_key = None
        parsed = {}
        lines = self.content.splitlines()
        # parse the content line by line
        for line in lines:
            res = message_pattern.search(line)
            if res is not None:
                current_key = res.group(1)
                if res.group(2) is not None:
                    parsed[current_key] = res.group(2)
                else:
                    parsed[current_key] = ""
            elif current_key is not None:
                parsed[current_key] += "\n" + line
        return parsed