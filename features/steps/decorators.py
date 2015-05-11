from functools import wraps
from cStringIO import StringIO
from PIL import Image


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
