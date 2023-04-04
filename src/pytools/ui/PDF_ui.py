#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class PDFWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(PDFWidget, self).__init__(master, **kw)
        frame2 = ttk.Frame(self)
        frame2.configure(height=200, width=200)
        self.type_combobox = ttk.Combobox(frame2)
        self.transform_type = tk.StringVar()
        self.type_combobox.configure(
            state="readonly",
            textvariable=self.transform_type,
            width=9)
        self.type_combobox.pack(pady=10, side="top")
        self.single_frame = ttk.Frame(frame2)
        self.single_frame.configure(height=200, width=200)
        label1 = ttk.Label(self.single_frame)
        label1.configure(text='single:')
        label1.pack(side="left")
        entry1 = ttk.Entry(self.single_frame)
        self.file_path = tk.StringVar()
        entry1.configure(
            state="readonly",
            textvariable=self.file_path,
            width=30)
        entry1.pack(padx=5, pady=10, side="left")
        button7 = ttk.Button(self.single_frame)
        button7.configure(text='choose', width=7)
        button7.pack(padx=5, pady=10, side="left")
        button7.configure(command=self.choose_file)
        separator2 = ttk.Separator(self.single_frame)
        separator2.configure(orient="vertical")
        separator2.pack(expand="true", fill="both", pady=10, side="left")
        self.single_transform_button = ttk.Button(self.single_frame)
        self.single_transform_button.configure(width=4)
        self.single_transform_button.pack(padx=5, pady=10, side="left")
        self.single_transform_button.configure(command=self.single_transform)
        self.single_frame.pack(side="top")
        self.batch_frame = ttk.Frame(frame2)
        self.batch_frame.configure(height=200, width=200)
        label2 = ttk.Label(self.batch_frame)
        label2.configure(text=' batch:')
        label2.pack(side="left")
        entry2 = ttk.Entry(self.batch_frame)
        self.directory_path = tk.StringVar()
        entry2.configure(
            state="readonly",
            textvariable=self.directory_path,
            width=30)
        entry2.pack(padx=5, pady=10, side="left")
        button9 = ttk.Button(self.batch_frame)
        button9.configure(text='choose', width=7)
        button9.pack(padx=5, pady=10, side="left")
        button9.configure(command=self.choose_directory)
        separator3 = ttk.Separator(self.batch_frame)
        separator3.configure(orient="vertical")
        separator3.pack(expand="true", fill="both", pady=10, side="left")
        self.batch_transform_button = ttk.Button(self.batch_frame)
        self.batch_transform_button.configure(width=4)
        self.batch_transform_button.pack(padx=5, pady=10, side="left")
        self.batch_transform_button.configure(command=self.batch_transform)
        self.batch_frame.pack(side="top")
        frame2.place(
            anchor="nw",
            relheight=0.5,
            relwidth=0.8,
            relx=0.1,
            rely=0.25,
            x=0,
            y=0)
        self.configure(height=600, width=700)
        # self.pack(side="top")

    def choose_file(self):
        pass

    def single_transform(self):
        pass

    def choose_directory(self):
        pass

    def batch_transform(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = PDFWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
