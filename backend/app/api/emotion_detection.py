from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.emotion_detector import EmotionDetector
from app.models.emotion import EmotionResponse

router = APIRouter()

class EmotionDetectionRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

@router.post("/detect-emotion", response_model=EmotionResponse)
async def detect_emotion(request: EmotionDetectionRequest):
    """
    Detect emotions in text and determine if overwhelm is present.
    """
    try:
        emotion_detector = EmotionDetector()
        emotion_reading = await emotion_detector.detect_emotion(request.text)
        
        if emotion_reading is None:
            raise HTTPException(
                status_code=400,
                detail="Could not detect emotions in the provided text"
            )
        
        return emotion_reading
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting emotions: {str(e)}"
        ) 