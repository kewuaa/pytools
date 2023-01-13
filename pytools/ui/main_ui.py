#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

from ..lib.asynctk import AsyncTk


class MainApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel = AsyncTk() if master is None else tk.Toplevel(master)
        self.toplevel.configure(height=800, width=600)
        self.toplevel.resizable(False, False)
        frame1 = ttk.Frame(self.toplevel)
        frame1.configure(height=600, width=800)
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=600, relief="groove", width=100)
        self.OCR_button = ttk.Button(frame2)
        self.OCR_button.configure(text='OCR')
        self.OCR_button.pack(padx=10, pady=35, side="top")
        self.OCR_button.configure(command=self.switch_to_OCR_frame)
        self.PDF_button = ttk.Button(frame2)
        self.PDF_button.configure(text='PDF')
        self.PDF_button.pack(padx=10, pady=15, side="top")
        self.PDF_button.configure(command=self.switch_to_PDF_frame)
        frame2.pack(expand="true", fill="both", side="left")
        self.main_frame = ttk.Frame(frame1)
        self.main_frame.configure(height=600, width=700)
        self.start_frame = ttk.Frame(self.main_frame)
        self.start_frame.configure(height=600, width=700)
        self.start_label = ttk.Label(self.start_frame)
        self.start_label.configure(anchor="center")
        self.start_label.place(
            anchor="nw",
            relheight=1.0,
            relwidth=1.0,
            relx=0.0,
            rely=0.0,
            x=0,
            y=0)
        self.start_frame.pack(expand="true", fill="both", side="top")
        self.main_frame.pack(expand="true", fill="both", side="left")
        frame1.pack(expand="true", fill="both", side="top")
        self.message_label = ttk.Label(self.toplevel)
        self.message_label.configure(relief="groove")
        self.message_label.pack(expand="true", fill="both", side="top")

        # Main widget
        self.mainwindow = self.toplevel

    def run(self):
        self.mainwindow.mainloop()

    def switch_to_OCR_frame(self):
        pass

    def switch_to_PDF_frame(self):
        pass


if __name__ == "__main__":
    app = MainApp()
    app.run()
