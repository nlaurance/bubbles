from functools import wraps
from io import StringIO
from PIL import Image

from behave import then

from .bubble import paste_bubble
from .bubble import paste_outline


def outline_elements_context(step):
    """ context.outline_elements is a list of
    x, y, width, height returned by dom_element_size
    keeping tracks of the parts of interest in the UI
    """
    @wraps(step)
    def wrapper(context, *args, **kwargs):
        outline_elements = getattr(context, 'outline_elements', [])
        new_elements = step(context, *args, **kwargs)
        outline_elements.extend(new_elements)
        context.outline_elements = outline_elements
        return new_elements
    return wrapper


def screenshot_context(step):
    """ context.current_screenshot keep tracks of the screenshot
    between steps
    """
    @wraps(step)
    def wrapper(context, *args, **kwargs):
        screenshot = getattr(context, 'current_screenshot',
                             Image.open(StringIO(context.browser.get_screenshot_as_png())))
        context.current_screenshot = screenshot

        updated_screenshot = step(context, *args, **kwargs)
        context.current_screenshot = updated_screenshot
        return updated_screenshot
    return wrapper


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


@then(u'I want a screenshot as "{filename}"')
@screenshot_context
def step_impl(context, filename):

    if isinstance(context.current_screenshot, Image.Image):
        context.current_screenshot.save(filename)
    else:
        with open(filename, 'wb') as fh:
            context.current_screenshot.seek(0)
            fh.write(context.current_screenshot.read())
