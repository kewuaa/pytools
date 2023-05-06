from functools import partial
from typing import Union, Iterator, Optional
from enum import IntEnum
import asyncio

from .core import pdf2img, pdf2docx, img2pdf, docx2pdf
from ..types import AnyPath


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
        loop: Optional[asyncio.base_events.BaseEventLoop] = None
    ) -> None:
        """初始化。

        :param loop: 事件循环对象
        """

        self._loop = loop or asyncio.get_event_loop()
        self._in_self_loop = not self._loop.is_running()
        self._pending_tasks = asyncio.queues.Queue(8)

    def __del__(self) -> None:
        if self._in_self_loop:
            async def shutdown():
                await self._loop.shutdown_asyncgens()
                await self._loop.shutdown_default_executor()
            if self._loop.is_running():
                self._loop.stop()
            for task in asyncio.tasks.all_tasks(self._loop):
                task.cancel()
            self._loop.run_until_complete(shutdown())

    def register(
        self,
        files: Iterator[Union[AnyPath, Iterator[AnyPath]]],
        dest_path: AnyPath,
        _type: TransformType,
        **kwargs,
    ) -> None:
        """添加需要转换的文件

        :param files: 需要转换的文件
        :param dest_path: 转换后的文件的保存位置
        :param _type: 转换类型
        """

        if _type is TransformType.PDF2IMG:
            transform = partial(pdf2img, dpi=kwargs.get('dpi'))
        elif _type is TransformType.PDF2DOCX:
            transform = pdf2docx
        elif _type is TransformType.IMG2PDF:
            transform = img2pdf
        else:
            transform = docx2pdf
        for file in files:
            self._loop.create_task(
                self._pending_tasks.put(
                    (transform, file, dest_path)
                )
            )

    async def _run(self) -> None:
        """处理循环中的任务。"""

        self._loop.call_soon_threadsafe(
            self._loop.create_task,
            self._stop(asyncio.current_task())
        )
        while 1:
            task = await self._pending_tasks.get()
            transform, *args = task
            self._loop.create_task(transform(*args))\
                .add_done_callback(lambda fut: self._pending_tasks.task_done())

    async def _stop(self, run_task: asyncio.tasks.Task) -> None:
        """当任务全部完成时停止事件循环。"""

        await self._pending_tasks.join()
        run_task.cancel()
        if self._in_self_loop:
            self._loop.stop()

    def run(self) -> None:
        """启动事件循环。"""

        self._loop.create_task(self._run())
        if self._in_self_loop:
            self._loop.run_forever()
