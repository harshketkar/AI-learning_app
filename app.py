from flask import Flask, jsonify
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)
scheduler = BackgroundScheduler()

# Create the prompt template
prompt_template = """Generate a daily learning content for Python Flask development. Include a topic header, a comprehensive summary, and 4-5 practice questions.

The content should be formatted in markdown like this:

---
**Topic:** [Generate an interesting Flask development topic]

**Summary:** [Provide a detailed explanation of the topic, including key concepts, best practices, and real-world applications]

**Practice Questions:**
1. [Question 1]
2. [Question 2]
[Optional Question 3]
---

Make sure the content is thorough, practical, and suitable for full-stack Python Flask developers."""

def log_sent_topic(content):
    """Log the sent topic with timestamp to a text file"""
    log_file = 'sent_topics.txt'
    current_time = datetime.now()
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n=== {current_time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(content)
            f.write("\n" + "="*50)
        
    except Exception as e:
        print(f"Error logging topic: {e}")

def generate_daily_content():
    """Generate daily content using Gemini API"""
    try:
        # Generate content using Gemini
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def send_daily_content():
    """Generate and send daily Flask content via email"""
    try:
        # Generate content
        content = generate_daily_content()
        
        if not content:
            return False
        
        # Create message
        msg = Message(
            subject="Your Daily Flask Learning Content",
            recipients=[os.getenv('RECIPIENT_EMAIL')],
            body=content
        )
        
        # Send email
        with app.app_context():
            mail.send(msg)
            
        # Log the sent content
        log_sent_topic(content)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/send-now')
def send_now():
    """Manual trigger endpoint for testing"""
    success = send_daily_content()
    if success:
        return jsonify({"status": "success", "message": "Content generated and sent successfully!"})
    return jsonify({"status": "error", "message": "Failed to generate or send content"}), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

# Schedule the job to run daily at 7:00 AM
scheduler.add_job(
    func=send_daily_content,
    trigger='cron',
    hour=7,
    minute=0
)

if __name__ == '__main__':
    # Start the scheduler
    scheduler.start()
    
    # Run the Flask app
    app.run(debug=True)
