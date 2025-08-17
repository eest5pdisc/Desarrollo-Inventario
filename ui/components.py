import tkinter as tk
from tkinter import ttk

class NumericEntry(ttk.Entry):
    """Entry que solo permite números."""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace_add("write", self.validate)

    def validate(self, *args):
        value = self.var.get()
        if not value.isdigit():
            self.var.set(''.join(filter(str.isdigit, value)))