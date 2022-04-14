
from selenium.webdriver.common.by import By
from framework.base_page import BasePage
from framework.elements.element_factory import ELEMENT_FACTORY, ElementType


class ResultPage(BasePage):

    def __init__(self):
        super().__init__(self.HEADER, "Телевизоры")

    HEADER = (
        By.XPATH, "//h1[@class='schema-header__title js-schema-header_title']")
    FILTER_CHECKBOX = '//span[@class="schema-filter__checkbox-text" and text()="{0}"]'
    LOADING_ANIM = (
        By.XPATH, "//div[contains(@class,'schema-filter-button__state_animated')]")
    MIN_PRICE_INPUT = (
        By.XPATH, '//input[contains(@class,"schema-filter-control__item schema-filter__number-input schema-filter__number-input_price") and @placeholder="от"]')
    MAX_PRICE_INPUT = (
        By.XPATH, '//input[contains(@class,"schema-filter-control__item schema-filter__number-input schema-filter__number-input_price") and @placeholder="до"]')
    MIN_SIZE_INPUT = (
        By.XPATH, '//select[contains(@class,"schema-filter-control__item")]')
    MIN_SIZE_VALUE_OPTION = '//div[contains(@class,"schema-filter-control schema-filter-control_select")]//option[@value="{0}"]'
    MAX_SIZE_INPUT = (
        By.XPATH, '//div[contains(@class,"schema-filter-control schema-filter-control_select")]/following-sibling::div/select')
    MAX_SIZE_VALUE_OPTION = '//div[contains(@class,"schema-filter-control schema-filter-control_select")]/following-sibling::div/select//option[@value="VALUE"]'
    ITEM_HEADERS = (
        By.XPATH, '//span[contains(@data-bind,"html: product.extended_name || product.full_name")]')
    ITEM_DESCRIPTIONS = (
        By.XPATH, '//span[contains(@data-bind,"html: product.description")]')
    ITEM_PRICES = '//span[@data-bind="html: $root.format.minPrice($data.prices, {0}BYN{0})"]'

    def wait_for_filter_results(self):
        try:
            element = ELEMENT_FACTORY.get_element(
                ElementType.CONTAINER, self.LOADING_ANIM, timeout=1)
            if element:
                element.wait_for_element_stale()
        except:
            return

    def click_on_filter_checkbox(self, keyword):
        filter_checkbox = ELEMENT_FACTORY.get_element(
            ElementType.CHECKBOX, (By.XPATH, self.FILTER_CHECKBOX.format(keyword)))
        filter_checkbox.scroll_to_element()
        filter_checkbox.move_cursor_to_element()
        filter_checkbox.click()
        self.wait_for_filter_results()

    def set_min_price(self, min_price):
        min_price_input = ELEMENT_FACTORY.get_element(
            ElementType.TEXTBOX, self.MIN_PRICE_INPUT)
        min_price_input.move_cursor_to_element()
        min_price_input.click()
        min_price_input.send_keys(min_price)
        self.wait_for_filter_results()

    def set_max_price(self, max_price):
        max_price_input = ELEMENT_FACTORY.get_element(
            ElementType.TEXTBOX, self.MAX_PRICE_INPUT)
        max_price_input.move_cursor_to_element()
        max_price_input.click()
        max_price_input.send_keys(max_price)
        self.wait_for_filter_results()

    def set_min_size(self, value):
        min_size_input = ELEMENT_FACTORY.get_element(
            ElementType.DROPDOWN, self.MIN_SIZE_INPUT)
        min_size_input.scroll_to_element()
        min_size_input.click()
        min_size_input.select_by_dropdown_value(value)
        self.wait_for_filter_results()

    def set_max_size(self, value):
        max_size_input = ELEMENT_FACTORY.get_element(
            ElementType.DROPDOWN, self.MAX_SIZE_INPUT)
        max_size_input.scroll_to_element()
        max_size_input.click()
        max_size_input.select_by_dropdown_value(value)
        self.wait_for_filter_results()

    def assert_headers(self, vendor):
        self.wait_for_filter_results()
        item_headers = ELEMENT_FACTORY.get_elements(
            ElementType.LABEL, self.ITEM_HEADERS)
        for item_header in item_headers:
            assert vendor in item_header.get_text()

    def assert_descriptions(self, resolution, min_size, max_size):
        item_descriptions = ELEMENT_FACTORY.get_elements(
            ElementType.LABEL, self.ITEM_DESCRIPTIONS)
        for item_description in item_descriptions:
            description_text = item_description.get_text()
            assert resolution in description_text
            description_list = description_text.split()
            size = description_list[0]
            assert (float(min_size)) / \
                10 <= float(size.replace('"', '')) <= (float(max_size))/10

    def assert_prices(self, max_price):
        item_prices = ELEMENT_FACTORY.get_elements(
            ElementType.LABEL, (By.XPATH, self.ITEM_PRICES.format("'")))
        for item_price in item_prices:
            price = item_price.get_text()
            pure_value = price.replace(' р.', '')
            value = pure_value.replace(",", ".")
            assert int(float(value)) <= int(max_price)
