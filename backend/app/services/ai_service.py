import time
import re
from typing import List, Optional
from app.models.task import TaskCreate, TaskResponse
from app.models.emotion import EmotionResponse, EmotionType
from app.services.emotion_detector import EmotionDetector

class BrainDumpResult:
    def __init__(self, tasks: List[TaskResponse], emotion_reading: Optional[EmotionResponse], processing_time: float):
        self.tasks = tasks
        self.emotion_reading = emotion_reading
        self.processing_time = processing_time

class AIService:
    def __init__(self):
        self.emotion_detector = EmotionDetector()
    
    async def process_brain_dump(self, text: str) -> BrainDumpResult:
        """
        Process brain dump text and extract tasks and emotions.
        """
        start_time = time.time()
        
        # Extract tasks from text
        tasks = self._extract_tasks(text)
        
        # Detect emotions
        emotion_reading = await self.emotion_detector.detect_emotion(text)
        
        processing_time = time.time() - start_time
        
        return BrainDumpResult(tasks, emotion_reading, processing_time)
    
    def _extract_tasks(self, text: str) -> List[TaskResponse]:
        """
        Extract tasks from brain dump text using simple NLP rules.
        In a real implementation, this would use more sophisticated NLP.
        """
        tasks = []
        
        # Split text into lines
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove common prefixes
            line = re.sub(r'^[-•*]\s*', '', line)
            
            # Skip if line is too short
            if len(line) < 3:
                continue
            
            # Determine energy level based on keywords
            energy = self._determine_energy_level(line)
            
            # Determine category based on keywords
            category = self._determine_category(line)
            
            # Check for avoidance patterns
            is_avoidance = self._detect_avoidance(line)
            
            # Create task
            task = TaskResponse(
                id=f"task_{len(tasks) + 1}",
                title=line,
                description=None,
                energy=energy,
                status="todo",
                category=category,
                created_at=time.time(),
                completed_at=None,
                due_date=None,
                focus_minutes=0,
                tags=[],
                is_avoidance=is_avoidance,
                emotion_score=0.0,
                original_brain_dump=text
            )
            
            tasks.append(task)
        
        return tasks
    
    def _determine_energy_level(self, text: str) -> str:
        """
        Determine energy level based on keywords in the text.
        """
        text_lower = text.lower()
        
        # High energy keywords
        high_energy_words = [
            'urgent', 'important', 'deadline', 'meeting', 'presentation',
            'project', 'report', 'analysis', 'research', 'study'
        ]
        
        # Low energy keywords
        low_energy_words = [
            'maybe', 'sometime', 'eventually', 'later', 'when i have time',
            'if possible', 'optional', 'nice to have', 'relax', 'rest'
        ]
        
        # Count matches
        high_count = sum(1 for word in high_energy_words if word in text_lower)
        low_count = sum(1 for word in low_energy_words if word in text_lower)
        
        if high_count > low_count:
            return "high"
        elif low_count > high_count:
            return "low"
        else:
            return "medium"
    
    def _determine_category(self, text: str) -> str:
        """
        Determine task category based on keywords.
        """
        text_lower = text.lower()
        
        categories = {
            'work': ['work', 'job', 'office', 'meeting', 'project', 'report', 'email'],
            'personal': ['personal', 'family', 'home', 'house', 'clean'],
            'health': ['exercise', 'workout', 'gym', 'health', 'doctor', 'medical'],
            'learning': ['learn', 'study', 'course', 'book', 'read', 'practice'],
            'social': ['friend', 'family', 'call', 'visit', 'party', 'social']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return "other"
    
    def _detect_avoidance(self, text: str) -> bool:
        """
        Detect avoidance patterns in the text.
        """
        text_lower = text.lower()
        
        avoidance_patterns = [
            'avoid', 'procrastinate', 'put off', 'delay', 'postpone',
            'maybe later', 'not sure', 'uncertain', 'hesitate'
        ]
        
        return any(pattern in text_lower for pattern in avoidance_patterns) 