import time
import selenium
from enum import Enum
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class CssSelectors(Enum):
    StackExchange = { "question": "", "pagination": "" }
    OldReddit = { "question": "", "pagination": "" }
    Answers = { "question": "", "pagination": "" }
    Brainly = { 
        "question": "div.sg-content-box__content > a", 
        "pagination": "div:nth-child(12) > span > div > svg" 
    }

def visit_all(
        driver, 
        base_url, 
        links_start=0,
        links_end=None,
        selector=CssSelectors.StackExchange, 
        query=None
    ):
    """
    Visits all links on a Brainly search page by opening each in a new tab,
    pausing for the extension to collect data, and returning to the main
    window to open the next link
    """
    request_url = base_url.format(query) if query else base_url
    driver.get(request_url)
    time.sleep(3)
    body = driver.find_element_by_tag_name('body')

    for _ in range(5):        
        links = body.find_elements_by_css_selector(selector.value["question"])
        links = links[links_start:links_end]
        print(len(links))

        for link in links:
            # Create an action chain to open the link in a new tab
            actions = ActionChains(driver)
            actions.move_to_element(link).perform()
            body.send_keys(Keys.PAGE_UP)
            time.sleep(1)
            actions.key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()

            # Switch to the new tab containing the Q/A and wait for
            # the extension to collect its data
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)

            # Close the Q/A tab
            driver.close()

            # Even though closing the previous tab returns us to the main
            # search tab, it is necessary to explicitly switch the context
            # back to the main tab for the links to work.
            driver.switch_to.window(driver.window_handles[0])

        paginator = driver.find_element_by_css_selector(selector.value["pagination"])
        actions = ActionChains(driver)
        actions.move_to_element(paginator).perform()
        time.sleep(1)
        actions.click(paginator).perform()
        time.sleep(3)


def init():
    """
    Main function, creates the driver instance and visits the necessary websites
    to collect data
    """
    # Setup options: Select the profile version to use, and load the extension
    # into driver
    options = webdriver.ChromeOptions()
    options.add_argument("--load-extension=../../../cq-frontends/cq-extension/build")

    # Create a driver instance and open up a website
    driver = webdriver.Chrome(options=options)
    return driver


if __name__ == "__main__":
    try:
        DRIVER = init()
        visit_all(
            DRIVER, 
            "https://brainly.com/app/ask?entry=top&q={}", 
            links_end=-1,
            selector=CssSelectors.Brainly,
            query="government"
        )

        DRIVER.quit()

    except selenium.common.exceptions.WebDriverException as error:
        # In the event that an error occurs, we still want to quit
        # driver, otherwise a chromedriver instance will keep running
        DRIVER.quit()

        raise error
