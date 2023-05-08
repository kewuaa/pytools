from typing import Callable, Any, Optional
from functools import partial, wraps
from pathlib import Path
from io import BytesIO

import sys
import asyncio

from PySide6 import QtWidgets
from qasync import QEventLoop, asyncClose
from PIL import ImageGrab, Image
import pyperclip
import aiofiles

from .transform import Transformer, TransformType
from .OCR import Recognizer
from .ui import ui_main, ui_popup_choose
from . import logging


def to_sync(async_func: Callable) -> Callable:
    """将异步函数转换为同步函数。"""

    @wraps(async_func)
    def run(
        *args,
        loop: Optional[asyncio.base_events.BaseEventLoop] = None,
        **kwargs
    ) -> Any:
        loop = loop or asyncio.get_running_loop()
        return loop.create_task(async_func(*args, **kwargs))
    return run


class PopupChoose(ui_popup_choose.Ui_Dialog, QtWidgets.QDialog):
    """弹出选择框。"""

    _LIST_ITEMS = tuple(_type.title() for _type in TransformType._member_names_)

    def __init__(self, parent: Optional[QtWidgets.QWidget]) -> None:
        super().__init__(parent)
        asyncio.get_running_loop().call_soon(self.setupUi)

    def setupUi(self) -> None:
        """初始化 UI。"""

        super().setupUi(self)
        self.comboBox.addItems(self._LIST_ITEMS)

    @property
    def choosed_item(self) -> TransformType:
        index = self.comboBox.currentIndex()
        return TransformType(index)


class App(ui_main.Ui_MainWindow, QtWidgets.QMainWindow):
    """GUI."""

    def __init__(self) -> None:
        # init qt application and event loop
        self._qt_app = QtWidgets.QApplication(sys.argv)
        self._loop: asyncio.base_events.BaseEventLoop = \
            QEventLoop(app=self._qt_app)
        asyncio.set_event_loop(self._loop)

        # init transformer
        self._transformer = Transformer(loop=self._loop)
        # init recognizer
        self._recognizer = Recognizer(loop=self._loop)
        # let recognizer exit before app exit
        self._recognizer.exit = asyncClose(self._recognizer.exit)

        # config logging
        logging.add_warning_logger(
            partial(QtWidgets.QMessageBox.warning, self, 'warning')
        )

        # init UI related
        super().__init__()
        self._loop.call_soon(self.setupUi)

    def setupUi(self) -> None:
        """渲染 UI 以及绑定回调函数。"""

        # setup UI
        super().setupUi(self)
        self._center()

        # connect signal
        self.run_button.clicked.connect(
            partial(self._begin_transform, loop=self._loop)
        )
        self.file_choose_button.clicked.connect(self._register_transform_task)
        self.from_file_button.clicked.connect(
            partial(self._recognize_files, loop=self._loop)
        )
        self.from_clipboard_button.clicked.connect(
            partial(self._recognize_img_from_clipboard, loop=self._loop)
        )
        self.copy_button.clicked.connect(self._copy_textbrowser)

    def _center(self):
        """窗口居中。"""

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @to_sync
    async def _recognize_img_from_clipboard(self) -> None:
        """识别剪切板中的图片。"""

        clipboard_img = ImageGrab.grabclipboard()
        if clipboard_img is None:
            QtWidgets.QMessageBox.information(
                self, 'info',
                '剪切板中未检测到图片'
            )
            return
        elif isinstance(clipboard_img, Image.Image):
            img_io = BytesIO()
            clipboard_img.save(img_io, 'PNG')
            img_data = img_io.getvalue()
        else:
            async with aiofiles.open(clipboard_img[0], 'rb') as f:
                img_data = await f.read()
        data = {'image': self._recognizer._encode(img_data)}
        result = await self._recognizer._send_data(data)
        self.result_textbrowser.setText(result)

    def _copy_textbrowser(self) -> None:
        """复制文本框中的内容到剪切板。"""

        text = self.result_textbrowser.toPlainText()
        if text.strip():
            pyperclip.copy(text)
            QtWidgets.QMessageBox.information(
                self, 'info',
                '复制成功'
            )
        else:
            QtWidgets.QMessageBox.information(
                self, 'info',
                '文本框为空'
            )

    @to_sync
    async def _recognize_files(self) -> None:
        """识别一个或多个文件。"""

        files, fts = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            '选择一个或多个图片',
            str(Path.cwd()),
            filter= 'image file (*.jpg *.png *.bmp);;PDF file (*.pdf)'
        )
        if not files:
            return
        result = await self._recognizer.recognize(files)
        if len(result) > 1:
            self.result_textbrowser.clear()
            for _id, text in result.items():
                self.result_textbrowser.append(f'<h1>{_id}:</h1>')
                self.result_textbrowser.append(text)
        else:
            for text in result.values():
                self.result_textbrowser.setText(text)

    def _register_transform_task(self) -> None:
        """注册转换任务。"""

        # 选择转换类型
        popup_choose = PopupChoose(self)
        if not popup_choose.exec_():
            return
        _type = popup_choose.choosed_item
        # 选择需要转换的文件
        if _type is TransformType.IMG2PDF:
            file_dialog = QtWidgets.QFileDialog(self)
            file_dialog.setWindowTitle('选择一个或多个包含图片的目录')
            file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            file_dialog.setOption(
                QtWidgets.QFileDialog.DontUseNativeDialog,
                True
            )
            for view in file_dialog.findChildren(QtWidgets.QListView) + \
                file_dialog.findChildren(QtWidgets.QTreeView):
                if isinstance(view.model(), QtWidgets.QFileSystemModel):
                    view.setSelectionMode(
                        QtWidgets.QAbstractItemView.ExtendedSelection
                    )
            if file_dialog.exec_():
                img_suffixs = {'.png', '.jpg', '.bmp'}
                files = file_dialog.selectedFiles()
                tasks = (
                    (
                        file for file in Path(_dir).iterdir()
                        if file.suffix in img_suffixs
                    )
                    for _dir in files
                )
            else:
                return
        else:
            if _type is TransformType.PDF2IMG or \
                _type is TransformType.PDF2DOCX:
                _filter = 'PDF file (*.pdf)'
            # elif _type is TransformType.IMG2PDF:
            #     _filter = 'image file (*.jpg,*.png,*.bmp)'
            else:
                _filter = 'docx file (*.doc *.docx)'
            files, fts = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                '选择一个或多个文件',
                str(Path.cwd()),
                filter=_filter
            )
            if not files:
                return
            tasks = files
        dest_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            '选择保存目录'
        )
        if dest_path:
            self._transformer.register(tasks, dest_path, _type)
            type_name = _type.name.title()
            self.task_listwidget.addItems([
                type_name + ': ' + file
                for file in files
            ])

    @to_sync
    async def _begin_transform(self) -> None:
        """开始进行转换。"""

        self.statusbar.showMessage('begin to transform', 1000)
        task = self._transformer.run()
        if task is not None:
            try:
                await task
            except asyncio.CancelledError:
                self.task_listwidget.clear()
                QtWidgets.QMessageBox.information(self, 'info', '转换完成')

    def run(self) -> None:
        """启动 GUI 界面。"""

        async def _run() -> None:
            fut = self._loop.create_future()
            self._qt_app.aboutToQuit.connect(
                lambda: (
                    self._recognizer.exit(),
                    fut.set_result(0),
                )
            )
            self.show()
            await fut
        with self._loop:
            self._loop.run_until_complete(_run())
