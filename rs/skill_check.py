import random
from typing import Literal
from d20 import roll

def sanity_check(metadata:dict) -> str:
    character = metadata["character"]
    sanity = character['sanity']

    if "sanity_lost" not in character:
        character["sanity_lost"] = 0
    
    if 'tags' not in character:
            character['tags'] = []
    
    roll_num = roll("1d100").total

    content = f"I am making a SANITY check against my own sanity points: {sanity - character["sanity_lost"]}."

    if roll_num <=  sanity:
        return content + f"\nAnd... SUCCESS! I rolled {roll_num} against my sanity: {sanity}."
    
    lost = roll("1d6").total
    
    character["sanity_lost"] += lost

    if character["sanity"] - character["sanity_lost"] <= character["sanity"] // 2:
        if "insane" not in character['tags']:
            character['tags'].append("insane")

    content += f"\nAnd... FAILED! I lost {lost} sanity points."
    
    if lost >= 5:
        content += f"\nI am shocked and lose control of my actions."

    return content

def skill_check(skill:str, dc:Literal["easy", "normal", "hard"]|None, metadata: dict|None) -> str:
    if skill == "sanity":
        return sanity_check(metadata)
    
    content = f"I am making a skill check using {skill.upper()} against a difficulty of {dc.upper()}."

    d = dc.lower()
    dc = 50
    if d == "easy":
        dc = 75
    elif d == "hard":
        dc = 25
    rolled = roll("1d100").total
    result = "Success" if rolled <= dc else "Failure"
    if rolled < 5:
        result = "Critical Success"
    elif rolled > 95:
        result = "Critical Failure"

    content += f"\nAnd I rolled a {rolled} for a result of {result.upper()}."
    return content