from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from smart_buddy.db import Base  # or from sqlalchemy.ext.declarative import declarative_base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {'extend_existing': True}  # ✅ Add this line

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    major = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    personality_traits = Column(String, nullable=True)  # e.g. "Introvert,Ambivert"
    study_style = Column(String, nullable=True)         # e.g. "Group"
    preferred_environment = Column(String, nullable=True)  # e.g. "Quiet"
    study_subjects = Column(String, nullable=True)
    # The Availability model's 'user' relationship expects 'availability' on this class
    availability_rel = relationship("Availability", back_populates="user")
    availability = Column(String, nullable=True)
    goals = Column(String, nullable=True)
