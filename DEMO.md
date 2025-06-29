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

### ✅ Advanced Voice Features

1. **Choose Voice**: Select from 6 AI voices in the web interface
2. **Consistent Experience**: Same voice used throughout the meeting
3. **Secure Configuration**: API key only via environment variables
4. **Voice Status**: Green indicator shows "AI Voice Active"
5. **Fallback**: Red indicator shows "Standard Voice" if Gemini unavailable

### ✅ Advanced Voice Features

- **Consistent Voice Selection**: Choose one voice for entire meeting
- **6 AI Voice Options**: Kore, Puck, Charon, Leda, Aoede, Enceladus
- **Dynamic Styles**: Welcome, Friendly, Encouraging, Transition
- **Context-Aware**: Different emotional tones for different announcements
- **High Quality**: Natural, expressive speech patterns
- **Secure**: API key only via environment variables

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
# Notion Configuration
NOTION_TOKEN=your_token
DATABASE_ID=your_database_id

# Gemini AI (Required for enhanced voices)
GEMINI_API_KEY=your_gemini_key
```

### Web Interface

- Voice selection dropdown
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
