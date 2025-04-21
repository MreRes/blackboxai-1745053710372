# WhatsApp Bot Setup Guide

This guide explains how to set up and run the WhatsApp bot locally on your computer.

## Prerequisites

- Node.js (version 16 or higher recommended)
- npm (Node package manager)
- Internet connection
- WhatsApp mobile app installed on your phone

## Setup Steps

1. **Clone or download the project repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**

   Run the following command in the project root directory to install required Node.js packages:

   ```bash
   npm install
   ```

3. **Start the bot**

   Run the bot with:

   ```bash
   node wa_bot_complete_full.js
   ```

4. **Access the QR code**

   - When the bot starts, it will attempt to connect to WhatsApp.
   - A QR code will be generated and printed in the terminal with clear separators.
   - Additionally, the QR code is served as an image at [http://localhost:8000](http://localhost:8000).
   - Open this URL in your web browser to scan the QR code with your WhatsApp mobile app.

5. **Scan the QR code**

   - Open WhatsApp on your phone.
   - Go to the WhatsApp Web section.
   - Scan the QR code displayed in the terminal or browser.
   - Once scanned, the bot will connect and start processing messages.

## Troubleshooting

- If you do not see the QR code in the terminal:
  - Check the terminal output for the section between:
    ```
    ========== WHATSAPP QR CODE ==========
    (QR code ASCII art)
    ========== END OF QR CODE ==========
    ```
  - If missing, open [http://localhost:8000](http://localhost:8000) in your browser to view the QR code image.

- If the bot shows connection errors or fails to receive the QR code:
  - Ensure your internet connection is stable.
  - Verify that your network allows WebSocket connections.
  - Check that the WhatsApp API version used by the bot is up to date.
  - Restart the bot to retry connection.

- If you get logged out or the bot disconnects:
  - Delete the `baileys_auth_info` folder in the project directory to reset authentication.
  - Restart the bot and scan the QR code again.

## Additional Notes

- The bot uses the Baileys library to connect to WhatsApp Web.
- The QR code is essential for authenticating the bot with your WhatsApp account.
- Keep your phone connected to the internet while using the bot.

## Contact

For further assistance, please refer to the project documentation or contact the maintainer.

---
