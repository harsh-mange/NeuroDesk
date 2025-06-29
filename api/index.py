from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import re
import time
from datetime import datetime

app = FastAPI(
    title="NeuroDesk API",
    description="AI-Powered Productivity & Mental Wellness API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple emotion detection keywords
EMOTION_KEYWORDS = {
    'joy': ['happy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'love', 'enjoy'],
    'sadness': ['sad', 'depressed', 'down', 'blue', 'melancholy', 'grief', 'lonely'],
    'anger': ['angry', 'furious', 'mad', 'irritated', 'frustrated', 'annoyed', 'rage'],
    'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'nervous', 'panic'],
    'overwhelmed': ['overwhelmed', 'stressed', 'burdened', 'swamped', 'drowning', 'too much'],
    'anxious': ['anxious', 'worried', 'concerned', 'uneasy', 'restless', 'tense'],
    'stressed': ['stressed', 'pressure', 'tension', 'strained', 'overworked']
}

def extract_tasks(text):
    """Extract tasks from brain dump text"""
    tasks = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 3:
            continue
            
        # Remove common prefixes
        line = re.sub(r'^[-•*]\s*', '', line)
        
        # Determine energy level
        energy = determine_energy_level(line)
        
        # Determine category
        category = determine_category(line)
        
        # Check for avoidance
        is_avoidance = detect_avoidance(line)
        
        task = {
            'id': f'task_{len(tasks) + 1}',
            'title': line,
            'description': None,
            'energy': energy,
            'status': 'todo',
            'category': category,
            'created_at': time.time(),
            'completed_at': None,
            'due_date': None,
            'focus_minutes': 0,
            'tags': [],
            'is_avoidance': is_avoidance,
            'emotion_score': 0.0,
            'original_brain_dump': text
        }
        
        tasks.append(task)
    
    return tasks

def determine_energy_level(text):
    """Determine energy level based on keywords"""
    text_lower = text.lower()
    
    high_energy_words = ['urgent', 'important', 'deadline', 'meeting', 'presentation', 'project', 'report']
    low_energy_words = ['maybe', 'sometime', 'eventually', 'later', 'when i have time', 'if possible', 'optional']
    
    high_count = sum(1 for word in high_energy_words if word in text_lower)
    low_count = sum(1 for word in low_energy_words if word in text_lower)
    
    if high_count > low_count:
        return "high"
    elif low_count > high_count:
        return "low"
    else:
        return "medium"

def determine_category(text):
    """Determine task category based on keywords"""
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

def detect_avoidance(text):
    """Detect avoidance patterns"""
    text_lower = text.lower()
    avoidance_patterns = ['avoid', 'procrastinate', 'put off', 'delay', 'postpone', 'maybe later', 'not sure']
    return any(pattern in text_lower for pattern in avoidance_patterns)

def detect_emotion(text):
    """Detect emotions in text"""
    if not text or len(text.strip()) < 3:
        return None
    
    text_lower = text.lower()
    emotion_scores = {}
    total_words = len(text_lower.split())
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        if count > 0:
            emotion_scores[emotion] = count / total_words
    
    if not emotion_scores:
        return {
            'id': 'emotion_1',
            'timestamp': time.time(),
            'primary_emotion': 'neutral',
            'confidence': 0.5,
            'source': 'rule_based',
            'text_content': text,
            'emotion_scores': {'neutral': 1.0},
            'is_overwhelm_detected': False,
            'overwhelm_score': 0.0
        }
    
    # Find primary emotion
    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
    confidence = emotion_scores[primary_emotion]
    
    # Calculate overwhelm score
    overwhelm_score = calculate_overwhelm_score(text_lower, emotion_scores)
    is_overwhelm_detected = overwhelm_score > 0.7
    
    return {
        'id': 'emotion_1',
        'timestamp': time.time(),
        'primary_emotion': primary_emotion,
        'confidence': confidence,
        'source': 'rule_based',
        'text_content': text,
        'emotion_scores': emotion_scores,
        'is_overwhelm_detected': is_overwhelm_detected,
        'overwhelm_score': overwhelm_score
    }

def calculate_overwhelm_score(text, emotion_scores):
    """Calculate overwhelm score"""
    overwhelm_emotion_score = emotion_scores.get('overwhelmed', 0.0)
    stress_score = emotion_scores.get('stressed', 0.0)
    anxiety_score = emotion_scores.get('anxious', 0.0)
    
    overwhelm_patterns = [r'\btoo much\b', r'\bcan\'t handle\b', r'\boverwhelming\b', r'\bexhausted\b']
    pattern_score = sum(1 for pattern in overwhelm_patterns if re.search(pattern, text))
    pattern_score = min(pattern_score / len(overwhelm_patterns), 1.0)
    
    total_score = (
        overwhelm_emotion_score * 0.4 +
        stress_score * 0.3 +
        anxiety_score * 0.2 +
        pattern_score * 0.1
    )
    
    return min(total_score, 1.0)

@app.get("/")
async def root():
    return {
        "message": "NeuroDesk API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/brain-dump")
async def brain_dump(request: dict):
    """Process brain dump and generate tasks"""
    try:
        text = request.get('text', '')
        if not text:
            return {"error": "No text provided"}
        
        start_time = time.time()
        
        # Extract tasks
        tasks = extract_tasks(text)
        
        # Detect emotions
        emotion_reading = detect_emotion(text)
        
        processing_time = time.time() - start_time
        
        return {
            "tasks": tasks,
            "emotion_reading": emotion_reading,
            "processing_time": processing_time,
            "total_tasks": len(tasks)
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/v1/detect-emotion")
async def detect_emotion_endpoint(request: dict):
    """Detect emotions in text"""
    try:
        text = request.get('text', '')
        if not text:
            return {"error": "No text provided"}
        
        emotion_result = detect_emotion(text)
        
        if emotion_result:
            return emotion_result
        else:
            return {"error": "Could not detect emotions"}
            
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/v1/generate-summary")
async def generate_summary(request: dict):
    """Generate daily summary and insights"""
    try:
        user_id = request.get('user_id', 'default_user')
        
        # Mock summary generation
        summary_text = f"Today's summary for {user_id}: You've been productive with a mix of high and medium energy tasks. Your mood appears balanced with some stress indicators."
        
        insights = [
            "You tend to work on high-energy tasks in the morning",
            "Consider breaking down larger projects into smaller tasks",
            "Your stress levels are manageable but monitor them"
        ]
        
        recommendations = [
            "Take short breaks between high-energy tasks",
            "Schedule low-energy tasks for afternoon",
            "Practice mindfulness techniques for stress management"
        ]
        
        return {
            "user_id": user_id,
            "summary_text": summary_text,
            "insights": insights,
            "recommendations": recommendations,
            "mood_score": 0.7,
            "productivity_score": 0.8,
            "generated_at": time.time()
        }
        
    except Exception as e:
        return {"error": str(e)}

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 