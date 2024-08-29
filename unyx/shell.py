from .unixsys import Directory, File
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
import pickle


class Shell:
    def __init__(self, system:str):
        with open(system, 'rb') as f:
            self.system:dict = pickle.load(f)
        self.current = self.system.get('root')
        self.root = tk.Tk()
        self.root.title('Unyx Shell')
