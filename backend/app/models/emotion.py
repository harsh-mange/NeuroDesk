from pydantic import BaseModel
from typing import Dict, Optional
from enum import Enum

class EmotionType(str, Enum):
    joy = "joy"
    sadness = "sadness"
    anger = "anger"
    fear = "fear"
    surprise = "surprise"
    disgust = "disgust"
    neutral = "neutral"
    overwhelmed = "overwhelmed"
    anxious = "anxious"
    stressed = "stressed"

class EmotionResponse(BaseModel):
    id: str
    timestamp: float
    primary_emotion: EmotionType
    confidence: float
    source: str
    text_content: Optional[str] = None
    emotion_scores: Dict[EmotionType, float] = {}
    is_overwhelm_detected: bool = False
    overwhelm_score: float = 0.0

    class Config:
        from_attributes = True 