# ThursdaySpeakloop Bot - Feature Demo Guide

## 🎯 Quick Demo Setup

### 1. Start the Application
```bash
python app.py
```
Navigate to: `http://localhost:5000`

### 2. Demo the AI Voice Features
```bash
python demo_ai_voices.py
```

## 🌟 Feature Showcase

### ✅ Real-time Progress Tracking
1. **Start Bot**: Click "Start ThursdaySpeakloop Bot"
2. **Watch Progress Panel**: 
   - Current team and speaker display
   - Progress bar updates automatically
   - Status changes from "Idle" → "Running" → "Completed"
3. **Manual Control**: Bot pauses after each team, click "Resume" to continue

### ✅ Button State Management
- **Start Button**: Automatically disables when bot is running
- **Resume Button**: Appears when bot pauses between teams
- **Reset Button**: Always available to stop and reset

### ✅ Gemini AI Voice Integration
1. **Configure API Key**: 
   - Enter Gemini API key in web interface, OR
   - Set `GEMINI_API_KEY` in `.env` file
2. **Voice Status**: Green indicator shows "AI Voice Active"
3. **Fallback**: Red indicator shows "Standard Voice" if Gemini unavailable

### ✅ Advanced Voice Features
- **30+ Voice Options**: Kore, Puck, Charon, Leda, etc.
- **Dynamic Styles**: Welcome, Friendly, Encouraging, Transition
- **Context-Aware**: Different voices for different announcement types
- **High Quality**: Natural, expressive speech patterns

## 🎭 Voice Demo Scripts

### Test All Voices
```bash
python demo_ai_voices.py
```

### Quick Voice Test
```python
from speaker_bot import test_voice_with_gemini
test_voice_with_gemini("Hello from ThursdaySpeakloop!", "Puck", "friendly")
```

## 📊 Real-time Features

### Progress API Endpoints
- `GET /progress` - Current bot status and progress
- `GET /status` - Bot running state
- `POST /reset` - Stop and reset bot

### Live Updates
- Progress panel updates every 2 seconds
- No page refresh needed
- Seamless user experience

## 🔧 Configuration Options

### Environment Variables
```env
NOTION_TOKEN=your_token
DATABASE_ID=your_database_id
GEMINI_API_KEY=your_gemini_key
VOICE_NAME=Puck
VOICE_STYLE=friendly
```

### Web Interface
- Gemini API key input field
- Real-time status indicators
- Progress tracking panel
- Manual control buttons

## 🚀 Getting Started

1. **Prerequisites**: Notion workspace with team database
2. **Setup**: Copy `.env.example` to `.env` and configure
3. **Install**: `pip install -r requirements.txt`
4. **Run**: `python app.py`
5. **Demo**: Open browser to `localhost:5000`

## 📱 Mobile-Friendly UI

- Responsive design
- Side-by-side layout on desktop
- Stacked layout on mobile
- Touch-friendly buttons

---

**All features are production-ready and fully documented!** 🎉
