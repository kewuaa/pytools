from sys import path
import asyncio
path[0] = path[0] + '/..'

from pytools.PDF_transformer import Transformer
transformer = Transformer()
pdf_file = r"C:\Users\kewuaa\Desktop"
word_file = ''
img_file = ''


async def test_word2pdf():
    await transformer.word2pdf(word_file)


async def test_pdf2word():
    await transformer.pdf2word(pdf_file)


async def test_pdf2img():
    await transformer.pdf2img(pdf_file)


async def test_img2pdf():
    await transformer.img2pdf(img_file)


async def main():
    await test_word2pdf()
    await test_pdf2word()
    await test_pdf2img()
    # await test_img2pdf()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
