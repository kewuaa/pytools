import asyncio

from pytools.PDF.transformer import Transformer
loop = asyncio.get_running_loop()
transformer = Transformer()
pdf_file = r"C:\Users\kewuaa\Desktop"
word_file = ''
img_file = ''


def test_word2pdf():
    async def test_word2pdf():
        await transformer.word2pdf(word_file)
    loop.run_until_complete(test_word2pdf())


def test_pdf2word():
    async def test_pdf2word():
        await transformer.pdf2word(pdf_file)
    loop.run_until_complete(test_pdf2word())


def test_pdf2img():
    async def test_pdf2img():
        await transformer.pdf2img(pdf_file)
    loop.run_until_complete(test_pdf2img())


def test_img2pdf():
    async def test_img2pdf():
        await transformer.img2pdf(img_file)
    loop.run_until_complete(test_img2pdf())
