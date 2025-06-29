# NeuroDesk - AI-Powered Productivity & Mental Wellness App

A Flutter-based application that combines productivity tools with mental wellness features using AI to help users manage tasks, emotions, and prevent burnout.

## 🧠 Core Features

### 1. Brain Dump to Task Cards (AI-Powered)
- Convert scattered thoughts into structured, categorized task cards
- Voice and text input support
- AI-powered categorization (energy, avoidance, emotion)

### 2. Visual Task Deck (Energy-Based UI)
- Organize tasks by required energy rather than strict deadlines
- Kanban-style interface with drag-and-drop functionality
- Energy-based task categorization

### 3. Emotion & Overwhelm Detection (AI)
- Real-time emotion detection from brain dumps
- Automatic suggestion of Reset Mode when overwhelmed
- Offline rule-based fallback

### 4. Burnout Prevention System
- Monitor task streaks and focus duration
- Customizable thresholds (default: 90 min or 3 tasks)
- Automatic break suggestions

### 5. Reset Mode
- Calming full-screen overlay when overwhelm is detected
- Breathing animation with optional cooldown timer (3-5 min)

### 6. TimePie (Optional Timer Layer)
- Visual time tracking with pie/bar charts
- Vibration feedback for time awareness
- Per-task focus time tracking

### 7. Daily Summary / Reflection (AI-Powered)
- End-of-day insights and positive reinforcement
- AI-generated summaries of daily activities
- Template or GPT-driven content

### 8. Notifications
- Gentle reminders for breaks and reflections
- Local notification system

### 9. Local & Cloud Storage
- Offline-first with local storage (Hive/SQLite)
- Future cloud sync support (Firebase/Supabase)

## 🛠 Tech Stack

### Frontend
- **Framework**: Flutter
- **State Management**: Riverpod or Bloc
- **Local Storage**: Hive/SQLite
- **UI Components**: Custom widgets, Draggable/DragTarget
- **Notifications**: flutter_local_notifications

### Backend
- **API**: FastAPI
- **AI/ML**: spaCy, transformers, OpenAI
- **NLP Models**: cardiffnlp/twitter-roberta-base-emotion
- **Storage**: SQLite (local), Firestore/Supabase (cloud)

## 🚀 Getting Started

### Prerequisites
- Flutter SDK (latest stable)
- Python 3.8+ (for FastAPI backend)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NeuroDesk
   ```

2. **Setup Flutter Frontend**
   ```bash
   cd frontend
   flutter pub get
   flutter run
   ```

3. **Setup FastAPI Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

## 📁 Project Structure

```
NeuroDesk/
├── frontend/                 # Flutter application
│   ├── lib/
│   │   ├── models/          # Data models
│   │   ├── services/        # API services
│   │   ├── providers/       # State management
│   │   ├── screens/         # UI screens
│   │   ├── widgets/         # Reusable widgets
│   │   └── utils/           # Utilities
│   └── pubspec.yaml
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/          # Data models
│   │   ├── services/        # Business logic
│   │   ├── api/             # API routes
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── main.py
└── docs/                     # Documentation
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in both frontend and backend directories:

**Backend (.env)**
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./neurodesk.db
```

**Frontend (.env)**
```
API_BASE_URL=http://localhost:8000
```

## 📱 Features in Development

- [x] Project structure setup
- [ ] Brain Dump feature
- [ ] Visual Task Deck
- [ ] Emotion Detection
- [ ] Burnout Prevention
- [ ] Reset Mode
- [ ] TimePie Timer
- [ ] Daily Summary
- [ ] Notifications
- [ ] Local Storage
- [ ] Cloud Sync

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue in the repository. 