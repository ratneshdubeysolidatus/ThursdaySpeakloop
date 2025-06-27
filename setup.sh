#!/bin/bash

# ThursdaySpeakloop Bot - Quick Setup Script

echo "🎤 Setting up ThursdaySpeakloop Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file from template
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Notion credentials"
fi

echo "✅ Setup complete!"
echo "📖 Next steps:"
echo "   1. Edit .env file with your Notion token and database ID"
echo "   2. Run: python app.py"
echo "   3. Open: http://localhost:5000"
