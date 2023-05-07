from pathlib import Path

from src.pytools.transform import Transformer, TransformType
from src import pytools


def test_transformer():
    dest_path = Path('./test_source/total').resolve()
    transformer = Transformer()
    transformer.register(
        [Path('./test_source/pdf2img/test.pdf')],
        dest_path,
        TransformType.PDF2IMG,
        dpi=60
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


# test_transformer()
pytools.App().run()
