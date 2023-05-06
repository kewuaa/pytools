from typing import Callable, Any
from pathlib import Path
from functools import wraps
import asyncio

from src.pytools.transform.core import pdf2img, pdf2docx, img2pdf, docx2pdf
from src.pytools.transform import Transformer, TransformType


def to_sync(func) -> Callable:
    @wraps(func)
    def run(*args, **kwargs) -> Any:
        return loop.run_until_complete(func(*args, **kwargs))
    loop = asyncio.get_event_loop()
    return run


@to_sync
async def test_pdf2img():
    pdf_file = Path('./test_source/pdf2img/test.pdf')
    await pdf2img(pdf_file, pdf_file.parent)


@to_sync
async def test_pdf2docx():
    pdf_file = Path('./test_source/pdf2docx/test.pdf')
    await pdf2docx(pdf_file, pdf_file.parent)


@to_sync
async def test_img2pdf():
    img_dir = Path('./test_source/img2pdf')
    img_files = img_dir.glob('*.png')
    await img2pdf(img_files, img_dir)


@to_sync
async def test_docx2pdf():
    docx_file = Path('./test_source/docx2pdf/test.docx')
    await docx2pdf(
        docx_file.resolve(),
        (docx_file.parent).resolve()
    )

def test_transformer():
    dest_path = Path('./test_source/total').resolve()
    transformer = Transformer()
    transformer.register(
        [Path('./test_source/pdf2img/test.pdf')],
        dest_path,
        TransformType.PDF2IMG
    )
    transformer.register(
        [Path('./test_source/pdf2docx/test.pdf')],
        dest_path,
        TransformType.PDF2DOCX
    )
    transformer.register(
        [Path('./test_source/img2pdf').glob('*.png')],
        dest_path,
        TransformType.IMG2PDF
    )
    transformer.register(
        [Path('./test_source/docx2pdf/test.docx').resolve()],
        dest_path,
        TransformType.DOCX2PDF
    )
    transformer.run()
