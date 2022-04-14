from framework.elements.base_element import BaseElement
from selenium.webdriver.support import expected_conditions as EC


class TextBox(BaseElement):
    def __init__(self, driver, element):
        super().__init__(driver, element)

    def send_keys(self, keys):
        self.wait.until(EC.element_to_be_clickable(self.element))
        self.element.send_keys(keys)
