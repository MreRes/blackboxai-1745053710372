import time
from whatsapp_bot import WhatsAppBot

def main():
    chromedriver_path = input("Enter path to ChromeDriver executable: ").strip()
    bot = WhatsAppBot(chromedriver_path)
    try:
        print("Please scan the QR code in the browser window to login to WhatsApp.")
        bot.wait_for_login()
        print("Logged in successfully. Listening for messages...")
        bot.listen_messages()
    except KeyboardInterrupt:
        print("Stopping bot...")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
