import time
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

QUESTION_LINK_SELECTOR = "//*[@id=\"search-results\"]/div[1]/div[2]/div[2]/div/article/div[1]/a/div/div/div"
PAGINATION_LINK_SELECTOR = "//*[@id=\"search-results\"]/div[1]/div[2]/div[3]/div/span"
QUERIES = [
    "government",
    "politics",
    "president",
    "food",
    "engineering",
    "design",
    "fashion",
    "house",
    "finance",
    "stock market",
    "economy",
    "social media",
    "health",
    "python",
    "java",
    "robotics",
    "Android",
    "Oedipus",
    "poem",
    "water",
    "fire",
    "earth",
    "air",
    "cell",
    "india",
    "united kingdom",
    "united states",
    "china"
    # "american history",
    # "pop culture",
    # "biology",
    # "physics",
    # "chemistry",
    # "anthropology",
    # "literature",
    # "grapes of wrath",
    # "great gatsby",
    # "calculus",
    # "plants",
    # "life",
    # "slavery",
    # "civil war",
    # "revolutionary war",
    # "anatomy",
    # "medicine",
    # "astronomy",
    # "college",
    # "heart",
    # "liver",
    # "electromagnetism",
    # "mechanics",
    # "rubik's cube",
]


def visit_all(driver, site):
    """
    Visits all links on a Brainly search page by opening each in a new tab,
    pausing for the extension to collect data, and returning to the main
    window to open the next link
    """
    base_url = "https://brainly.com/app/ask?entry=top&q={}".format(site)
    driver.get(base_url)
    time.sleep(3)

    pages = driver.find_elements_by_xpath(PAGINATION_LINK_SELECTOR)
    pages = pages[1:]
    body = driver.find_element_by_tag_name('body')

    for page_link in pages:
        try:
            if page_link.text == '':
                continue

            actions = ActionChains(driver)
            actions.move_to_element(page_link).perform()
            time.sleep(1)
            actions.click(page_link).perform()
            time.sleep(3)
            links = body.find_elements_by_xpath(QUESTION_LINK_SELECTOR)

            for link in links:
                try:
                    # Create an action chain to open the link in a new tab
                    actions = ActionChains(driver)
                    actions.move_to_element(link).perform()
                    body.send_keys(Keys.PAGE_UP)
                    time.sleep(1)
                    actions.key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()

                    # Switch to the new tab containing the Q/A and wait for
                    # the extension to collect its data
                    driver.switch_to_window(driver.window_handles[-1])
                    time.sleep(3)

                    # Close the Q/A tab
                    driver.close()

                    # Even though closing the previous tab returns us to the main
                    # search tab, it is necessary to explicitly switch the context
                    # back to the main tab for the links to work.
                    driver.switch_to_window(driver.window_handles[0])

                except Exception:
                    driver.switch_to_window(driver.window_handles[0])

        except Exception:
            driver.switch_to_window(driver.window_handles[0])


def init():
    """
    Main function, creates the driver instance and visits the necessary websites
    to collect data
    """
    # Setup options: Select the profile version to use, and load the extension
    # into driver
    options = webdriver.ChromeOptions()
    options.add_argument("""user-data-dir=/Users/Development/Library/
        Application Support/Google/driver/Default""")
    options.add_argument("--load-extension=../../test-extension/build")

    # Create a driver instance and open up a website
    driver = webdriver.Chrome(chrome_options=options)
    return driver


if __name__ == "__main__":
    try:
        DRIVER = init()
        for query in QUERIES:
            visit_all(DRIVER, query)

        DRIVER.quit()

    except selenium.common.exceptions.WebDriverException as error:
        # In the event that an error occurs, we still want to quit
        # driver, otherwise a chromedriver instance will keep running
        DRIVER.quit()

        raise error
