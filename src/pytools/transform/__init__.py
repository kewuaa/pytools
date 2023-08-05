import asyncio
from enum import IntEnum
from typing import Iterable, Optional

from ..types import AnyPath
from .core import docx2pdf, img2pdf, pdf2docx, pdf2img


class TransformType(IntEnum):
    """支持的转换类型。"""

    PDF2IMG = 0
    PDF2DOCX = 1
    IMG2PDF = 2
    DOCX2PDF = 3


class Transformer:
    """控制文件转换类。"""

    def __init__(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """初始化。

        :param loop: 事件循环对象
        """

        self._loop = loop if loop is not None else asyncio.get_event_loop()

    async def __call__(
        self,
        files: Iterable[AnyPath],
        dest_path: AnyPath,
        type: TransformType,
    )-> None:
        """ 转换。

        :param files: 需要转换的文件
        :param dest_path: 转换后的文件的保存位置
        :param type: 转换类型
        """

        if type is TransformType.PDF2IMG:
            for file in files:
                await pdf2img(file, dest_path, loop=self._loop)
        elif type is TransformType.PDF2DOCX:
            for file in files:
                await pdf2docx(file, dest_path, loop=self._loop)
        elif type is TransformType.IMG2PDF:
            for imgs_dir in files:
                await img2pdf(imgs_dir, dest_path, loop=self._loop)
        elif type is TransformType.DOCX2PDF:
            for file in files:
                await docx2pdf(file, dest_path, loop=self._loop)
