from behave import when, then
from selenium.webdriver.common.by import By

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.BASE_URL)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = context.driver.find_element(By.ID, 'search_results')
    assert name in found.text

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = context.driver.find_element(By.ID, 'flash_message')
    assert message in found.text
