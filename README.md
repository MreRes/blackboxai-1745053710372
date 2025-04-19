# WhatsApp AI Financial Planner Assistant

This project is a WhatsApp chatbot AI Financial Planner Assistant to help manage and record personal finances. It uses an unofficial WhatsApp gateway (wa wab) with ChromeDriver for WhatsApp automation and Hugging Face transformers for AI natural language understanding.

## Features

- Report income and expenses in Indonesian language (formal, informal, and mixed sentence formats)
- Store financial data securely
- Access financial reports via chatbot and a web interface
- Logging for debugging and monitoring
- Automated testing for chatbot functionality and error detection
- Test result reporting program

## Technology Stack

- Python 3.11.0
- wa wab (unofficial WhatsApp gateway) with ChromeDriver
- Hugging Face transformers for AI
- SQLite for data storage
- Flask for web interface
- Logging module for debugging
- Pytest for testing

## Setup

1. Install Python 3.11.0
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Download and setup ChromeDriver compatible with your Chrome version.
4. Run the WhatsApp bot:
   ```
   python whatsapp_bot.py
   ```
5. Run the web app:
   ```
   python web_app.py
   ```

## Testing

Run tests with:
```
pytest tests/
```

## Notes

- This project uses an unofficial WhatsApp gateway and may be subject to WhatsApp's terms of service.
- Use responsibly and ensure data privacy.
