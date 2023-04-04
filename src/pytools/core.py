from functools import partial
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from io import BytesIO
import tkinter as tk
import asyncio

from PIL import Image

from pytools import image
from .ui import main_ui
from .ui import OCR_ui
from .ui import PDF_ui
from .lib import clipboard
from .lib.alib import asynctk
from .lib.alib import aiofile
from .OCR import Recognizer
from .PDF import Transformer
from . import logging
from . import setting
_cwd = Path(__file__).parent


class OCRWidget(OCR_ui.OCRWidget):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self._last_dir = ''
        self._init_recognizer()
        name = 'snapshot.exe'
        self._paths = (
            str(_cwd / name),
            str(Path.cwd() / name),
            name,
        )
        image.set(
            'run',
            self.single_recognize_button,
            self.batch_recognize_button,
        )

    def _init_recognizer(self) -> None:
        self._recognizer = Recognizer(loop=asynctk.async_loop)
        asynctk.add_done_before_exit(self._recognizer.exit)

    def choose_file(self) -> None:
        filetypes = [
            (suffix[1:].upper(), suffix)
            for suffix in self._recognizer.support_type
        ]
        file = filedialog.askopenfilename(
            title='choose the image',
            initialdir=self._last_dir or str(Path.cwd()),
            filetypes=filetypes,
        )
        if file:
            self.file_path.set(file)
            self._last_dir = file + '/../'
            logging.info(f'file "{file}" choosed')

    def choose_directory(self) -> None:
        directory = filedialog.askdirectory(
            title='choose the directory',
            initialdir=self._last_dir or str(Path.cwd())
        )
        if directory:
            self.directory_path.set(directory)
            self._last_dir = directory
            logging.info(f'directory "{directory}" choosed')

    def run_snapshot(self) -> None:
        async def popen():
            for p in self._paths:
                proc = await asyncio.create_subprocess_shell(
                    p,
                    stderr=asyncio.subprocess.PIPE,
                    stdin=None,
                    stdout=None,
                )
                stdout, stderr = await proc.communicate()
                if not stderr:
                    return
            logging.warning('could not find executable snapshot')
        asynctk.create_task(popen())

    def _get_img(self):
        file = self.file_path.get()
        img = file if file else clipboard.get_img()
        return img

    def view_image(self) -> None:
        img = self._get_img()
        if type(img) is str:
            asynctk.create_task(image.load(img)).add_done_callback(
                lambda fut: fut.result().show()
                if fut.exception() is None
                else logging.warning(str(fut.exception()))
            )
        elif isinstance(img, Image.Image):
            async def show(img: Image.Image):
                await aiofile.AWrapper(img.show)()
            asynctk.create_task(show(img))
        else:
            logging.info('no image file choosed and no image in clip board')

    def copy_result(self) -> None:
        text = self.result_text.get(1.0, 'end').strip()
        if text:
            clipboard.copy(text)
            logging.info('already copy to clipboard')
        else:
            logging.info('empty Text')

    def _write(self, text: str) -> None:
        self.result_text.delete(1.0, 'end')
        self.result_text.insert('end', text)

    def single_recognize(self) -> None:
        def callback(fut: asyncio.futures.Future):
            exception = fut.exception()
            if exception is not None:
                msg = str(exception)
                logging.error(msg)
                return
            result = fut.result()
            self._write(result)
        img = self._get_img()
        if type(img) is str:
            asynctk.create_task(self._recognizer.recognize(img))\
                .add_done_callback(callback)
        elif isinstance(img, Image.Image):
            f = BytesIO()
            img.save(f, format='PNG')
            data = f.getvalue()
            asynctk.create_task(self._recognizer.recognize('', image=data))\
                .add_done_callback(callback)
            f.close()
        else:
            logging.warning('no image file choosed and no image in clip board')

    def reset_concurrency(self) -> None:
        concurrency = int(self.concurrency_spinbox.get())
        self._recognizer.reset_concurrency(concurrency)

    async def _write_to_file(self, directory: str, result: dict) -> None:
        dir = Path(directory)
        dir.mkdir(exist_ok=True)
        for name, text in result.items():
            async with aiofile.async_open(dir / f'{name}.txt', 'w') as f:
                await f.write(text)
        logging.info(f'successfully write the result to {directory}')

    def batch_recognize(self) -> None:
        directory = self.directory_path.get()
        if not directory:
            logging.warning('no directory choosed')
        else:
            def callback(fut: asyncio.futures.Future):
                exception = fut.exception()
                if exception is not None:
                    logging.error(str(exception))
                    return
                result = fut.result()
                asynctk.create_task(self._write_to_file(
                    directory,
                    result,
                ))
            asynctk.create_task(self._recognizer.recognize(directory))\
                .add_done_callback(callback)


class PDFWidget(PDF_ui.PDFWidget):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self._last_dir = ''
        self._init_pdf_transformer()
        image.set(
            'run',
            self.single_transform_button,
            self.batch_transform_button,
        )

    def _init_pdf_transformer(self) -> None:
        self._transformer = Transformer(loop=asynctk.async_loop)
        keys = self._transformer.SupportType.__members__.keys()
        self.type_combobox.configure(values=tuple(keys))
        self.type_combobox.current(0)

    def choose_file(self) -> None:
        SupportType = self._transformer.SupportType
        transform_type = self.type_combobox.current()
        if transform_type == SupportType.pdf2word or \
                transform_type == SupportType.pdf2img:
            filetypes = [('PDF', '.pdf')]
        elif transform_type == SupportType.word2pdf:
            filetypes = [
                ('WORD', '.doc'),
                ('WORD', '.docx'),
            ]
        elif transform_type == SupportType.img2pdf:
            filetypes = [
                (suffix[1:].upper(), suffix)
                for suffix in self._transformer.support_img_type
            ]
        file = filedialog.askopenfilename(
            title='choose the image',
            initialdir=self._last_dir or str(Path.cwd()),
            filetypes=filetypes,
        )
        if file:
            self.file_path.set(file)
            self._last_dir = file + '/../'
            logging.info(f'file "{file}" choosed')

    def choose_directory(self) -> None:
        directory = filedialog.askdirectory(
            title='choose the directory',
            initialdir=self._last_dir or str(Path.cwd())
        )
        if directory:
            self.directory_path.set(directory)
            self._last_dir = directory
            logging.info(f'directory "{directory}" choosed')

    def _schedule_transform(self, file_or_dir: Path) -> None:
        transform_type = self.type_combobox.current()
        SupportType = self._transformer.SupportType
        if transform_type == SupportType.pdf2word:
            asynctk.create_task(self._transformer.pdf2word(file_or_dir))
        elif transform_type == SupportType.word2pdf:
            asynctk.create_task(self._transformer.word2pdf(file_or_dir))
        elif transform_type == SupportType.pdf2img:
            asynctk.create_task(self._transformer.pdf2img(file_or_dir))
        elif transform_type == SupportType.img2pdf:
            asynctk.create_task(self._transformer.img2pdf(file_or_dir))

    def single_transform(self) -> None:
        file = self.file_path.get()
        if not file:
            logging.warning('no file choosed')
            return
        self._schedule_transform(file)

    def batch_transform(self) -> None:
        directory = self.directory_path.get()
        if not directory:
            logging.warning('no directory choosed')
            return
        self._schedule_transform(directory)


class MainApp(main_ui.MainApp):
    def __init__(self) -> None:
        super().__init__()
        self.mainwindow.title('pytools')
        self.ocr_frame = None
        self.pdf_frame = None
        self.__setting = {}
        self.__themes = {}
        image.set('start', self.start_label)
        self.__load_theme_submenu()

        def log(msg: str, color: str = 'blue', delay=3000) -> None:
            self.message_label.configure(text=msg, foreground=color)
            self.mainwindow.after(
                delay,
                lambda: self.message_label.configure(text='')
            )
        logging.add_info_logger(partial(log))
        logging.add_warning_logger(partial(log, color='red'))
        logging.add_error_logger(
            lambda msg: messagebox.showerror('error', msg),
        )

    def __load_setting(self, setting: dict) -> None:
        self.__setting.update(setting)
        theme = setting.get('theme', 'xpnative')
        load_theme = self.__themes.get(theme)
        if load_theme is None:
            logging.warning(
                f'{theme} is part of ttkthemes, but you do not have ttkthemes',
            )
        else:
            load_theme()

    def __set_theme(self, theme: str) -> None:
        self.__setting['theme'] = theme
        self.__themes[theme]()

    def __load_theme_submenu(self) -> None:
        def add_theme_command(theme: str) -> None:
            self.theme_submenu.add_command(
                label=theme,
                command=partial(self.__set_theme, theme)
            )
        interval = 50
        # add theme options
        style = tk.ttk.Style(self.mainwindow)
        for i, theme in enumerate(style.theme_names()):
            self.__themes[theme] = partial(style.theme_use, theme)
            self.mainwindow.after(i * interval, add_theme_command, theme)
        i += 1
        self.mainwindow.after(
            i * interval,
            self.theme_submenu.add,
            'separator',
        )

        # 添加ttkthemes的主题样式
        def add_additional_themes():
            try:
                import ttkthemes
            except ImportError:
                msg = 'load ttkthemes failed, use pip to install it'
                logging.info(msg)
            else:
                self.theme_submenu.delete('load more')
                logging.info('loading ttkthemes......')
                theme_style = ttkthemes.ThemedStyle(self.mainwindow)
                for i, theme in enumerate(ttkthemes.THEMES):
                    self.__themes[theme] = partial(
                        theme_style.set_theme,
                        theme,
                    )
                    self.mainwindow.after(
                        i * interval,
                        add_theme_command,
                        theme,
                    )
                self.mainwindow.after(
                    (i + 1) * interval,
                    logging.info,
                    'ttkthemes loaded',
                )
        i += 1
        self.mainwindow.after(
            i * interval,
            lambda: self.theme_submenu.add_command(
                    label='load more',
                    command=add_additional_themes
                ),
        )
        i += 1
        self.mainwindow.after(i * interval, add_additional_themes)

        i += 1
        self.mainwindow.after(i * interval, setting.load, self.__load_setting)
        self.mainwindow.add_done_before_exit(
            partial(setting.save, self.__setting),
        )

    def _clear_main_frame(self) -> None:
        for child in self.main_frame.winfo_children():
            child.pack_forget()

    def switch_to_OCR_frame(self) -> None:
        if self.ocr_frame is None:
            self.ocr_frame = OCRWidget(self.main_frame)
        self._clear_main_frame()
        self.ocr_frame.pack()

    def switch_to_PDF_frame(self) -> None:
        if self.pdf_frame is None:
            self.pdf_frame = PDFWidget(self.main_frame)
        self._clear_main_frame()
        self.pdf_frame.pack()
