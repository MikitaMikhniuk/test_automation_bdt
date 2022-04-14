from framework.browser import BROWSER
from onliner.page_objects.main_page import MainPage
from onliner.page_objects.catalog_page import CatalogPage
from onliner.page_objects.result_page import ResultPage
from behave import *


@given(u'website "{url}"')
def step_impl(context, url):
    context.browser = BROWSER
    context.browser.maximize_window()
    context.browser.navigate(url)


@when(u'"{header}" page is opened')
def step_impl(context, header):
    context.main_page = MainPage()
    context.main_page.click_on_catalog_top_bar(header)

@step(u'navigate to "{menu}" -> "{submenu}" -> "{item}"')
def step_imp(context, menu, submenu, item):
    context.catalog_page = CatalogPage()
    context.catalog_page.navigate_to_menu(menu)
    context.catalog_page.navigate_to_submenu(submenu)
    context.catalog_page.click_on_submenu_item(item)

@then(u'apply following filters and verify results')
def step_impl(context):
    context.result_page = ResultPage()
    for row in context.table.rows:
        header = row[0]
        value = row[1]
        if header in ["vendor", "resolution"]:
            context.result_page.click_on_filter_checkbox(value)
        if header == "max_price":
            context.result_page.set_max_price(value)
        if header == "min_size":
            context.result_page.set_min_size(value)
        if header == "max_size":
            context.result_page.set_max_size(value)
    context.res = {row[0]: row[1] for row in context.table.rows}
    context.result_page.assert_headers(context.res["vendor"])
    context.result_page.assert_descriptions(
        context.res["resolution"], context.res["min_size"], context.res["max_size"])
    context.result_page.assert_prices(context.res["max_price"])
    context.browser.tear_down(context.browser.driver)
