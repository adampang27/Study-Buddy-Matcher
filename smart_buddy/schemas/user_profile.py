from pydantic import BaseModel
from typing import List

class UserProfileCreate(BaseModel):
    name: str
    email: str
    personality_type: str
    study_style: str
    environment: str
    focus_area: str

class ProfileCreate(BaseModel):
    username: str
    email: str
    password: str
    study_style: str
    environment: str
    personality: str
    focus_areas: List[str]
    availability: dict
