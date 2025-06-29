from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

# HTML interface
HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeuroDesk - Brain Dump & Task Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4A90E2 0%, #7BB3F0 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .content {
            padding: 30px;
        }

        .section {
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 15px;
            background: #f8f9fa;
            border-left: 5px solid #4A90E2;
        }

        .section h2 {
            color: #4A90E2;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .input-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
        }

        textarea:focus {
            outline: none;
            border-color: #4A90E2;
        }

        button {
            background: linear-gradient(135deg, #4A90E2 0%, #7BB3F0 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .results {
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border: 1px solid #e1e5e9;
        }

        .task-card {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #4A90E2;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .task-title {
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }

        .task-meta {
            display: flex;
            gap: 15px;
            font-size: 14px;
            color: #666;
        }

        .energy-high { border-left-color: #E57373; }
        .energy-medium { border-left-color: #FFB74D; }
        .energy-low { border-left-color: #81C784; }

        .emotion-result {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #e1e5e9;
        }

        .emotion-primary {
            font-weight: 600;
            color: #4A90E2;
            margin-bottom: 10px;
        }

        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }

        .example-text {
            background: #f0f8ff;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-style: italic;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 NeuroDesk</h1>
            <p>AI-Powered Brain Dump & Task Management</p>
        </div>

        <div class="content">
            <!-- Brain Dump Section -->
            <div class="section">
                <h2>💭 Brain Dump to Tasks</h2>
                <p>Type your scattered thoughts and we'll convert them into organized tasks with energy levels.</p>
                
                <div class="example-text">
                    <strong>Example:</strong><br>
                    "Need to finish project report, feeling stressed about meeting tomorrow, want to start learning guitar, should call mom this week"
                </div>

                <div class="input-group">
                    <label for="brainDumpText">Your Thoughts:</label>
                    <textarea id="brainDumpText" placeholder="Type your thoughts here..."></textarea>
                </div>

                <button onclick="processBrainDump()" id="brainDumpBtn">Generate Tasks</button>

                <div id="brainDumpResults" class="results" style="display: none;">
                    <h3>Generated Tasks:</h3>
                    <div id="tasksList"></div>
                    
                    <h3>Emotion Analysis:</h3>
                    <div id="emotionAnalysis"></div>
                </div>
            </div>

            <!-- Emotion Detection Section -->
            <div class="section">
                <h2>😊 Emotion Detection</h2>
                <p>Analyze the emotional content of your text.</p>

                <div class="input-group">
                    <label for="emotionText">Text to Analyze:</label>
                    <textarea id="emotionText" placeholder="Enter text to analyze emotions..."></textarea>
                </div>

                <button onclick="detectEmotion()" id="emotionBtn">Detect Emotions</button>

                <div id="emotionResults" class="results" style="display: none;">
                    <h3>Emotion Analysis Results:</h3>
                    <div id="emotionDetails"></div>
                </div>
            </div>

            <!-- Daily Summary Section -->
            <div class="section">
                <h2>📊 Daily Summary</h2>
                <p>Generate insights and recommendations for your day.</p>

                <button onclick="generateSummary()" id="summaryBtn">Generate Summary</button>

                <div id="summaryResults" class="results" style="display: none;">
                    <h3>Daily Summary:</h3>
                    <div id="summaryDetails"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = ''; // Use relative paths for Vercel deployment

        async function processBrainDump() {
            const text = document.getElementById('brainDumpText').value.trim();
            if (!text) {
                alert('Please enter some text first!');
                return;
            }

            const btn = document.getElementById('brainDumpBtn');
            const results = document.getElementById('brainDumpResults');
            
            btn.disabled = true;
            btn.textContent = 'Processing...';
            results.style.display = 'none';

            try {
                const response = await fetch(`/api/v1/brain-dump`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text })
                });

                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                displayTasks(data.tasks);
                displayEmotion(data.emotion_reading);
                
                results.style.display = 'block';
                
            } catch (error) {
                showError('Brain Dump', error.message);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate Tasks';
            }
        }

        async function detectEmotion() {
            const text = document.getElementById('emotionText').value.trim();
            if (!text) {
                alert('Please enter some text first!');
                return;
            }

            const btn = document.getElementById('emotionBtn');
            const results = document.getElementById('emotionResults');
            
            btn.disabled = true;
            btn.textContent = 'Analyzing...';
            results.style.display = 'none';

            try {
                const response = await fetch(`/api/v1/detect-emotion`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text })
                });

                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                displayEmotionDetails(data);
                results.style.display = 'block';
                
            } catch (error) {
                showError('Emotion Detection', error.message);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Detect Emotions';
            }
        }

        async function generateSummary() {
            const btn = document.getElementById('summaryBtn');
            const results = document.getElementById('summaryResults');
            
            btn.disabled = true;
            btn.textContent = 'Generating...';
            results.style.display = 'none';

            try {
                const response = await fetch(`/api/v1/generate-summary`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_id: 'user_1' })
                });

                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                displaySummary(data);
                results.style.display = 'block';
                
            } catch (error) {
                showError('Summary Generation', error.message);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate Summary';
            }
        }

        function displayTasks(tasks) {
            const container = document.getElementById('tasksList');
            container.innerHTML = '';

            tasks.forEach(task => {
                const taskCard = document.createElement('div');
                taskCard.className = `task-card energy-${task.energy}`;
                
                taskCard.innerHTML = `
                    <div class="task-title">${task.title}</div>
                    <div class="task-meta">
                        <span>Energy: ${task.energy}</span>
                        <span>Category: ${task.category}</span>
                        <span>Status: ${task.status}</span>
                        ${task.is_avoidance ? '<span style="color: #E57373;">⚠️ Avoidance</span>' : ''}
                    </div>
                `;
                
                container.appendChild(taskCard);
            });
        }

        function displayEmotion(emotion) {
            const container = document.getElementById('emotionAnalysis');
            container.innerHTML = `
                <div class="emotion-result">
                    <div class="emotion-primary">Primary Emotion: ${emotion.primary_emotion}</div>
                    <div>Confidence: ${(emotion.confidence * 100).toFixed(1)}%</div>
                    <div>Overwhelm Score: ${(emotion.overwhelm_score * 100).toFixed(1)}%</div>
                    ${emotion.is_overwhelm_detected ? '<div style="color: #E57373; font-weight: 600;">⚠️ Overwhelm Detected</div>' : ''}
                </div>
            `;
        }

        function displayEmotionDetails(emotion) {
            const container = document.getElementById('emotionDetails');
            container.innerHTML = `
                <div class="emotion-result">
                    <div class="emotion-primary">Primary Emotion: ${emotion.primary_emotion}</div>
                    <div>Confidence: ${(emotion.confidence * 100).toFixed(1)}%</div>
                    <div>Overwhelm Score: ${(emotion.overwhelm_score * 100).toFixed(1)}%</div>
                    ${emotion.is_overwhelm_detected ? '<div style="color: #E57373; font-weight: 600;">⚠️ Overwhelm Detected</div>' : ''}
                    <div style="margin-top: 10px;">
                        <strong>All Emotions:</strong><br>
                        ${Object.entries(emotion.emotion_scores).map(([emotion, score]) => 
                            `${emotion}: ${(score * 100).toFixed(1)}%`
                        ).join(', ')}
                    </div>
                </div>
            `;
        }

        function displaySummary(summary) {
            const container = document.getElementById('summaryDetails');
            container.innerHTML = `
                <div style="margin-bottom: 20px;">
                    <strong>Summary:</strong><br>
                    ${summary.summary_text}
                </div>
                
                <div style="margin-bottom: 20px;">
                    <strong>Insights:</strong><br>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        ${summary.insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <strong>Recommendations:</strong><br>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        ${summary.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
                
                <div style="display: flex; gap: 20px;">
                    <div><strong>Mood Score:</strong> ${(summary.mood_score * 100).toFixed(0)}%</div>
                    <div><strong>Productivity Score:</strong> ${(summary.productivity_score * 100).toFixed(0)}%</div>
                </div>
            `;
        }

        function showError(feature, message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.innerHTML = `<strong>${feature} Error:</strong> ${message}`;
            
            // Remove any existing error messages
            document.querySelectorAll('.error').forEach(el => el.remove());
            
            // Add the new error message
            document.querySelector('.content').insertBefore(errorDiv, document.querySelector('.content').firstChild);
            
            // Remove error after 5 seconds
            setTimeout(() => errorDiv.remove(), 5000);
        }

        // Add some example text on page load
        window.onload = function() {
            document.getElementById('brainDumpText').value = 
                "Need to finish project report\\nFeeling stressed about meeting tomorrow\\nWant to start learning guitar\\nShould call mom this week";
            
            document.getElementById('emotionText').value = 
                "I'm feeling overwhelmed with work and stressed about the upcoming deadline. I need to take a break and exercise more.";
        };
    </script>
</body>
</html>
"""

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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the HTML interface"""
    return HTMLResponse(content=HTML_INTERFACE)

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