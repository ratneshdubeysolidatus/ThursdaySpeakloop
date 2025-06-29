# ThursdaySpeakloop Bot 🎤

An automated meeting facilitator bot that integrates with Notion databases to randomly select team members for standup updates using text-to-speech.

## Features

- 🤖 **AI-Enhanced Voices**: Gemini AI integration for expressive, human-like speech
- 🎭 **Multiple Voice Personalities**: Choose from 30+ distinct AI voices (Kore, Puck, Charon, etc.)
- 🎨 **Contextual Speech Styles**: Welcome, friendly, encouraging, completion tones
- 🗣️ **Intelligent Fallback**: Gracefully falls back to pyttsx3 if Gemini unavailable
- 🎲 **Random Selection**: Fairly shuffles teams and randomly picks team members
- ⏸️ **Smart Auto-Pause**: Automatically pauses after each team's update
- 🎮 **Manual Control**: Resume to continue to next team, or manually pause anytime
- ✅ **Completion Detection**: Automatically stops when all teams have presented
- 🌐 **Web Interface**: Clean, modern UI with real-time status updates
- 📊 **Notion Integration**: Fetches team data directly from your Notion database
- 🐳 **Docker Support**: Containerized deployment ready

## Prerequisites

- Python 3.10+
- Notion API Token
- **Gemini AI API Key** (optional, for enhanced voices)
- Notion Database with the following structure:
  - `Name` (Title): Team name
  - `Developers` (Multi-select): List of team members

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/ratneshdubeysolidatus/ThursdaySpeakloop.git
   cd ThursdaySpeakloop
   ```

2. **Set up virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Copy the example environment file and configure:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your credentials:

   ```env
   NOTION_TOKEN=your_notion_token
   DATABASE_ID=your_database_id
   GEMINI_API_KEY=your_gemini_key  # Optional for AI voices
   ```

5. **Configure AI Voices (Optional)**

   - Get Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Add to `.env` file (required for enhanced voices)
   - Test voices at [AI Studio Speech](https://aistudio.google.com/generate-speech)

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## How It Works

The bot follows a structured workflow designed for smooth meeting facilitation:

1. **🚀 Start**: Bot announces the beginning of the meeting
2. **🎲 Random Selection**: Teams and speakers are shuffled for fairness
3. **📢 Team Announcement**: Bot calls out the team name
4. **👤 Speaker Selection**: Randomly chosen team member is announced
5. **⏸️ Auto-Pause**: Bot automatically pauses after each team's update
6. **▶️ Manual Resume**: Click "Resume" to continue to the next team
7. **🔄 Repeat**: Process continues for all teams
8. **✅ Completion**: Bot announces end when all teams have presented
9. **🎭 Joke Section**: Bot tells a relevant, AI-generated joke to end on a positive note
10. **👋 Sign-off**: Final goodbye message

### Meeting Control

- **Auto-Pause**: After each team completes their update, the bot pauses automatically
- **Manual Control**: Use the web interface to pause/resume anytime
- **Real-time Status**: Live updates show current bot state
- **Progress Tracking**: See which teams have completed their updates

## Configuration

### Notion Setup

1. Create a Notion integration at https://developers.notion.com/
2. Copy your internal integration token
3. Share your database with the integration
4. Copy your database ID from the URL

### Environment Variables (Recommended)

Create a `.env` file:

```
NOTION_TOKEN=your_notion_token_here
DATABASE_ID=your_database_id_here
```

## Voice Enhancement with Gemini AI 🤖

### Setup Gemini AI (Optional but Recommended)

1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Test Voices**: Try different voices at [AI Studio Speech](https://aistudio.google.com/generate-speech)
3. **Configure**: Add your API key to environment or web interface

### Voice Features

**🎭 Available Voices** (30+ options):

- **Kore**: Firm, authoritative
- **Puck**: Upbeat, energetic
- **Charon**: Informative, clear
- **Leda**: Youthful, friendly
- **Aoede**: Breezy, casual
- **Enceladus**: Breathy, gentle

**🎨 Dynamic Styles**:

- **Welcome**: Enthusiastic meeting start
- **Friendly**: Professional team calls
- **Encouraging**: Supportive member selection
- **Completion**: Celebratory wrap-up
- **Transition**: Smooth flow between teams

### Environment Variables (Enhanced)

Create a `.env` file:

```env
# Notion Configuration
NOTION_TOKEN=your_notion_token_here
DATABASE_ID=your_database_id_here

# Gemini AI Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
```

**Without Gemini**: Bot uses pyttsx3 (standard TTS)  
**With Gemini**: Bot uses AI-enhanced expressive voices

### AI-Powered Features

With Gemini AI enabled, the bot provides enhanced functionality:

**🎭 Smart Joke Generation**
- Fresh, relevant jokes for each meeting
- Business/tech/workplace themed humor
- Quality validation with retry logic
- Clean, professional content
- Fallback jokes if AI unavailable

**🗣️ Expressive Voice Synthesis**
- Natural, context-aware speech patterns
- Dynamic emotional styles (welcome, friendly, encouraging)
- Professional voice consistency
- High-quality 24kHz audio output

### Voice Selection

The bot now provides **consistent voice selection** throughout the meeting:

- **UI Selection**: Choose your preferred voice from the dropdown menu
- **Available Voices**: Kore, Puck, Charon, Leda, Aoede, Enceladus
- **Consistent Experience**: Same voice used for all announcements
- **Security**: Gemini API key secured via environment variables only

## Docker Deployment

```bash
docker build -t thursday-speakloop-bot .
docker run -p 5000:5000 thursday-speakloop-bot
```

## API Endpoints

- `GET /` - Main interface with real-time status
- `POST /` - Start bot with credentials
- `POST /pause` - Manually pause the bot
- `POST /resume` - Resume the bot (works for both manual and auto-pause)
- `GET /status` - Get current bot status (JSON response)

## Project Structure

```
├── app.py                 # Flask web application
├── speaker_bot.py         # Core bot logic
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── templates/
│   ├── index.html        # Main interface
│   └── success.html      # Success page
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use and modify as needed.

## Security Note

Never commit API tokens or sensitive credentials to version control. Use environment variables or secure configuration files that are gitignored.
