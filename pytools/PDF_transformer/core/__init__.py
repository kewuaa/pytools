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
        await doc.SaveAs(str(dest_path), FileFormat=17)
        await doc.Close(0)

    async def word2pdf(
        self,
        word_file: str or Path,
        dest_path: str or Path = None,
    ) -> None:
        try:
            word = await aiofile.AWrapper(client.Dispatch('Word.Application'))
        except Exception as e:
            msg = 'your computer seems not have Word Application -> ' + \
                str(e)
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            word = aiofile.AIOWrapper(word)
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

    async def __img2pdf(
        self,
        img_file: str or Path,
        dest_path: str or Path,
    ) -> None:
        pdf = await aiofile.AWrapper(fitz.open)()
        pdf = aiofile.AIOWrapper(pdf)
