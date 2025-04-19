# WhatsApp AI Financial Planner Assistant

This project is a WhatsApp chatbot AI Financial Planner Assistant to help manage and record personal finances. It uses an unofficial WhatsApp gateway (wa wab) with ChromeDriver for WhatsApp automation and Hugging Face transformers for AI natural language understanding.

## Features

- Report income and expenses in Indonesian language (formal, informal, and mixed sentence formats)
- Store financial data securely
- Access financial reports via chatbot and a web interface with authentication
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
   python whatsapp_bot.py <path_to_chromedriver>
   ```
5. Run the web app:
   ```
   python web_app.py
   ```
6. Access the web app at `http://localhost:5000/login` and login with:
   - Username: admin
   - Password: password123

## Testing

Run tests with:
```
python tests/test_reporter.py
```

## Deployment

For convenience, you can run both the WhatsApp bot and web app concurrently using a terminal multiplexer or separate terminals.

Alternatively, create a shell script `run.sh`:

```bash
#!/bin/bash
# Run WhatsApp bot and web app concurrently

# Replace with your chromedriver path
CHROMEDRIVER_PATH="/path/to/chromedriver"

# Start WhatsApp bot in background
python whatsapp_bot.py "$CHROMEDRIVER_PATH" &

# Start web app
python web_app.py
```

Make it executable:
```
chmod +x run.sh
```

Run:
```
./run.sh
```

## Notes

- This project uses an unofficial WhatsApp gateway and may be subject to WhatsApp's terms of service.
- Use responsibly and ensure data privacy.
