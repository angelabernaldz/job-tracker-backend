from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.job_application import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate
from db.models import JobApplication, User
from db.session import get_db
from core.dependencies import get_current_user

router = APIRouter(prefix="/jobs")

@router.post("/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job: JobApplicationCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_job = JobApplication(
        **job.dict(),
        user_id=current_user.id
    )
    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Database error: {str(e.orig)}"
        )
    
    return db_job       

    
@router.get("/", response_model=List[JobApplicationResponse])
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    jobs = (
        db.query(JobApplication)
        .filter(JobApplication.user_id == current_user.id)
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    return jobs


@router.get("/{job_id}", response_model=JobApplicationResponse)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    job = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == job_id,
            JobApplication.user_id == current_user.id
        )
        .first()
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found"
        )

    return job


@router.patch("/{job_id}", response_model=JobApplicationResponse)
def update_job(
    job_id: int,
    job_update: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    job = (
        db.query(JobApplication)
        .filter(JobApplication.id == job_id,
                JobApplication.user_id == current_user.id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found"
        )
    
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = (
        db.query(JobApplication)
        .filter(JobApplication.id == job_id,
                JobApplication.user_id == current_user.id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found"
        )
    
    db.delete(job)
    db.commit()

    return 