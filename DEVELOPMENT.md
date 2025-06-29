# NeuroDesk Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flutter SDK (latest stable)
- Git

### Initial Setup
1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd NeuroDesk
   python setup.py
   ```

2. **Configure environment variables:**
   - Update `backend/.env` with your OpenAI API key
   - Update `frontend/.env` with your API base URL

3. **Run the application:**
   ```bash
   # Terminal 1: Start backend
   cd backend
   python main.py
   
   # Terminal 2: Start frontend
   cd frontend
   flutter run
   ```

## 📁 Project Structure

```
NeuroDesk/
├── frontend/                 # Flutter application
│   ├── lib/
│   │   ├── models/          # Data models (Task, Session, Emotion)
│   │   ├── providers/       # Riverpod state management
│   │   ├── screens/         # UI screens
│   │   ├── widgets/         # Reusable widgets
│   │   ├── theme/           # App theme and styling
│   │   └── main.dart        # App entry point
│   └── pubspec.yaml         # Flutter dependencies
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic
│   │   └── database.py      # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── main.py              # FastAPI entry point
└── docs/                     # Documentation
```

## 🧠 Core Features Implementation

### 1. Brain Dump to Task Cards
**Status:** ✅ Basic implementation complete

**Frontend:** `frontend/lib/screens/brain_dump_screen.dart`
- Text input for brain dumps
- Processing indicator
- Task generation simulation

**Backend:** `backend/app/api/brain_dump.py`
- `/api/v1/brain-dump` endpoint
- AI-powered task extraction
- Emotion detection integration

**Next Steps:**
- [ ] Integrate OpenAI API for better task extraction
- [ ] Add voice input with speech-to-text
- [ ] Implement task categorization with ML

### 2. Visual Task Deck (Energy-Based UI)
**Status:** ✅ Core implementation complete

**Frontend:** `frontend/lib/screens/task_deck_screen.dart`
- Kanban-style energy columns (Low/Medium/High)
- Drag-and-drop functionality
- Task cards with energy indicators

**Models:** `frontend/lib/models/task.dart`
- Task model with energy levels
- Status management
- Category classification

**Next Steps:**
- [ ] Add task filtering and sorting
- [ ] Implement task editing
- [ ] Add task templates

### 3. Emotion & Overwhelm Detection
**Status:** ✅ Basic implementation complete

**Backend:** `backend/app/services/emotion_detector.py`
- Rule-based emotion detection
- Overwhelm score calculation
- Keyword-based analysis

**Models:** `frontend/lib/models/emotion.dart`
- Emotion types and readings
- Overwhelm detection
- Emotion trends

**Next Steps:**
- [ ] Integrate cardiffnlp/twitter-roberta-base-emotion model
- [ ] Add real-time emotion tracking
- [ ] Implement emotion history

### 4. Burnout Prevention System
**Status:** 🔄 Partially implemented

**Models:** `frontend/lib/models/session.dart`
- Focus session tracking
- Daily session aggregation
- Burnout indicators

**Next Steps:**
- [ ] Implement session timer
- [ ] Add burnout detection algorithms
- [ ] Create break reminders

### 5. Reset Mode
**Status:** ⏳ Not implemented

**Planned Features:**
- Full-screen calming overlay
- Breathing animation
- Cooldown timer
- Overwhelm detection triggers

### 6. TimePie Timer
**Status:** ⏳ Not implemented

**Planned Features:**
- Visual time tracking
- Pie/bar chart visualization
- Vibration feedback
- Per-task focus tracking

### 7. Daily Summary / Reflection
**Status:** ✅ Basic API structure complete

**Backend:** `backend/app/api/summary_generation.py`
- `/api/v1/generate-summary` endpoint
- Mock summary generation
- Insights and recommendations

**Next Steps:**
- [ ] Integrate with actual user data
- [ ] Add AI-powered insights
- [ ] Implement summary scheduling

### 8. Notifications
**Status:** ⏳ Not implemented

**Planned Features:**
- Break reminders
- Reflection prompts
- Overwhelm alerts
- Daily summary notifications

### 9. Local & Cloud Storage
**Status:** ✅ Local storage implemented

**Frontend:** `frontend/lib/providers/task_provider.dart`
- Hive local storage
- Offline-first architecture
- State management with Riverpod

**Next Steps:**
- [ ] Add cloud sync (Firebase/Supabase)
- [ ] Implement data backup
- [ ] Add data export/import

## 🛠 Development Workflow

### Frontend Development
```bash
cd frontend

# Get dependencies
flutter pub get

# Run the app
flutter run

# Generate code (for Hive, Riverpod, etc.)
flutter packages pub run build_runner build

# Run tests
flutter test
```

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest
```

### Code Generation
The project uses code generation for:
- **Hive adapters:** `flutter packages pub run build_runner build`
- **Riverpod providers:** `flutter packages pub run build_runner build`
- **API clients:** `flutter packages pub run build_runner build`

## 🧪 Testing Strategy

### Frontend Testing
- **Unit tests:** Provider logic, utility functions
- **Widget tests:** UI components
- **Integration tests:** User workflows

### Backend Testing
- **Unit tests:** Service logic, utility functions
- **API tests:** Endpoint functionality
- **Integration tests:** Database operations

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./neurodesk.db
```

**Frontend (.env):**
```env
API_BASE_URL=http://localhost:8000
```

### Feature Flags
- Enable/disable AI features
- Toggle voice input
- Configure emotion detection sensitivity

## 📊 Performance Considerations

### Frontend
- Lazy loading for large task lists
- Efficient state management with Riverpod
- Optimized animations and transitions

### Backend
- Async processing for AI operations
- Database connection pooling
- Caching for frequently accessed data

## 🔒 Security

### Data Protection
- Local data encryption with Hive
- Secure API communication
- User data privacy controls

### API Security
- Input validation with Pydantic
- Rate limiting
- CORS configuration

## 🚀 Deployment

### Frontend (Flutter)
- Build for Android: `flutter build apk`
- Build for iOS: `flutter build ios`
- Web deployment: `flutter build web`

### Backend (FastAPI)
- Docker containerization
- Environment-specific configurations
- Database migrations with Alembic

## 🤝 Contributing

### Code Style
- **Frontend:** Follow Flutter style guide
- **Backend:** Follow PEP 8
- **Documentation:** Clear docstrings and comments

### Git Workflow
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

## 📈 Roadmap

### Phase 1: Core Features ✅
- [x] Basic task management
- [x] Brain dump functionality
- [x] Emotion detection
- [x] Energy-based UI

### Phase 2: AI Integration 🔄
- [ ] OpenAI integration
- [ ] Advanced emotion detection
- [ ] Smart task categorization
- [ ] Personalized insights

### Phase 3: Advanced Features ⏳
- [ ] Reset mode
- [ ] TimePie timer
- [ ] Notifications
- [ ] Cloud sync

### Phase 4: Polish & Scale ⏳
- [ ] Performance optimization
- [ ] Advanced analytics
- [ ] Multi-platform support
- [ ] Enterprise features

## 🆘 Troubleshooting

### Common Issues

**Flutter build errors:**
```bash
flutter clean
flutter pub get
flutter packages pub run build_runner build --delete-conflicting-outputs
```

**Backend import errors:**
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

**Hive database issues:**
```bash
# Clear Hive data
flutter packages pub run build_runner clean
```

## 📚 Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Riverpod Documentation](https://riverpod.dev/)
- [Hive Documentation](https://docs.hivedb.dev/)

## 🎯 Next Steps

1. **Complete AI Integration:** Integrate OpenAI API for better task extraction
2. **Implement Reset Mode:** Create the calming overlay for overwhelm
3. **Add Notifications:** Implement local notifications for breaks and reminders
4. **Enhance Analytics:** Add more detailed productivity insights
5. **Cloud Sync:** Implement data synchronization across devices

---

**Happy coding! 🚀** 