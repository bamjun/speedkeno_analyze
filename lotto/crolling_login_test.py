import configparser
import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

config = configparser.ConfigParser()
config.read("config.ini")

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no browser UI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--incognito")  # Enable incognito mode


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# URL of the page to scrape
url = "https://dhlottery.co.kr/gameInfo.do?method=kenoWinNoList"


# Credentials
username = config["lotto"]["id"]
password = config["lotto"]["password"]


# Function to log into the website
def login(driver):
    # Open the login page
    driver.get(url)

    # Wait for the login elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userId")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    # Enter username and password
    user_id_input = driver.find_element(By.ID, "userId")
    password_input = driver.find_element(By.NAME, "password")

    user_id_input.send_keys(username)
    password_input.send_keys(password)

    # Press Enter to submit the login form
    password_input.send_keys(Keys.RETURN)

    # # Wait for the login process to complete
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.tbl_data.tbl_data_col')))

    print("Login successful.")


# Function to scrape data from each page
def scrape_page(page_number):
    try:

        # Navigate to the page using selfSubmit(page_number)
        driver.get(url)

        calendar_input = driver.find_element(By.ID, "calendar")

        # Use JavaScript to set the value
        driver.execute_script("arguments[0].value = '2024-08-04';", calendar_input)

        driver.execute_script(f"selfSubmit('{page_number}');")

        # Allow time for the page to load
        time.sleep(2)

        # Get the page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the table and rows with class "tbl_data tbl_data_col"
        table = soup.find("table", class_="tbl_data tbl_data_col")
        rows = table.find("tbody").find_all("tr")

        data = []
        for row in rows:
            cols = row.find_all("td")
            draw_date = cols[0].text.strip()
            draw_number = int(cols[1].text.strip())
            numbers = [int(num) for num in cols[2].text.strip().split(",")]
            additional_info = cols[3].text.strip()

            data.append(
                {
                    "draw_date": draw_date,
                    "draw_number": draw_number,
                    "numbers": numbers,
                    "additional_info": additional_info,
                }
            )

        return data

    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")
        return []


# Log into the website
login(driver)


# Scrape data from all pages
all_data = []
for page in range(1, 23):
    print(f"Scraping page {page}...")
    page_data = scrape_page(page)
    all_data.extend(page_data)

# Close the driver
driver.quit()

# Save the data to a JSON file
with open("wins.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Data scraping completed and saved to wins.json.")
