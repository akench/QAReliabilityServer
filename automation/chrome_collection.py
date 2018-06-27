import time
import selenium
from selenium import webdriver

LINK_SELECTOR = "#search-results > div.sg-layout__content > \
    div.sg-content-box.search-results.stream-container.sg-layout__box > \
    div.sg-content-box__content.sg-content-box__content--spaced-bottom-large.search-results__items.js-search-items > \
    div > article > div.sg-content-box__content > a > div > div > div"
QUERIES = [
    "history"
]

def visit_all(chrome, site):
    base_url = "https://brainly.com/app/ask?entry=top&q={}".format(site)
    chrome.get(base_url)
    links = chrome.find_elements_by_css_selector(LINK_SELECTOR)

    for link in links:
        link.click()
        time.sleep(2)
        chrome.execute_script("window.history.go(-1)")

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

    for query in QUERIES:
        visit_all(chrome, query)

chrome = None
if __name__ == "__main__":
    try:
        main()
    except selenium.common.exceptions.WebDriverException as error:
        # In the event that an error occurs, we still want to quit
        # Chrome, otherwise a chromdriver instance will keep running
        if chrome:
            chrome.quit()
            