from pathlib import Path
from PIL import ImageTk, Image
import tkinter as tk

from ..lib.aiofile import AWrapper
from ..lib import asynctk
__cwd = Path(__file__).parent


async def __set(name: str, widget: tk.Widget, *widgets) -> None:
    img = await aget(name)
    # widget.update()
    size = widget.winfo_width(), widget.winfo_height()
    resized_img = img.resize(size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized_img)
    widget.img = img
    widget.configure(image=img)
    if widgets:
        for w in widgets:
            w.configure(image=img)


def set(name: str, widget: tk.Widget, *widgets) -> None:
    widget.after(
        10,
        asynctk.create_task,
        __set(name, widget, *widgets),
    )


async def aget(name: str) -> Image.Image:
    img = tuple(__cwd.glob(f'{name}.*'))
    if not img:
        raise RuntimeError(f'could not find img named {name} in {str(__cwd)}')
    img: Image.Image = await AWrapper(Image.open)(str(img[0]))
    return img


async def load(path: str or Path) -> Image.Image:
    img = await AWrapper(Image.open)(str(path))
    return img
