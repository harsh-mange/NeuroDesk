import re
from typing import Dict, Optional
from app.models.emotion import EmotionResponse, EmotionType

class EmotionDetector:
    def __init__(self):
        # Emotion keywords for rule-based detection
        self.emotion_keywords = {
            EmotionType.joy: [
                'happy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic',
                'love', 'enjoy', 'pleased', 'satisfied', 'grateful', 'blessed'
            ],
            EmotionType.sadness: [
                'sad', 'depressed', 'down', 'blue', 'melancholy', 'grief',
                'lonely', 'hopeless', 'disappointed', 'heartbroken'
            ],
            EmotionType.anger: [
                'angry', 'furious', 'mad', 'irritated', 'frustrated', 'annoyed',
                'rage', 'hate', 'disgusted', 'outraged'
            ],
            EmotionType.fear: [
                'afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous',
                'panic', 'dread', 'fearful', 'intimidated'
            ],
            EmotionType.surprise: [
                'surprised', 'shocked', 'amazed', 'astonished', 'stunned',
                'unexpected', 'sudden', 'unbelievable'
            ],
            EmotionType.overwhelmed: [
                'overwhelmed', 'stressed', 'burdened', 'swamped', 'drowning',
                'too much', 'can\'t handle', 'exhausted', 'burned out'
            ],
            EmotionType.anxious: [
                'anxious', 'worried', 'concerned', 'uneasy', 'restless',
                'tense', 'jittery', 'on edge', 'apprehensive'
            ],
            EmotionType.stressed: [
                'stressed', 'pressure', 'tension', 'strained', 'overworked',
                'under pressure', 'tight deadline', 'crunch time'
            ]
        }
    
    async def detect_emotion(self, text: str) -> Optional[EmotionResponse]:
        """
        Detect emotions in text using rule-based approach.
        In production, this would use a pre-trained model like cardiffnlp/twitter-roberta-base-emotion
        """
        if not text or len(text.strip()) < 3:
            return None
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Count emotion keywords
        emotion_scores = {}
        total_words = len(text_lower.split())
        
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotion_scores[emotion] = count / total_words
        
        if not emotion_scores:
            # Default to neutral if no emotions detected
            return EmotionResponse(
                id="emotion_1",
                timestamp=0,
                primary_emotion=EmotionType.neutral,
                confidence=0.5,
                source="rule_based",
                text_content=text,
                emotion_scores={EmotionType.neutral: 1.0},
                is_overwhelm_detected=False,
                overwhelm_score=0.0
            )
        
        # Find primary emotion (highest score)
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        confidence = emotion_scores[primary_emotion]
        
        # Calculate overwhelm score
        overwhelm_score = self._calculate_overwhelm_score(text_lower, emotion_scores)
        is_overwhelm_detected = overwhelm_score > 0.7
        
        return EmotionResponse(
            id="emotion_1",
            timestamp=0,
            primary_emotion=primary_emotion,
            confidence=confidence,
            source="rule_based",
            text_content=text,
            emotion_scores=emotion_scores,
            is_overwhelm_detected=is_overwhelm_detected,
            overwhelm_score=overwhelm_score
        )
    
    def _calculate_overwhelm_score(self, text: str, emotion_scores: Dict[EmotionType, float]) -> float:
        """
        Calculate overwhelm score based on emotion scores and text patterns.
        """
        # Base score from emotion scores
        overwhelm_emotion_score = emotion_scores.get(EmotionType.overwhelmed, 0.0)
        stress_score = emotion_scores.get(EmotionType.stressed, 0.0)
        anxiety_score = emotion_scores.get(EmotionType.anxious, 0.0)
        
        # Text pattern indicators
        overwhelm_patterns = [
            r'\btoo much\b', r'\bcan\'t handle\b', r'\boverwhelming\b',
            r'\btoo many\b', r'\bexhausted\b', r'\btired\b', r'\bfatigued\b'
        ]
        
        pattern_score = sum(1 for pattern in overwhelm_patterns if re.search(pattern, text))
        pattern_score = min(pattern_score / len(overwhelm_patterns), 1.0)
        
        # Combine scores
        total_score = (
            overwhelm_emotion_score * 0.4 +
            stress_score * 0.3 +
            anxiety_score * 0.2 +
            pattern_score * 0.1
        )
        
        return min(total_score, 1.0) 