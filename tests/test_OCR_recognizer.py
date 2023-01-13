from sys import path
import asyncio
path[0] = path[0] + '/..'

from pytools.OCR_recognizer import Recognizer
recognizer = Recognizer()
img_file = ''


async def main():
    await recognizer.recognize(img_file)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
