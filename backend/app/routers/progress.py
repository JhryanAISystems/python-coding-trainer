from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProgressResponse
from app.services.progress_service import get_progress

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("", response_model=ProgressResponse)
def read_progress(db: Session = Depends(get_db)):
    return get_progress(db)
