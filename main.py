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

# Function to ask for duration using Tkinter
def ask_duration():
    ROOT = tk.Tk()
    ROOT.withdraw()
    # The input dialog
    USER_INP = simpledialog.askstring(title="Set Duration",
                                      prompt="Enter Duration in Seconds:")
    return int(USER_INP)  # Convert minutes to seconds

def safe_append_to_worksheet(worksheet, data, max_retries=100, delay=5):
    attempts = 0
    while True:
        try:
            worksheet.append_row(data)
            break  # Break the loop if successful
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}. Retrying...")
            time.sleep(delay)  # Wait for a while before retrying
            attempts += 1
    else:
        print("Failed to append data after several retries.")

def login_to_website(driver, username, password, login_url):
    while True:
        try:
            driver.get(login_url)
            time.sleep(2)

            # Find the username and password input fields and the submit button
            username_field = driver.find_element(By.ID, 'login_username')
            password_field = driver.find_element(By.ID, 'login_password')
            submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

            # Enter your login credentials
            username_field.send_keys(username)
            password_field.send_keys(password)

            # Submit the form
            submit_button.click()

            # Wait for the next page to load or for login to complete
            time.sleep(5)

            # Check if login was successful
            if "login" not in driver.current_url.lower():
                return True  # Successful login
            else:
                print("Login attempt failed. Retrying...")
                time.sleep(5)  # Wait before retrying

        except Exception as e:
            print(f"An error occurred during login: {e}")

    print("Failed to log in.")
    return False

# Set duration time
duration = ask_duration()

# Load environment variables from the .env file
dotenv.load_dotenv()

# Load Google Sheets credentials from environment variable
google_credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
if not google_credentials_path:
    raise ValueError("The Google Sheets credentials path is not set in the environment variables")

# Set the scope and credentials for Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet by title
sheet_url = "https://docs.google.com/spreadsheets/d/1r_96ut4UIoDEkSYQqyaSCNKppQwR7VyXZPn-lWOKcvI/edit?usp=sharing"
spreadsheet = client.open_by_url(sheet_url)

# Get the worksheet by name
worksheet_name = "Sheet1"
worksheet = spreadsheet.get_worksheet(0)

# If the worksheet is not found, create a new one
if worksheet is None:
    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

# Define the header names
header_names = ["Data Time", "Huay 264", "Huay VIP 264", "LTO 264", "LTO VIP 264 ", "ชัดเจน 264", "ชัดเจน VIP 264"]
total_data = [header_names]

# Check if the worksheet is empty (no header row) and add headers if needed
existing_headers = worksheet.row_values(1)
if not existing_headers:
    worksheet.insert_row(header_names, index=1)

# Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# URL of the login page
login_url = 'https://dnabet.vip/login'

# Your login credentials
username = 'Gargoyle007'
password = 'Gg123456'

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options)

# Login to the website
if not login_to_website(driver, username, password, login_url):
    print("Exiting due to login failure.")
    driver.quit()
    exit()

# Main loop for data extraction
while True:
    try:
        # Navigate to the data URL
        driver.get("https://dnabet.vip/lotto/result")
        time.sleep(10)

        # Wait for the page to load and for a specific element to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-container')))

        # Extract the data
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_elements = soup.find_all('div', class_='sc-9e723fdc-0 krDVwH undefined card border-gradient !lg:p-[20px] !p-[10px]')
        order = [8, 9, 16, 17, 12, 13]
        data = []
        data_com = []
        current_datetime = datetime.now()

        # Format the date and time as YYYY-MM-DD HH:MM
        data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        data.append(data_time)

        for item in order:
            # Check if the index 'item' is within the range of 'div_elements'
            if item < len(div_elements):
                div_element = div_elements[item]
                span_element = div_element.find('span', class_='ant-typography text-[0.85rem] lg:text-[1rem]')
                divs_font_numeral = div_element.find_all('strong')

                # Check if the necessary elements are found
                if span_element and len(divs_font_numeral) >= 2:
                    value_1 = span_element.get_text().split(" ")[-1]
                    value_2 = divs_font_numeral[3].get_text()
                    value_3 = divs_font_numeral[4].get_text()

                    data.append(value_1)
                    data.append(value_2)
                    data.append(value_3)
                    data_com.append(value_1)
                    data_com.append(value_2)
                    data_com.append(value_3)
                else:
                    print(f"Required elements not found for item at index {item}.")
            else:
                print(f"Index {item} is out of range for 'div_elements'.")

        print(data)
        try:
            if data_com != total_data[-1] and len(data) >= 19:
                total_data.append(data_com)
                safe_append_to_worksheet(worksheet, data)
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for the specified duration before repeating
        time.sleep(duration)

    except Exception as e:
        print(f"An error occurred: {e}")

        # Attempt to log in again if an error occurs
        if not login_to_website(driver, username, password, login_url):
            print("Exiting due to login failure.")
            break

        # Wait for a while before retrying
        time.sleep(10)
