import concurrent.futures
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from logger_config import setup_logger
import threading
import sys
import os
import argparse

logger = setup_logger()

class WhatsAppBot:
    def __init__(self, driver_path: str, user_data_dir: str = None):
        self.driver_path = driver_path
        self.driver = None
        # Allow custom user data directory for session persistence
        if user_data_dir:
            self.user_data_dir = os.path.abspath(user_data_dir)
        else:
            self.user_data_dir = os.path.abspath("./User_Data")

    def start(self):
        import platform
        logger.info("Starting WhatsApp Bot...")
        options = Options()
        # Use a persistent user data directory to save session
        options.add_argument(f"--user-data-dir={self.user_data_dir}")  # To keep session
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        # Uncomment the following line to run Chrome in headless mode for testing
        # options.add_argument("--headless")
        # Specify Chrome binary location if needed
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

        # Use webdriver_manager to get ChromeDriver automatically
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://web.whatsapp.com")
        logger.info(f"Please scan the QR code to log in if not already logged in. Session data stored in {self.user_data_dir}")
        # Wait for login
        self.wait_for_login()

    def wait_for_login(self):
        logger.info("Waiting for WhatsApp Web to load and login...")
        while True:
            try:
                # Check for the presence of the search box as login confirmation
                search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                if search_box.is_displayed():
                    logger.info("Logged in successfully.")
                    break
            except Exception:
                pass
            time.sleep(2)

    async def listen_messages_async(self):
        logger.info("Listening for incoming messages asynchronously...")
        from ai_model import FinancialPlannerAI
        from data_storage import DataStorage
        import re

        ai = FinancialPlannerAI()
        storage = DataStorage()

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor()

        async def process_chat(chat):
            try:
                parent = await loop.run_in_executor(executor, lambda: chat.find_element(By.XPATH, './../../..'))
                chat_title = await loop.run_in_executor(executor, lambda: parent.find_element(By.XPATH, './/span[@dir="auto"]').text)
                await loop.run_in_executor(executor, parent.click)
                await asyncio.sleep(2)

                messages = await loop.run_in_executor(executor, lambda: self.driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]//span[@class="selectable-text copyable-text"]'))
                if not messages:
                    return
                last_message = messages[-1].text.strip()
                logger.info(f"Received message from {chat_title}: {last_message}")

                # Send acknowledgment message to confirm receipt
                ack_message = "Pesan Anda telah diterima oleh bot."
                await loop.run_in_executor(executor, lambda: self.send_message(chat_title, ack_message))

                income_pattern = re.compile(r'(pemasukan|income|masuk|terima|dapat|nambah|tambah|deposit|credit).*?([\d.,]+)', re.IGNORECASE)
                outcome_pattern = re.compile(r'(pengeluaran|keluar|pakai|bayar|kurang|utang|debit|withdraw).*?([\d.,]+)', re.IGNORECASE)

                def parse_amount(text):
                    cleaned = text.replace('.', '').replace(',', '')
                    try:
                        return float(cleaned)
                    except:
                        return None

                amount = None
                description = last_message
                if income_pattern.search(last_message):
                    amount_match = income_pattern.search(last_message)
                    amount = parse_amount(amount_match.group(2))
                    if amount is not None:
                        user_id = storage.get_user_id_by_phone(chat_title)
                        if user_id is None:
                            user_id = 1  # default user id fallback
                        storage.add_income(user_id, amount, description, sender_phone=chat_title)
                        response_text = f"Pemasukan sebesar Rp {amount} telah dicatat."
                    else:
                        response_text = "Maaf, saya tidak dapat mengenali jumlah pemasukan."
                elif outcome_pattern.search(last_message):
                    amount_match = outcome_pattern.search(last_message)
                    amount = parse_amount(amount_match.group(2))
                    if amount is not None:
                        user_id = storage.get_user_id_by_phone(chat_title)
                        if user_id is None:
                            user_id = 1  # default user id fallback
                        storage.add_outcome(user_id, amount, description, sender_phone=chat_title)
                        response_text = f"Pengeluaran sebesar Rp {amount} telah dicatat."
                    else:
                        response_text = "Maaf, saya tidak dapat mengenali jumlah pengeluaran."
                elif last_message.lower() in ['laporan', 'report', 'rekap']:
                    user_id = storage.get_user_id_by_phone(chat_title)
                    if user_id is None:
                        user_id = 1
                    report = storage.get_report(user_id)
                    if report:
                        response_text = (f"Laporan Keuangan:\n"
                                         f"Pemasukan: Rp {report['total_income']}\n"
                                         f"Pengeluaran: Rp {report['total_outcome']}\n"
                                         f"Saldo: Rp {report['balance']}\n\n"
                                         f"Untuk laporan lengkap, kunjungi: http://localhost:5000")
                    else:
                        response_text = "Maaf, tidak dapat mengambil laporan saat ini."
                elif last_message.lower().startswith('add budget'):
                    try:
                        parts = last_message.split()
                        if len(parts) >= 5:
                            category = parts[2]
                            amount = float(parts[3])
                            period = parts[4]
                            storage.add_budget(user_id, category, amount, period)
                            response_text = f"Budget untuk kategori '{category}' sebesar Rp {amount} per {period} telah ditambahkan."
                        else:
                            response_text = "Format perintah budget salah. Gunakan: add budget <kategori> <jumlah> <periode>"
                    except Exception as e:
                        response_text = f"Terjadi kesalahan saat menambahkan budget: {e}"
                elif last_message.lower().startswith('show budgets'):
                    budgets = storage.get_budgets(user_id)
                    if budgets:
                        response_text = "Daftar Budget:\n"
                        for b in budgets:
                            response_text += f"- {b['category']}: Rp {b['amount']} per {b['period']}\n"
                    else:
                        response_text = "Belum ada budget yang tercatat."
                elif last_message.lower().startswith('add goal'):
                    try:
                        parts = last_message.split()
                        if len(parts) >= 4:
                            name = parts[2]
                            target_amount = float(parts[3])
                            storage.add_goal(user_id, name, target_amount)
                            response_text = f"Goal '{name}' dengan target Rp {target_amount} telah ditambahkan."
                        else:
                            response_text = "Format perintah goal salah. Gunakan: add goal <nama> <target_jumlah>"
                    except Exception as e:
                        response_text = f"Terjadi kesalahan saat menambahkan goal: {e}"
                elif last_message.lower().startswith('show goals'):
                    goals = storage.get_goals(user_id)
                    if goals:
                        response_text = "Daftar Goals:\n"
                        for g in goals:
                            response_text += f"- {g['name']}: Target Rp {g['target_amount']}, Saat ini Rp {g['current_amount']}\n"
                    else:
                        response_text = "Belum ada goal yang tercatat."
                else:
                    response_text = ai.generate_response(last_message)

                await loop.run_in_executor(executor, lambda: self.send_message(chat_title, response_text))
                logger.info(f"Sent response to {chat_title}: {response_text}")

            except Exception as e:
                logger.error(f"Error processing chat {chat}: {e}")

        while True:
            try:
                unread_chats = await loop.run_in_executor(executor, lambda: self.driver.find_elements(By.XPATH, '//span[@aria-label="Unread message"]'))
                tasks = [process_chat(chat) for chat in unread_chats]
                await asyncio.gather(*tasks)
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Error in listen_messages_async loop: {e}")
                await asyncio.sleep(5)

    def send_message(self, chat_title: str, message: str):
        logger.info(f"Sending message to {chat_title}: {message}")
        try:
            # Search for chat by title
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(chat_title)
            time.sleep(2)
            chat = self.driver.find_element(By.XPATH, f'//span[@title="{chat_title}"]')
            chat.click()
            time.sleep(2)

            # Find message input box
            input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            input_box.click()
            input_box.send_keys(message)
            time.sleep(1)

            # Click send button
            send_button = self.driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
            send_button.click()
            logger.info(f"Message sent to {chat_title}")
        except Exception as e:
            logger.error(f"Error sending message to {chat_title}: {e}")

    def stop(self):
        if self.driver:
            self.driver.quit()
            logger.info("WhatsApp Bot stopped.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WhatsApp Bot")
    parser.add_argument("chromedriver_path", help="Path to chromedriver executable")
    parser.add_argument("--user_data_dir", help="Path to Chrome user data directory for session persistence", default="./User_Data")

    args = parser.parse_args()

    bot = WhatsAppBot(args.chromedriver_path, args.user_data_dir)

    # Start the bot in a separate thread to avoid blocking
    def start_bot():
        bot.start()

    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    # Run the async listener in the main thread event loop
    asyncio.run(bot.listen_messages_async())
