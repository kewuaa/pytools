import asyncio

from pytools.OCR.recognizer import Recognizer
recognizer = Recognizer()
img_file = ''


def test_recognizer():
    async def main():
        await recognizer.recognize(img_file)
        asyncio.get_event_loop().run_until_complete(main())
