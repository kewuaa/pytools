from sys import path
path[0] = path[0] + '/..'
import asyncio

from pytools.PDF_transformer import Transformer
# from pytools.OCR_recognizer.core import Recognizer


async def main():
    transformer = Transformer()
    pdf_file = r"C:\Users\kewuaa\Desktop\【电子科大】潘楚闻-电磁场与无线技术 (1).pdf"
    await transformer.pdf2img(pdf_file)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
