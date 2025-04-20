from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    options = Options()
    options.add_argument("--user-data-dir=./User_Data")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")

    print("Please scan the QR code if not logged in.")
    # Wait for login by checking search box presence
    while True:
        try:
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            if search_box.is_displayed():
                print("Logged in successfully.")
                break
        except:
            pass
        time.sleep(2)

    # Check for unread message indicators
    unread_xpath = '//span[@aria-label="Unread message"]'
    unread_elements = driver.find_elements(By.XPATH, unread_xpath)
    print(f"Found {len(unread_elements)} unread message indicators with XPath: {unread_xpath}")

    # For each unread message, print chat title and last message text
    for idx, unread in enumerate(unread_elements):
        try:
            parent = unread.find_element(By.XPATH, './../../..')
            chat_title = parent.find_element(By.XPATH, './/span[@dir="auto"]').text
            print(f"Unread chat {idx+1}: {chat_title}")

            parent.click()
            time.sleep(2)

            messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]//span[@class="selectable-text copyable-text"]')
            if messages:
                last_message = messages[-1].text.strip()
                print(f"Last message in chat '{chat_title}': {last_message}")
            else:
                print(f"No incoming messages found in chat '{chat_title}'")
        except Exception as e:
            print(f"Error processing unread chat {idx+1}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
