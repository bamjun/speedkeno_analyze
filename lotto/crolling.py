import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no browser UI)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the page to scrape
url = 'https://dhlottery.co.kr/gameInfo.do?method=kenoWinNoList'

# Function to scrape data from each page
def scrape_page(page_number):
    try:
        # Navigate to the page using selfSubmit(page_number)
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[onclick="selfSubmit({page_number})"]'))
        ).click()
        
        # Allow time for the page to load
        time.sleep(2)

        # Get the page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table and rows with class "tbl_data tbl_data_col"
        table = soup.find('table', class_='tbl_data tbl_data_col')
        rows = table.find('tbody').find_all('tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            draw_date = cols[0].text.strip()
            draw_number = int(cols[1].text.strip())
            numbers = [int(num) for num in cols[2].text.strip().split(',')]
            additional_info = cols[3].text.strip()

            data.append({
                'draw_date': draw_date,
                'draw_number': draw_number,
                'numbers': numbers,
                'additional_info': additional_info
            })

        return data

    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")
        return []

# Scrape data from all pages
all_data = []
for page in range(1, 23):
    print(f"Scraping page {page}...")
    page_data = scrape_page(page)
    all_data.extend(page_data)

# Close the driver
driver.quit()

# Save the data to a JSON file
with open('wins.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Data scraping completed and saved to wins.json.")
