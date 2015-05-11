from behave import given, when, then
from hamcrest import assert_that, string_contains_in_order
from hamcrest import greater_than_or_equal_to
from hamcrest import equal_to, contains, is_in, contains_string
from time import sleep
from PIL import Image

from bubble import paste_bubble
from bubble import paste_outline
from decorators import outline_elements_context, screenshot_context


@given(u'I access the main devpi page as "{user}"')
def step_impl(context, user):
    context.browser.get('http://127.0.0.1:3141')
    context.user = user


@when(u'I click My personal repository')
def step_impl(context):
    index = 'dev'
    full_index = '/'.join((context.user, index))
    link_to_repos = context.browser.find_element_by_xpath("//a[text()='{0}']".format(full_index))
    link_to_repos.click()


def dom_element_size(dom_element):
    x, y = dom_element.location['x'], dom_element.location['y']
    width, height = dom_element.size['width'], dom_element.size['height']
    return x, y, width, height


@then(u'I see my package list')
@outline_elements_context
def step_impl(context):
    package_list = context.browser.find_element_by_class_name('packages')
    packages = package_list.find_elements_by_xpath("//td/a")
    assert_that(len(packages), greater_than_or_equal_to(1))
    return [dom_element_size(packages[0]),dom_element_size(packages[1])]

@then(u'I have permission to upload packages')
@outline_elements_context
def step_impl(context):
    permissions = context.browser.find_element_by_class_name('permissions')

    my_permission = permissions.find_element_by_xpath(
        "descendant::span[contains(text(), '{0}')]".format(context.user))
    return [dom_element_size(my_permission)]


@then(u'I can see my "{index}" index')
@outline_elements_context
def step_impl(context, index):
    full_index = '/'.join((context.user, index))
    link_to_repos = context.browser.find_element_by_xpath("//a[text()='{0}']".format(full_index))
    assert_that(context.browser.page_source, string_contains_in_order(full_index))

    return [dom_element_size(link_to_repos)]

@then(u'I want to "{hilight}" this element')
@then(u'I want to "{hilight}" these elements')
@screenshot_context
def step_impl(context, hilight):
    outline_elements = getattr(context, 'outline_elements', [])
    if hilight == "outline":
        commented = paste_outline(context.current_screenshot,
                                  outline_elements)
    return commented

@then(u'I annotate this in the "{hotspot}" with')
@screenshot_context
def step_impl(context, hotspot):
    outline_elements = getattr(context, 'outline_elements', [])
    commented = paste_bubble(context.current_screenshot,
                             outline_elements,
                             hotspot,
                             context.text)
    return commented

    # context.browser.save_screenshot(filename)
    # import pdb; pdb.set_trace()

@then(u'I want a screenshot as "{filename}"')
@screenshot_context
def step_impl(context, filename):

    if isinstance(context.current_screenshot, Image.Image):
        context.current_screenshot.save(filename)
    else:
        with open(filename, 'wb') as fh:
            context.current_screenshot.seek(0)
            fh.write(context.current_screenshot.read())
