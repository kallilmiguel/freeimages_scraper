
import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import insert_image_url

# Set up argument parsing
def parse_arguments():

    parser = argparse.ArgumentParser(description='Scrape images and store in SQLite database.')
    parser.add_argument('--search_term', type=str, default='dog', help='Search term for images')
    parser.add_argument('--db_path', type=str, default='./db/images.db', help='Path to SQLite database')
    parser.add_argument('--n_images', type=int, default=1000, help='Number of images to be saved')
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    args = parse_arguments()

    # Use args to access command-line arguments
    search_term = args.search_term
    db_path = args.db_path

    # Initialize Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    freeimages_url = "https://www.freeimages.com"
    # Navigate to the website
    driver.get(freeimages_url)
    original_window = driver.current_window_handle
    page_number = 1

    search_input = driver.find_element(By.ID, "search-input")
    search_input.clear()
    search_input.click()
    search_input.send_keys(search_term)

    search_button = driver.find_element(By.ID, "search-submit-button")
    search_button.click()

    driver.switch_to.window(original_window)

    urls = []
    while(len(urls) < args.n_images):
        try:
            grid_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "grid-container"))
            )
            photo_elements = grid_element.find_elements(By.CLASS_NAME, "grid-item")

            # Filter elements to ensure they only have "grid-item" as their class, this is to avoid iStock ads, for example
            for photo_element in photo_elements:
                if photo_element.get_attribute("class") == "grid-item" and len(urls) < args.n_images:
                    url = photo_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if url not in urls:  # Check to avoid duplicates
                        urls.append(url)
                        insert_image_url(db_path=db_path, url=url)


            page_number+=1
            
            driver.get(f"{freeimages_url}/search/{search_term}/{page_number}")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error navigating to page {page_number}: {e}")
            break  # Exit the loop if an error occurs


# %%
