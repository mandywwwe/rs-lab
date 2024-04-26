import random
from typing import Literal
from d20 import roll

def sanity_check(metadata:dict) -> str:
    character = metadata["character"]
    sanity = character['sanity']
    
    roll_num = roll("1d100").total

    content = f"I am making a SANITY check against my own sanity:{sanity}."

    if roll_num <=  sanity:
        return content + f"\nAnd... SUCCESS! I rolled {roll_num} against my sanity: {sanity}."
    
    lost = roll("1d6").total
    character["sanity"] -= lost

    if "symptom" in metadata:
        l = len(metadata["symptom"])
        symptom =random.randrange(0, l)
        symptom_str = metadata["symptom"][symptom]
        
        if "symptoms" not in character:
            character["symptoms"] = []

        if symptom_str not in character["symptoms"]:
            character['symptoms'].append(symptom_str)

    content += f"\nAnd... FAILED! I lost {lost} sanity points, and gained a symptom: {symptom_str}."
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