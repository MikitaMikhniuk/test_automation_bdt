from framework.elements.element_factory import ELEMENT_FACTORY, ElementType
from selenium.webdriver.common.by import By


class OnlinerHeader:

    CATALOG_TOP_BAR = '//a[contains(@class,"b-main-navigation__link")]/span[text()="{0}"]'

    def click_on_catalog_top_bar(self, section):
        catalog_top_bar = ELEMENT_FACTORY.get_element(
            ElementType.BUTTON, (By.XPATH, self.CATALOG_TOP_BAR.format(section)))
        catalog_top_bar.click()
