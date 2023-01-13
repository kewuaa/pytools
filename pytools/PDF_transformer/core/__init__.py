from enum import IntEnum
from pathlib import Path
import asyncio

from win32com import client
from pdf2docx import Converter
import fitz

from pytools.libs import aiofile
from pytools import logging


class Transformer:
    class SupportType(IntEnum):
        pdf2word = 0
        word2pdf = 1
        pdf2img = 2

    def __init__(self, loop: asyncio.base_events.BaseEventLoop = None) -> None:
        self.__loop = loop or asyncio.get_event_loop()

    async def __pdf2word(
        self,
        file: Path,
        dest_path: Path,
        password: str,
        start: int,
        end: int,
        pages: list,
    ) -> None:
        cv = aiofile.AIOWrapper(Converter(str(file), password=password))
        dest_path = dest_path / (file.stem + '.docx')
        try:
            await cv.convert(str(dest_path), start, end, pages)
        finally:
            await cv.close()

    async def pdf2word(
        self,
        pdf_file: str or Path,
        dest_path: str or Path = None,
        password: str = None,
        start: int = 0,
        end: int = None,
        pages: list = None
    ):
        pdf_file = Path(pdf_file) if type(pdf_file) is not Path else pdf_file
        if pdf_file.is_dir():
            dest_path = dest_path or pdf_file
            tasks = [
                self.__loop.create_task(self.__pdf2word(
                    file,
                    dest_path,
                    password,
                    start,
                    end,
                    pages,
                ))
                for file in pdf_file.iterdir()
                if file.suffix == '.pdf'
            ]
            if not tasks:
                msg = f'no pdf file found in {pdf_file}'
                logging.error(msg)
                raise RuntimeError(msg)
            for task in tasks:
                await task
        elif pdf_file.is_file():
            if pdf_file.suffix != '.pdf':
                msg = 'pdf2word need pdf type file'
                logging.error(msg)
                raise RuntimeError(msg)
            dest_path = dest_path or pdf_file.parent
            await self.__pdf2word(
                pdf_file,
                dest_path,
                password,
                start,
                end,
                pages,
            )
        else:
            msg = f'"{pdf_file}" not a file or directory'
            logging.error(msg)
            raise RuntimeError(msg)
        logging.info(f'successfully converted to {dest_path}')

    async def __word2pdf(self, word, file: Path, dest_path: Path) -> None:
        dest_path = dest_path / (file.stem + '.pdf')
        doc = await aiofile.AWrapper(word.Documents.Open)(str(file))
        doc = aiofile.AIOWrapper(doc)
        try:
            await doc.SaveAs(str(dest_path), FileFormat=17)
        except Exception as e:
            logging.error(str(e))
            raise e
        finally:
            await doc.Close(0)

    async def word2pdf(
        self,
        word_file: str or Path,
        dest_path: str or Path = None,
    ) -> None:
        word = await aiofile.AWrapper(client.Dispatch)('Word.Application')
        word = aiofile.AIOWrapper(word)
        try:
            word_file = Path(word_file) if type(word_file) is not Path \
                else word_file
            if word_file.is_dir():
                dest_path = dest_path or word_file
                tasks = [
                    self.__loop.create_task(self.__word2pdf(
                        word,
                        file,
                        dest_path,
                    ))
                    for file in word_file.listdir()
                    if file.suffix in ('.doc', '.docx')
                ]
                if not tasks:
                    msg = f'no word file found in {word_file}'
                    logging.error(msg)
                    raise RuntimeError(msg)
                for task in tasks:
                    await task
            elif word_file.is_file():
                if word_file.suffix not in ('.doc', '.docx'):
                    msg = 'word2pdf need word file'
                    logging.error(msg)
                    raise RuntimeError(msg)
                dest_path = dest_path or word_file.parent
                await self.__word2pdf(word, word_file, dest_path)
            else:
                msg = f'"{word_file}" not a file or directory'
                logging.error(msg)
                raise RuntimeError(msg)
            logging.info(f'successfully transformed to {dest_path}')
        finally:
            await word.Quit()

    async def __img2pdf(self, img_file: Path, dest_path: Path) -> None:
        pdf = await aiofile.AWrapper(fitz.open)()
        pdf = aiofile.AIOWrapper(pdf)

    async def __pdf2img(
        self,
        pdf_file: Path,
        dest_path: Path,
        dpi: int,
        alpha: bool,
        format: str,
    ):
        async def save_page(index: int):
            pm = await aiofile.AWrapper(pdf[index].get_pixmap)(dpi=dpi, alpha=alpha)
            # pm = pdf[index].get_pixmap(dpi=dpi)
            path = dest_path / f'{index + 1}.{format}'
            await aiofile.AWrapper(pm.save)(str(path))
        pdf = await aiofile.AWrapper(fitz.open)(str(pdf_file))
        apdf = aiofile.AIOWrapper(pdf)
        try:
            page_num = pdf.page_count
            tasks = [
                self.__loop.create_task(save_page(i))
                for i in range(page_num)
            ]
            for task in tasks:
                await task
        except Exception as e:
            logging.error(str(e))
            raise e
        finally:
            await apdf.close()

    async def pdf2img(
        self,
        pdf_file: str or Path,
        dest_path: str or Path = None,
        dpi: int = 300,
        alpha: bool = False,
        format: str = 'png',
    ):
        pdf_file = pdf_file if type(pdf_file) is Path else Path(pdf_file)
        if pdf_file.is_file():
            dest_path = dest_path or pdf_file.parent
            await self.__pdf2img(pdf_file, dest_path, dpi, alpha, format)
        elif pdf_file.is_dir():
            dest_path = dest_path or pdf_file
            tasks = [
                self.__loop.create_task(self.__pdf2img(
                    file,
                    dest_path,
                    dpi,
                    alpha,
                    format,
                ))
                for file in pdf_file.iterdir() if file.suffix == '.pdf'
            ]
            if not tasks:
                msg = f'no pdf file found in {pdf_file}'
                logging.error(msg)
                raise RuntimeError(msg)
            for task in tasks:
                await task
        else:
            msg = f'"{pdf_file}" not a file or directory'
            logging.error(msg)
            raise RuntimeError(msg)
        logging.info(f'successfully transformed to {dest_path}')
