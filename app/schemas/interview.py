from typing import List, Optional
from datetime import date
from pydantic import BaseModel

# ---- Stage ----
class InterviewStageBase(BaseModel):
    stage_name: str
    stage_date: Optional[date] = None
    stage_notes: Optional[str] = None
    completed: Optional[bool] = False


class InterviewStageCreate(InterviewStageBase):
    pass


class InterviewStageUpdate(BaseModel):
    stage_name: Optional[str]
    stage_date: Optional[date]
    stage_notes: Optional[str]
    completed: Optional[bool]


class InterviewStageResponse(InterviewStageBase):
    id: int

    class Config:
        orm_mode = True


# ---- Interview ----
class InterviewBase(BaseModel):
    job_id: int


class InterviewCreate(InterviewBase):
    stages: Optional[List[InterviewStageCreate]] = []


class InterviewResponse(InterviewBase):
    id: int
    stages: List[InterviewStageResponse] = []

    class Config:
        orm_mode = True
