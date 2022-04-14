from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.browser import BROWSER
from framework.utils import json_reader

CONFIG_PATH = "onliner\\resources\\factory_config.json"
config = json_reader.get_json(CONFIG_PATH)


class BaseElement:

    timeout = config["DEFAULT_WAIT_TIME"]

    def __init__(self, driver, element):
        self.driver = driver
        self.element = element
        self.wait = WebDriverWait(self.driver, self.timeout)

    def click(self):
        self.wait.until(EC.element_to_be_clickable(self.element))
        self.element.click()

    def click_and_wait(self):
        self.click()
        self.wait.until(EC.staleness_of(self.element))
        try:
            assert BROWSER.get_document_state() == "complete"
        except AssertionError:
            print("Page was not loaded after click event")

    def scroll_to_element(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element)

    def move_cursor_to_element(self):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.element)

    def get_text(self):
        return self.element.text

    def get_attribute(self, attribute):
        return self.element.get_attribute(attribute)

    def wait_for_element_stale(self):
        self.wait.until(EC.staleness_of(self.element.element))
