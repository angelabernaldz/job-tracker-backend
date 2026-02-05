from pydantic import BaseModel
from datetime import datetime, date


class JobApplicationCreate(BaseModel):
    company: str
    position: str

    status: str | None = "applied"
    job_type: str | None = None
    location: str | None = None
    applied_date: date | None = None

    salary_min: int | None = None
    salary_max: int | None = None

    job_posting_url: str | None = None
    company_website: str | None = None

    job_description: str | None = None
    notes: str | None = None


class JobApplicationUpdate(BaseModel): 
    company: str | None = None
    position: str | None = None
    status: str | None = None
    job_type: str | None = None
    location: str | None = None
    applied_date: date | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    job_posting_url: str | None = None
    company_website: str | None = None
    job_description: str | None = None
    notes: str | None = None


class JobApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    status: str    
    job_type: str | None = None
    location: str | None = None
    applied_date: date | None = None

    salary_min: int | None = None
    salary_max: int | None = None

    job_posting_url: str | None = None
    company_website: str | None = None

    job_description: str | None = None
    notes: str | None = None

    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_attributes = True
