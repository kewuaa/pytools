from PIL import ImageGrab
import pyperclip
copy = pyperclip.copy


def get_img():
    img = ImageGrab.grabclipboard()
    tp = type(img)
    if tp is list:
        img = img[0]
    return img
