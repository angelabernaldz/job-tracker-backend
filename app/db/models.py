from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    job_applications = relationship(
        "JobApplication",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class JobApplication(Base):

    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, default="applied", nullable=False)
    job_type = Column(String, nullable=False)
    location = Column(String, nullable=False)

    applied_date = Column(Date, nullable=True)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)

    job_posting_url = Column(String, nullable=True)
    company_website = Column(String, nullable=True)

    job_description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    interviews = relationship("Interview", back_populates="job", cascade="all, delete-orphan")


class Interview(Base):

    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_applications.id", ondelete="CASCADE"))
    stages = relationship("InterviewStage", back_populates="interview", cascade="all, delete-orphan")
    
    job = relationship("JobApplication", back_populates="interview")


class InterviewStage(Base):

    __tablename__ = "interview_stages"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"))
    stage_name = Column(String, nullable=False)
    stage_date = Column(Date, nullable=True)
    stage_notes = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    interview = relationship("Interview", back_populates="stages")
