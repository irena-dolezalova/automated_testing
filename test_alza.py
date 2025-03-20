from playwright.sync_api import sync_playwright
import pytest


@pytest.fixture()
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)

        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    page.goto("https://www.alza.cz/")

    # rejecting of the cookies
    page.locator("body > div.js-cookies-info.cookies-info > div > div > div.cookies-info__buttons > a.cookies-info__button.cookies-info__button--link.js-cookies-info-reject").click()

    yield page
    page.close()


def test_count_items_displayed(page):
    """
    test tests the category mobiles
    applies filters (mobile brand, year of introduction (launched), internal memory size)
    after applying filters the total number of items offered (mobiles) is displayed
    verifies whether the calculated number of total items is the same as the number of items actually displayed on the page
    """

    # category Phones, Smart Watches & Tablets
    page.locator("#litp18890259").click()

    # category Mobile Phones
    page.locator("#ltp > div:nth-child(3) > div > div > div.catalogLocalTitlePage-alz-1 > div:nth-child(5) > a > span").click()

    # brand Samsung
    page.locator("#producer-1299 > div.valueInputContainer > label").check()

    # launched (year of the introduction)
    page.locator("#topped-value-24207-239995278 > div.valueInputContainer > label").check()

    # internal memory size
    page.locator("#topped-value-13175-239911162 > div.valueInputContainer > label").check()

    # results
    count_items = int(page.locator("#lblNumberItem").inner_text())
    count_items_displayed = page.locator("div.fb > a").count()

    assert count_items == count_items_displayed


def test_cart_items_names(page):
    """
    test tests the category smart rings
    uses the global search engine to search for "smart rings"
    applies a filter (smart rings, payment rings, cheapest, in stock)
    adds the first two items to the cart
    verifies that the correct items are in the shopping cart
    """

    # searched text "chytré prsteny"
    page.locator("#body3Inner > div.component.header > div > div.header-alz-4 > div > div > header > div.header-alz-11 > div > div.header-alz-120 > div > input").fill("chytré prsteny")

    # pressing Enter (searching)
    page.locator("#body3Inner > div.component.header > div > div.header-alz-4 > div > div > header > div.header-alz-11 > div > div.header-alz-120 > button.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.header-alz-133.header-alz-123.blue.btn-textLeft.btn-inline.header-1tqamc4").press("Enter")

    # category Smart Rings
    page.locator("#content0 > div.categoryPage.withLeftParametrization > div.mainContent > div.catlistContainer.subCatIncluded > div > div.subCategoriesCollapsed > div > ul:nth-child(1) > li > a").click()

    # category Payment Rings
    page.locator("#content0 > div.categoryPage.withLeftParametrization > div.mainContent > div.catlistContainer.subCatIncluded > div > div.category-tiles__categories.cz > a:nth-child(5)").click()

    # sorting (Price Low to High)
    page.locator("#blockFilterNoEmpty > div.sorting.js-sorting > ul > li:nth-child(3) > a.sorting__item-link.js-sort-item").click()

    # products in stock
    page.locator("#cpcm_cpc_parametrization_basicFilter_reactComponentCityBranchSelect > div > div:nth-child(1) > div.cityBranchSelect-alz-1 > fieldset > div > div:nth-child(2) > label > span.MuiButtonBase-root.MuiRadio-root.MuiRadio-colorPrimary.PrivateSwitchBase-root.MuiRadio-root.MuiRadio-colorPrimary.MuiRadio-root.MuiRadio-colorPrimary.city-branch-select-x6092y > input").click()

    
    item_names = []
    
    # first item
    first_item = page.locator("#boxes > div.box.browsingitem.js-box.canBuy.inStockAvailability.first.firstRow > div.top > div.fb > a").inner_text()

    # adding the name of the first item to the list "item_names"
    item_names.append(first_item)

    # adding the first item to the cart
    page.locator("#boxes > div.box.browsingitem.js-box.canBuy.inStockAvailability.first.firstRow > div.bottom > div.price > span > div > div > a").click()
    
    # second item
    second_item = page.locator("#boxes > div:nth-child(2) > div.top > div.fb > a").inner_text()

    # adding the name of the second item to the list "item_names"
    item_names.append(second_item)

    # adding the second item to the cart
    page.locator("#boxes > div:nth-child(2) > div.bottom > div.price > span > div > div > a").click()
    
    # shopping cart
    page.locator("#body3Inner > div.component.header > div > div.header-alz-4 > div > div > header > div.header-alz-19 > a").click()

    # results
    items_in_shopping_cart = page.locator("div.nameAndAccessoriesContainer").all()
      
    for index, item in enumerate(items_in_shopping_cart):
        assert item_names[index] in item.inner_text()



def test_change_language(page):
    """"
    test tests the change of the page language settings
    changes from Czech language (default value) to English language
    verifies that the change has occurred, i.e. after hovering the mouse over the language switcher icon, the text "Language: EN" will appear
    """
    
    # language switcher
    page.locator("#body3Inner > div.component.header > div > div.header-alz-4 > div > div > header > div.header-alz-18 > div.header-alz-21 > span > span").click()

    # changing the language
    page.locator("body > div.MuiDialog-root.header-alz-141.header-alz-137.header-alz-138.header-alz-139.header-alz-140.MuiModal-root.header-12i68ig > div.MuiDialog-container.MuiDialog-scrollPaper.header-ekeie0 > div > div > div:nth-child(2) > div > button:nth-child(2) > label > span.MuiButtonBase-root.MuiRadio-root.MuiRadio-colorPrimary.PrivateSwitchBase-root.MuiRadio-root.MuiRadio-colorPrimary.MuiRadio-root.MuiRadio-colorPrimary.header-x6092y > input").check()

    # confirmation of change 
    page.locator("body > div.MuiDialog-root.header-alz-141.header-alz-137.header-alz-138.header-alz-139.header-alz-140.MuiModal-root.header-12i68ig > div.MuiDialog-container.MuiDialog-scrollPaper.header-ekeie0 > div > div > div.header-alz-99 > button").click()

    # viewing tooltip (after hovering the mouse over the language switcher)
    page.locator("#body3Inner > div.component.header > div > div.header-alz-4 > div > div > header > div.header-alz-18 > div.header-alz-21 > span > span").hover()

    # result
    tooltip_text = page.locator('//*[@id=":R18piq:"]/div').inner_text()

    assert tooltip_text == 'Language: EN'
   
   