from typing import Callable, Any
from pathlib import Path
from functools import wraps
import asyncio

from src.pytools.transform.core import pdf2img, pdf2docx, img2pdf, docx2pdf


def to_sync(func) -> Callable:
    @wraps(func)
    def run(*args, **kwargs) -> Any:
        return loop.run_until_complete(func(*args, **kwargs))
    loop = asyncio.get_event_loop()
    return run


@to_sync
async def test_pdf2img():
    pdf_file = Path('./test_source/test.pdf')
    await pdf2img(pdf_file, pdf_file.parent / 'images')


@to_sync
async def test_pdf2docx():
    pdf_file = Path('./test_source/test.pdf')
    await pdf2docx(pdf_file, pdf_file.parent / f'{pdf_file.stem}.docx')


@to_sync
async def test_img2pdf():
    img_dir = Path('./test_source/images')
    img_files = img_dir.glob('*.png')
    await img2pdf(img_files, img_dir / 'test.pdf')


@to_sync
async def test_docx2pdf():
    docx_file = Path('./test_source/test.docx')
    await docx2pdf(
        docx_file.resolve(),
        (docx_file.parent / (docx_file.stem + '1.pdf')).resolve()
    )
