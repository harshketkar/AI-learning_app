﻿# AI Learning App

An automated Flask learning platform that generates and delivers daily Flask development content using Google's Gemini AI. The application sends customized learning materials, including topic summaries and practice questions, directly to your email.

## Features

- 🤖 AI-powered content generation using Google's Gemini API
- 📧 Automated daily email delivery of learning materials
- 📚 Comprehensive Flask development topics
- ❓ Practice questions for each topic
- ⏰ Scheduled content delivery at 7:00 AM daily
- 🔄 Manual trigger endpoint for immediate content delivery
- 📝 Content logging for tracking sent topics

## Prerequisites

- Python 3.11 or higher
- Gmail account for sending emails
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd AI-learning_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following configuration:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-specific-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   RECIPIENT_EMAIL=recipient-email@example.com
   GEMINI_API_KEY=your-gemini-api-key
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. The application will:
   - Start the scheduler to send daily content at 7:00 AM
   - Run the Flask server on `http://localhost:5000`

### Endpoints

- `/send-now` - Manually trigger content generation and delivery
- `/health` - Health check endpoint

## Technology Stack

- **Flask**: Web framework for the application
- **Google Gemini AI**: Content generation
- **APScheduler**: Task scheduling
- **Flask-Mail**: Email handling
- **python-dotenv**: Environment variable management
- **LangChain**: AI/ML operations

## Project Structure

```
AI-learning_app/
├── app.py              # Main application file
├── topics.py           # Flask learning topics
├── requirements.txt    # Project dependencies
├── sent_topics.txt    # Log of sent topics
└── .env               # Environment variables
```

## Security Notes

- Store sensitive information in the `.env` file
- Use app-specific passwords for Gmail
- Keep your Gemini API key secure

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

