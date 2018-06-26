import time
import selenium
from selenium import webdriver

chrome = None
def main():
    """
    Main function, creates the Chrome instance and visits the necessary websites
    to collect data
    """
    # Setup options: Select the profile version to use, and load the extension
    # into Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("""user-data-dir=/Users/Development/Library/
        Application Support/Google/Chrome/Default""")
    options.add_argument("--load-extension=../test-extension/build")

    # Create a Chrome instance and open up a website
    chrome = webdriver.Chrome(chrome_options=options)
    chrome.get('https://brainly.com/question/10546818')

    # Wait for an adequate amount of time for the data to get collected
    time.sleep(2)

    # Quit the browser
    chrome.quit()

if __name__ == "__main__":
    try:
        main()
    except selenium.common.exceptions.WebDriverException as exception:
        # In the event that an error occurs, we still want to quit
        # Chrome, otherwise a chromdriver instance will keep running
        if chrome:
            chrome.quit()
            