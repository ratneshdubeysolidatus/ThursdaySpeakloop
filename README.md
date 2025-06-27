# ThursdaySpeakloop Bot 🎤

An automated meeting facilitator bot that integrates with Notion databases to randomly select team members for standup updates using text-to-speech.

## Features

- 🗣️ **Text-to-Speech**: Audibly announces team turns and selected speakers
- 🎲 **Random Selection**: Fairly shuffles teams and randomly picks team members
- ⏸️ **Pause/Resume**: Real-time control during meetings
- 🌐 **Web Interface**: Clean, modern UI for easy configuration
- 📊 **Notion Integration**: Fetches team data directly from your Notion database
- 🐳 **Docker Support**: Containerized deployment ready

## Prerequisites

- Python 3.10+
- Notion API Token
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

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

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

## Docker Deployment

```bash
docker build -t thursday-speakloop-bot .
docker run -p 5000:5000 thursday-speakloop-bot
```

## API Endpoints

- `GET /` - Main interface
- `POST /` - Start bot with credentials
- `POST /pause` - Pause the bot
- `POST /resume` - Resume the bot

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
