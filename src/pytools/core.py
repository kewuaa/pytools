import asyncio
import sys
from io import BytesIO
from pathlib import Path

import aiofiles
import pyperclip
from PIL import Image, ImageGrab
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from qasync import (
    QEventLoop,
    asyncClose,
    asyncSlot,
)

from .OCR import Recognizer
from .transform import Transformer, TransformType
from .ui.main_ui import Ui_MainWindow


class Pytools(Ui_MainWindow, QtWidgets.QMainWindow):
    """ GUI."""

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()

        # init transformer
        self._transformer = Transformer(loop=self._loop)
        # init recognizer
        self._recognizer = Recognizer(loop=self._loop)

        # init UI related
        super().__init__()
        self._loop.call_soon(self.setupUi)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.deinit()
        return super().closeEvent(event)

    def deinit(self) -> None:
        asyncClose(self._recognizer.exit)()

    def setupUi(self) -> None:
        super().setupUi(self)
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(
            self.pdf2img_radioButton,
            TransformType.PDF2IMG.value
        )
        self.buttonGroup.addButton(
            self.pdf2docx_radioButton,
            TransformType.PDF2DOCX.value
        )
        self.buttonGroup.addButton(
            self.img2pdf_radioButton,
            TransformType.IMG2PDF.value
        )
        self.buttonGroup.addButton(
            self.docx2pdf_radioButton,
            TransformType.DOCX2PDF.value
        )
        self._center()

    def _center(self):
        """窗口居中。"""

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @asyncSlot()
    async def on_from_clipboard_button_clicked(self) -> None:
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

    @Slot()
    def on_copy_button_clicked(self) -> None:
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

    @asyncSlot()
    async def on_from_file_button_clicked(self) -> None:
        files, fts = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            '选择一个或多个图片',
            str(Path.cwd()),
            filter= 'image file (*.jpg *.png *.bmp);;PDF file (*.pdf)'
        )
        _ = fts
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

    @Slot()
    def on_transform_button_clicked(self) -> None:
        """注册转换任务。"""

        index = self.buttonGroup.checkedId()
        if index < 0:
            QtWidgets.QMessageBox.information(
                self,
                "info",
                "not choose transform type yet"
            )
            return
        type = TransformType(index)
        # 选择需要转换的文件
        if type is TransformType.IMG2PDF:
            file_dialog = QtWidgets.QFileDialog(self)
            file_dialog.setWindowTitle('选择一个或多个包含图片的目录')
            file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
            file_dialog.setOption(
                QtWidgets.QFileDialog.Option.DontUseNativeDialog,
                True
            )
            for view in file_dialog.findChildren(QtWidgets.QListView) + \
                file_dialog.findChildren(QtWidgets.QTreeView):
                if isinstance(view.model(), QtWidgets.QFileSystemModel):
                    view.setSelectionMode(
                        QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
                    )
            if file_dialog.exec():
                files = file_dialog.selectedFiles()
            else:
                return
        else:
            if type is TransformType.PDF2IMG or \
                type is TransformType.PDF2DOCX:
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
            _ = fts
            if not files:
                return
        dest_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            '选择保存目录'
        )
        if dest_path:
            self._loop.create_task(self._transformer(files, dest_path, type)) \
                .add_done_callback(
                    lambda fut: QtWidgets.QMessageBox.information(self, "info", "done")
                    if fut.exception() is None else None
                )


def run() -> None:
    """ run the application."""

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    pytools = Pytools()
    pytools.show()
    with loop:
        loop.run_forever()
