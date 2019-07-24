from PIL import Image, ImageDraw, ImageFont
from ninepatch import Ninepatch

DEBUG = False


def text2img(text, main_text_start=(0,0), fg='black', bg=None,
             font_ttf="/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
             font_size=20):
    """ Creates an image rendering the given text

    :param text: the multiline string to show
    :param main_text_start: would allow a left and top margin
    :param fg: font color
    :param bg: background color, default to transparent
    :param font_ttf: full path a a TTF Font file
    :param font_size: in point
    :return: A PIL image with the text rendered
    """
    image = Image.new('RGBA', (2048, 2048), bg)
    drawer = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_ttf, font_size)
    # worst case x_offset and y_offset
    x_offset, y_offset = font.getoffset('/Pj')
    _, height = drawer.textsize('Pj', font=font)

    text_start = main_text_start
    main_text_end = main_text_start

    for text_line in text.split('\n'):
        # drawing text
        drawer.text(text_start, text_line, fill=fg, font=font)
        # sizing
        width, _ = drawer.textsize(text_line, font=font)
        # update line bounding box
        text_start = tuple(map(sum, zip(text_start, (x_offset, height))))
        text_end = tuple(map(sum, zip(text_start, (width, 0))))
        # update main bounding box
        main_text_start = tuple(map(min, zip(main_text_start, text_start)))
        main_text_end = tuple(map(max, zip(main_text_end, text_end)))

    if False:
        drawer.rectangle((main_text_start, main_text_end), outline='blue')
    extract = image.crop((main_text_start[0], main_text_start[1],
                          main_text_end[0], main_text_end[1]))
    del image
    if DEBUG:
        extract.save('text.png')
    return extract


def bubble(text, hotspot="se"):
    """ Generates an info bubble

    :param text: The multiline string to insert in the annotation info bubble
    :param hotspot: orientation, determines the image used
    :return:
    """
    # ninepatch = Ninepatch('./bubbles/{0}.9.png'.format(hotspot))
    ninepatch = Ninepatch('/home/nlaurance/PycharmProjects/bubbles/bubbles/{0}.9.png'.format(hotspot))
    text_as_image = text2img(text)
    scaled_bubble = ninepatch.render_wrap(text_as_image)
    if DEBUG:
        scaled_bubble.save('bubble.png')
    return scaled_bubble


def paste_outline(screenshot, coords):
    """ center an outline image around all the given elements coordinates

    :param screenshot: current screenshot, PIL Image or StringIO
    :param coords: list of coordinates, tuples of x, y, width, height
    """
    for coord in coords:
        x, y, width, height = coord

        ninepatch = Ninepatch('./bubbles/neon.9.png')
        outline_img = ninepatch.render_to_fit((width, height))
        # fully centered
        outline_w, outline_h = outline_img.size
        paste_x = int(x - (outline_w - width)/2)
        paste_y = int(y - (outline_h - height)/2)

        screenshot.paste(outline_img, (paste_x, paste_y), outline_img)
    return screenshot

paste_spot = {
    "n": lambda x, y, width, height, bubble_w, bubble_h: (int(x + (width - bubble_w)/2), int(y - bubble_h)),
    "s": lambda x, y, width, height, bubble_w, bubble_h: (int(x + (width - bubble_w)/2), int(y + height)),
    "e": lambda x, y, width, height, bubble_w, bubble_h: (int(x + width), int(y + (height - bubble_h)/2)),
    "w": lambda x, y, width, height, bubble_w, bubble_h: (int(x - bubble_w), int(y + (height - bubble_h)/2)),
    "nw": lambda x, y, width, height, bubble_w, bubble_h: (int(x - bubble_w), int(y - bubble_h)),
    "ne": lambda x, y, width, height, bubble_w, bubble_h: (int(x + width), int(y - bubble_h)),
    "se": lambda x, y, width, height, bubble_w, bubble_h: (int(x + width), int(y + height)),
    "sw": lambda x, y, width, height, bubble_w, bubble_h: (int(x - bubble_w), int(y + height)),
}


def paste_bubble(screenshot, coords, hotspot, text):
    """ Adds a text info bubble in a screenshot

    :param screenshot: current screenshot, PIL Image or StringIO
    :param coords: list of coordinates, tuples of x, y, width, height
    :param hotspot: orientation of the bubble
    :param text: multiline string, text to insert
    :return: PIL Image
    """
    for coord in coords:
        x, y, width, height = coord

    bubble_img = bubble(text, hotspot)
    bubble_w, bubble_h = bubble_img.size
    paste_x, paste_y = paste_spot[hotspot](x, y, width, height, bubble_w, bubble_h)

    screenshot.paste(bubble_img, (paste_x, paste_y), bubble_img)
    return screenshot


if __name__ == '__main__':
    DEBUG = True
    bubble('Oh! lorem ipsum')
    text2img('sic fluentes\nex mercantur')
