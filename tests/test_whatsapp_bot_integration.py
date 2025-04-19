import unittest
import time
from whatsapp_bot import WhatsAppBot

class TestWhatsAppBotIntegration(unittest.TestCase):

    def setUp(self):
        # Provide the path to your chromedriver executable
        self.driver_path = "/path/to/chromedriver"
        self.bot = WhatsAppBot(self.driver_path)
        self.bot.start()
        # Wait some time for manual QR code scan if needed
        print("Please scan the QR code in the browser window to login.")
        time.sleep(30)  # Adjust time as needed for scanning

    def test_send_and_receive_message(self):
        # This test assumes you have a contact named "Test Contact" in WhatsApp
        test_contact = "Test Contact"
        test_message = "Hello from test"
        self.bot.send_message(test_contact, test_message)
        # Wait for bot to process and respond
        time.sleep(10)
        # Since this is an integration test, manual verification may be needed
        print(f"Sent message to {test_contact}: {test_message}")
        print("Please verify the bot's response in WhatsApp manually.")

    def tearDown(self):
        self.bot.stop()

if __name__ == "__main__":
    unittest.main()
