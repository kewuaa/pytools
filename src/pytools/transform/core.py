from typing import Optional, Iterable
from pathlib import Path
from io import BytesIO
import asyncio

from aiofiles import os as aos
from pdf2docx import Converter as _Converter
from pdf2docx.page.Pages import Pages
from win32com import client
from PIL import Image
import pythoncom
import fitz
import aiofiles

from .. import logging
from ..types import AnyPath


class Converter(_Converter):
    def __init__(
        self,
        pdf_file: str,
        pdf_data: bytes,
        password: Optional[str] = None
    ) -> None:
        self.filename_pdf = pdf_file
        self.password = str(password or '')
        self._fitz_doc = fitz.Document(stream=pdf_data, filetype='pdf')

        self._pages = Pages()


async def pdf2img(
    pdf_file: AnyPath,
    dest_path: AnyPath,
    *, loop: Optional[asyncio.base_events.BaseEventLoop] = None,
    dpi: Optional[int] = None,
) -> None:
    """实现 PDF 到 图片的转换

    :param pdf_file: PDF 文件路径
    :param dest_path: 转换后的文件的保存路径
    :param loop: 事件循环对象
    :param dpi: 图片的 dpi
    """

    async def convert_page(index: int) -> None:
        pixmap = pdf[index].get_pixmap(dpi=dpi or 100)
        imbytes = pixmap.tobytes()
        page = index + 1
        save_path = dest_path / f'page_{page}.png'
        async with aiofiles.open(save_path, 'wb') as f:
            await f.write(imbytes)
        # with open(save_path, 'wb') as f:
        #     f.write(imbytes)
        logging.info(f'page {page} of {pdf_file} converted')
    loop = loop or asyncio.get_running_loop()
    dest_path = Path(dest_path) / Path(pdf_file).stem

    async with aiofiles.open(pdf_file, 'rb') as f:
        buf = await f.read()
    pdf = fitz.Document(stream=buf, filetype='pdf')
    close_pdf = aos.wrap(pdf.close)
    try:
        await aos.makedirs(dest_path, exist_ok=True)
        page_num = pdf.page_count
        tasks = [
            loop.create_task(convert_page(index)) for index in range(page_num)
        ]
        for task in tasks:
            await task
        logging.info(f'pdf2img done, result saved at {dest_path}')
    finally:
        await close_pdf(loop=loop)


async def pdf2docx(
    pdf_file: AnyPath,
    dest_path: AnyPath,
    *, loop: Optional[asyncio.base_events.BaseEventLoop] = None,
    password: Optional[str] = None,
    start: int = 0,
    end: Optional[int] = None,
) -> None:
    """实现 PDF 到 Word 的转换

    :param pdf_file: PDF 文件的路径
    :param dest_path: 转换后文件的保存路径
    :param loop: 事件循环对象
    """

    loop = loop or asyncio.get_running_loop()
    dest_path = Path(dest_path) / (Path(pdf_file).stem + '.docx')

    async with aiofiles.open(pdf_file, 'rb') as f:
        buf = await f.read()
    converter = Converter(pdf_file, buf, password)
    close_converter = aos.wrap(converter.close)
    try:
        converter.convert(dest_path, start=start, end=end)
        logging.info(f'pdf2docx done, result saved at {dest_path}')
    finally:
        await close_converter(loop=loop)


async def img2pdf(
    img_files: Iterable[AnyPath],
    dest_path: AnyPath,
    *,
    loop: Optional[asyncio.base_events.BaseEventLoop] = None,
) -> None:
    """实现图片到 PDF 的转换

    :param img_files: 图片文件的路径组成的序列
    :param dest_path: 转换文件的保存路径
    :param loop: 事件循环对象
    """

    async def load_img(img_file: AnyPath) -> Image.Image:
        img_file = Path(img_file)
        async with aiofiles.open(img_file, 'rb') as f:
            img_data = await f.read()
        img = Image.open(BytesIO(img_data))
        is_png = 0
        if img_file.suffix == '.png':
            is_png = 1
        if is_png:
            bg = Image.new('RGB', img.size, (255, 255, 255))
            channels = img.split()
            bg.paste(img, mask=None if len(channels) < 4 else channels[3])
            img = bg
        logging.info(f'{img_file} loaded')
        return img
    loop = loop or asyncio.get_running_loop()
    dest_path = Path(dest_path) / 'output.pdf'

    tasks = [
        loop.create_task(load_img(img_file))
        for img_file in img_files
    ]
    imgs: list[Image.Image] = [await task for task in tasks]
    pdf = BytesIO()
    if len(imgs) > 1:
        imgs[0].save(pdf, 'PDF', save_all=True, append_images=imgs[1:])
    else:
        imgs[0].save(pdf, 'PDF')
    async with aiofiles.open(dest_path, 'wb') as f:
        await f.write(pdf.getvalue())
    logging.info(f'img2pdf done, result saved at {dest_path}')


async def docx2pdf(
    docx_file: AnyPath,
    dest_path: AnyPath,
    *, loop: Optional[asyncio.base_events.BaseEventLoop] = None
) -> None:
    """实现 Word 到 PDF 的转换

    :param docx_file: Word 文件的路径，需要绝对路径
    :param dest_path: 转换文件的保存路径，需要绝对路径
    :param loop: 事件循环对象
    """

    @aiofiles.os.wrap
    def convert() -> None:
        pythoncom.CoInitialize()
        word = client.Dispatch('Word.Application')
        try:
            doc = word.Documents.Open(str(docx_file))
            try:
                doc.SaveAs(str(dest_path), FileFormat=17)
                logging.info(f'docx2pdf done, result saved at {dest_path}')
            finally:
                doc.Close(0)
        finally:
            word.Quit()
            pythoncom.CoUninitialize()
    loop = loop or asyncio.get_running_loop()
    dest_path = Path(dest_path) / (Path(docx_file).stem + '.pdf')

    await convert(loop=loop)
