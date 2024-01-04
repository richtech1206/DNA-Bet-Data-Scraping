import os
import requests
import dotenv
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to ask for duration using Tkinter
def ask_duration():
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title="Set Duration", prompt="Enter Duration in Seconds:")
    return int(USER_INP)

def safe_append_to_worksheet(worksheet, data, max_retries=5, delay=5):
    for _ in range(max_retries):
        try:
            worksheet.append_row(data)
            return
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying...")
            time.sleep(delay)
    print("Failed to append data after retries.")

def login_to_website(driver, username, password, login_url):
    for _ in range(3):
        try:
            driver.get(login_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_username')))
            username_field = driver.find_element(By.ID, 'login_username')
            password_field = driver.find_element(By.ID, 'login_password')
            submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

            username_field.send_keys(username)
            password_field.send_keys(password)
            submit_button.click()

            WebDriverWait(driver, 10).until(EC.url_changes(login_url))
            if "login" not in driver.current_url.lower():
                return True
            time.sleep(10)
        except TimeoutException as e:
            print(f"Login timeout: {e}. Retrying...")
        except Exception as e:
            print(f"Login error: {e}")
    return False

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path='chromedriver.exe')
    return webdriver.Chrome(service=service, options=chrome_options)

def main():
    total_data = [["Data Time", "Huay 264", "Huay VIP 264", "LTO 264", "LTO VIP 264", "ชัดเจน 264", "ชัดเจน VIP 264"]]
    duration = ask_duration()
    dotenv.load_dotenv()
    google_credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    if not google_credentials_path:
        raise ValueError("Google Sheets credentials path is not set.")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
    client = gspread.authorize(creds)

    sheet_url = "https://docs.google.com/spreadsheets/d/1r_96ut4UIoDEkSYQqyaSCNKppQwR7VyXZPn-lWOKcvI/edit?usp=sharing"
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.get_worksheet(0) or spreadsheet.add_worksheet(title="Sheet1", rows="100", cols="20")

    header_names = ["Data Time", "Huay 264", "Huay VIP 264", "LTO 264", "LTO VIP 264", "ชัดเจน 264", "ชัดเจน VIP 264"]
    if not worksheet.row_values(1):
        worksheet.insert_row(header_names, index=1)

    driver = init_driver()
    login_url = 'https://dnabet.vip/login'
    username = 'Gargoyle007'
    password = 'Gg123456'

    if not login_to_website(driver, username, password, login_url):
        print("Login failure.")
        driver.quit()
        return

    while True:
        try:
            driver.get("https://dnabet.vip/lotto/result")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-container')))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            div_elements = soup.find_all('div', class_='sc-9e723fdc-0 krDVwH undefined card border-gradient !lg:p-[20px] !p-[10px]')
            order = [8, 9, 16, 17, 12, 13]
            data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            data_com = []   
            for item in order:
                if item < len(div_elements):
                    div_element = div_elements[item]
                    span_element = div_element.find('span', class_='ant-typography text-[0.85rem] lg:text-[1rem]')
                    divs_font_numeral = div_element.find_all('strong')
                    if span_element and len(divs_font_numeral) >= 2:
                        data.extend([span_element.get_text().split(" ")[-1], divs_font_numeral[3].get_text(), divs_font_numeral[4].get_text()])
                        data_com.extend([span_element.get_text().split(" ")[-1], divs_font_numeral[3].get_text(), divs_font_numeral[4].get_text()])
            if len(data) >= 19 and data_com != total_data[-1]:
                total_data.append(data_com)
                safe_append_to_worksheet(worksheet, data)
            print(data)            

            time.sleep(duration)
        except TimeoutException as e:
            print(f"Timeout error: {e}. Attempting re-login.")
            while not login_to_website(driver, username, password, login_url):
                print("Re-login failed. Retrying...")
                time.sleep(10)  # Waiting before retrying
        except Exception as e:
            print(f"Error: {e}. Attempting re-login.")
            while not login_to_website(driver, username, password, login_url):
                print("Re-login failed. Retrying...")
                time.sleep(10)  # Waiting before retrying

    driver.quit()

if __name__ == "__main__":
    main()