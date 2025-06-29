from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.ai_service import AIService
from app.models.task import TaskCreate, TaskResponse
from app.models.emotion import EmotionResponse

router = APIRouter()

class BrainDumpRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class BrainDumpResponse(BaseModel):
    tasks: List[TaskResponse]
    emotion_reading: Optional[EmotionResponse] = None
    processing_time: float

@router.post("/brain-dump", response_model=BrainDumpResponse)
async def process_brain_dump(request: BrainDumpRequest):
    """
    Process brain dump text and convert to structured tasks with emotion analysis.
    """
    try:
        ai_service = AIService()
        
        # Process the brain dump
        result = await ai_service.process_brain_dump(request.text)
        
        return BrainDumpResponse(
            tasks=result.tasks,
            emotion_reading=result.emotion_reading,
            processing_time=result.processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing brain dump: {str(e)}"
        )

@router.get("/brain-dump/history")
async def get_brain_dump_history(user_id: str, limit: int = 10):
    """
    Get brain dump history for a user.
    """
    try:
        # TODO: Implement brain dump history retrieval
        return {
            "brain_dumps": [],
            "total_count": 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving brain dump history: {str(e)}"
        ) 