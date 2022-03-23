from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from framework.base.base_page import BasePage
from framework.base.base_element import BaseElement
from framework.utils import waiter

class ResultPage(BasePage, BaseElement):
    
    def __init__(self, driver):
        super().__init__(driver)

    FILTER_CHECKBOX = '//span[@class="schema-filter__checkbox-text" and text()="keyword"]'
    LOADING_ANIM = (By.XPATH, '//div[@class="schema-products schema-products_processing"]')
    MIN_PRICE_INPUT = '//input[contains(@class,"schema-filter-control__item schema-filter__number-input schema-filter__number-input_price") and @placeholder="от"]'
    MAX_PRICE_INPUT = '//input[contains(@class,"schema-filter-control__item schema-filter__number-input schema-filter__number-input_price") and @placeholder="до"]'
    SCHEMA_PROD = (By.XPATH, '//div[@class="schema-products"]')
    MIN_SIZE_INPUT = '//select[contains(@class,"schema-filter-control__item")]'
    MIN_SIZE_VALUE_OPTION = '//div[contains(@class,"schema-filter-control schema-filter-control_select")]//option[@value="VALUE"]'
    MAX_SIZE_INPUT = '//div[contains(@class,"schema-filter-control schema-filter-control_select")]/following-sibling::div/select'
    MAX_SIZE_VALUE_OPTION = '//div[contains(@class,"schema-filter-control schema-filter-control_select")]/following-sibling::div/select//option[@value="VALUE"]'
    ITEM_HEADERS = '//span[contains(@data-bind,"html: product.extended_name || product.full_name")]'
    ITEM_DESCRIPTIONS = '//span[contains(@data-bind,"html: product.description")]'
    ITEM_PRICES = '//span[@data-bind="html: $root.format.minPrice($data.prices, ''BYN'')"]'
    RESULT_PAGE_TITLE = '//h1[contains(@class,"schema-header__title")]'

    def wait_for_filter_results(self):
        wait_until_not = waiter.UntilNot(self.driver)
        wait_until_not.presence_of_element_located(self.LOADING_ANIM)

    def click_on_filter_checkbox(self, keyword):
        filter_checkbox = self.find_element_by_xpath(self.get_locator_with_replaced_xpath(self.FILTER_CHECKBOX, "keyword", keyword))
        self.scroll_element_into_view(filter_checkbox)
        self.move_to_element(filter_checkbox)
        self.click_on_element(filter_checkbox)
        self.wait_for_filter_results()
        return filter_checkbox
    
    def set_min_price(self, min_price):
        min_price_input = self.find_element_by_xpath(self.MIN_PRICE_INPUT)
        self.move_to_element(min_price_input)
        self.click_on_element(min_price_input)
        self.send_keys(min_price_input, min_price)
        self.wait_for_filter_results()
        return min_price_input

    def set_max_price(self, max_price):
        max_price_input = self.find_element_by_xpath(self.MAX_PRICE_INPUT)
        self.move_to_element(max_price_input)
        self.click_on_element(max_price_input)
        self.send_keys(max_price_input, max_price)
        wait_until = waiter.Until(self.driver)
        wait_until.presence_of_element_located(self.SCHEMA_PROD)
        return max_price_input
    
    def set_min_size(self, value):
        min_size_input = self.find_element_by_xpath(self.MIN_SIZE_INPUT)
        self.click_on_element(min_size_input)
        element = (By.XPATH, self.get_locator_with_replaced_xpath(self.MIN_SIZE_VALUE_OPTION, "VALUE", value))
        wait_until = waiter.Until(self.driver)
        wait_until.visibility_of_element_located(element)
        self.select_by_dropdown_value(min_size_input, value)
        self.wait_for_filter_results()
        return min_size_input

    def set_max_size(self, value):
        max_size_input = self.find_element_by_xpath(self.MAX_SIZE_INPUT)
        self.click_on_element(max_size_input)
        self.select_by_dropdown_value(max_size_input, value)
        element = (By.XPATH, self.get_locator_with_replaced_xpath(self.MAX_SIZE_VALUE_OPTION, "VALUE", value))
        wait_until = waiter.Until(self.driver)
        wait_until.visibility_of_element_located(element)
        self.click_on_element(max_size_input)
        self.wait_for_filter_results()
        return max_size_input

    def find_item_headers(self):
        self.wait_for_filter_results()
        item_headers = self.find_elements_by_xpath(self.ITEM_HEADERS)
        return item_headers

    def find_item_descriptions(self):
        item_descriptions = self.find_elements_by_xpath(self.ITEM_DESCRIPTIONS)
        return item_descriptions

    def find_item_prices(self):
        item_prices = self.find_elements_by_xpath(self.ITEM_PRICES)
        return item_prices

    def verify_result_page_by_header(self, header):
        result_page_header = self.find_element_by_xpath(self.RESULT_PAGE_TITLE)    
        assert result_page_header.text == header


    def assert_headers(self, vendor):
        for item_header in self.find_item_headers():
            assert vendor in item_header.text
    
    def assert_descriptions(self, resolution, min_size, max_size):
        for item_description in self.find_item_descriptions():
            assert resolution in item_description.text
            description_list = item_description.text.split()
            size = description_list[0]
            assert (float(min_size))/10 <= float(size.replace('"', '')) <= (float(max_size))/10

    def assert_prices(self, max_price):
        for item_price in self.find_item_prices():
            price = item_price.text.replace('\u00A0р.', '')
            assert int(price) <= int(max_price)
