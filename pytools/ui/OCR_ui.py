#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class OCRWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(OCRWidget, self).__init__(master, **kw)
        notebook1 = ttk.Notebook(self)
        notebook1.configure(height=600, width=700)
        frame1 = ttk.Frame(notebook1)
        frame1.configure(height=600, width=700)
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, relief="groove", width=200)
        frame6 = ttk.Frame(frame2)
        frame6.configure(height=200, width=200)
        entry2 = ttk.Entry(frame6)
        self.file_path = tk.StringVar()
        entry2.configure(
            state="readonly",
            textvariable=self.file_path,
            width=30)
        entry2.pack(side="left")
        button3 = ttk.Button(frame6)
        button3.configure(text='choose', width=7)
        button3.pack(padx=10, pady=10, side="left")
        button3.configure(command=self.choose_file)
        frame6.pack(padx=10, pady=10, side="left")
        separator2 = ttk.Separator(frame2)
        separator2.configure(orient="vertical")
        separator2.pack(expand="true", fill="both", pady=10, side="left")
        button2 = ttk.Button(frame2)
        button2.configure(text='snapshot', width=9)
        button2.pack(padx=10, pady=10, side="left")
        button2.configure(command=self.run_snapshot)
        separator1 = ttk.Separator(frame2)
        separator1.configure(orient="vertical")
        separator1.pack(expand="true", fill="both", pady=10, side="left")
        button1 = ttk.Button(frame2)
        button1.configure(text='view', width=5)
        button1.pack(padx=10, pady=10, side="left")
        button1.configure(command=self.view_image)
        frame2.grid(column=0, padx=30, pady=30, row=0, sticky="w")
        self.single_recognize_button = ttk.Button(frame1)
        self.single_recognize_button.configure(width=4)
        self.single_recognize_button.grid(column=1, row=0)
        self.single_recognize_button.configure(command=self.single_recognize)
        self.result_text = tk.Text(frame1)
        self.result_text.configure(
            autoseparators="true",
            font="{none} 16 {}",
            height=20,
            maxundo=23,
            undo="true",
            width=48)
        self.result_text.grid(column=0, columnspan=2, padx=20, row=2)
        button4 = ttk.Button(frame1)
        button4.configure(text='copy', width=5)
        button4.grid(column=2, row=2, sticky="s")
        button4.configure(command=self.copy_result)
        frame1.pack(side="top")
        notebook1.add(frame1, text='single')
        frame3 = ttk.Frame(notebook1)
        frame3.configure(height=600, width=700)
        frame4 = ttk.Frame(frame3)
        frame4.configure(height=200, width=200)
        frame5 = ttk.Frame(frame4)
        frame5.configure(height=200, width=200)
        entry1 = ttk.Entry(frame5)
        self.directory_path = tk.StringVar()
        entry1.configure(
            state="readonly",
            textvariable=self.directory_path,
            width=30)
        entry1.pack(padx=10, pady=10, side="left")
        button5 = ttk.Button(frame5)
        button5.configure(text='choose', width=7)
        button5.pack(padx=10, pady=10, side="left")
        button5.configure(command=self.choose_directory)
        frame5.pack(fill="x", padx=10, pady=10, side="top")
        frame7 = ttk.Frame(frame4)
        frame7.configure(height=200, width=200)
        label2 = ttk.Label(frame7)
        label2.configure(text='concurrency')
        label2.pack(padx=23, pady=10, side="left")
        self.concurrency_spinbox = ttk.Spinbox(frame7)
        self.concurrency_spinbox.configure(from_=1, to=4, width=3)
        _text_ = '2'
        self.concurrency_spinbox.delete("0", "end")
        self.concurrency_spinbox.insert("0", _text_)
        self.concurrency_spinbox.pack(padx=10, pady=10, side="left")
        self.concurrency_spinbox.configure(command=self.reset_concurrency)
        frame7.pack(fill="x", side="top")
        self.batch_recognize_button = ttk.Button(frame4)
        self.batch_recognize_button.configure(width=4)
        self.batch_recognize_button.pack(padx=10, pady=20, side="top")
        self.batch_recognize_button.configure(command=self.batch_recognize)
        frame4.place(
            anchor="nw",
            relheight=0.5,
            relwidth=0.5,
            relx=0.25,
            rely=0.25,
            x=0,
            y=0)
        frame3.pack(side="top")
        notebook1.add(frame3, text='batch')
        notebook1.pack(side="top")
        self.configure(height=600, width=700)
        # self.pack(side="top")

    def choose_file(self):
        pass

    def run_snapshot(self):
        pass

    def view_image(self):
        pass

    def single_recognize(self):
        pass

    def copy_result(self):
        pass

    def choose_directory(self):
        pass

    def reset_concurrency(self):
        pass

    def batch_recognize(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = OCRWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
