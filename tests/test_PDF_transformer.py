from sys import path
path[0] = path[0] + '/..'
import asyncio

from pytools.PDF_transformer.core import Transformer
from pytools.OCR_recognizer.core import Recognizer
from pytools.logging import logger


async def main():
    transformer = Transformer()
    pdf_file = r"C:\Users\kewuaa\Desktop\Microwave EDA\电磁散射\金属球体仿真1.pdf"
    await transformer.pdf2word(pdf_file)
    print('=' * 33)
    logger.info('test!' * 3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
