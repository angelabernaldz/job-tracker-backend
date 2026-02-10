from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.session import get_db
from schemas.interview import InterviewResponse, InterviewCreate
from schemas.interview import InterviewStageCreate, InterviewStageUpdate, InterviewStageResponse
from db.models import Interview, InterviewStage

router = APIRouter(prefix="/interviews")

# ----- Interview ----- #
@router.post("/", response_model=InterviewResponse)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):

    db_interview = Interview(**interview.dict())
    try:
        db.add(db_interview)
        db.commit()
        db.refresh(db_interview)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Database error: {str(e.orig)}"
        )
    
    return db_interview


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: int, db: Session = Depends(get_db)):

    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(interview_id: int, db: Session = Depends(get_db)):

    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    db.delete(interview)
    db.commit()

    return 


# ----- InterviewStage ----- #
@router.post("/stages", response_model=InterviewStageResponse)
def create_stage(stage: InterviewStageCreate, db: Session = Depends(get_db)):
    db_stage = InterviewStage(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


@router.patch("/stages/{stage_id}", response_model=InterviewStageResponse)
def update_stage(stage_id: int, stage_update: InterviewStageUpdate, db: Session = Depends(get_db)):
    stage = db.query(InterviewStage).filter(InterviewStage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stage not found"
    )

    for key, value in stage_update.dict(exclude_unset=True).items():
        setattr(stage, key, value)

    db.commit()
    db.refresh(stage)
    return stage


@router.delete("/stages/{stage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = db.query(InterviewStage).filter(InterviewStage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Stage not found"
        )
    
    db.delete(stage)
    db.commit()
    return