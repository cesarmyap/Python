import tkinter as tk
from tkinter import ttk


def apply_style():
    style = ttk.Style()

    # Configure theme
    style.theme_use('clam')

    # Configure colors
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=6)
    style.configure('Treeview', font=('Arial', 10), rowheight=25)
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

    # Configure Entry
    style.configure('TEntry', font=('Arial', 10), padding=5)

    # Configure Combobox
    style.configure('TCombobox', font=('Arial', 10), padding=5)

    # Configure Notebook
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=10)

    # Configure Labels
    style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
    style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))

    # Configure Buttons
    style.configure('Primary.TButton', background='#007bff', foreground='white')
    style.map('Primary.TButton',
              background=[('active', '#0056b3'), ('pressed', '#004085')])

    style.configure('Success.TButton', background='#28a745', foreground='white')
    style.map('Success.TButton',
              background=[('active', '#218838'), ('pressed', '#1e7e34')])

    style.configure('Warning.TButton', background='#ffc107', foreground='black')
    style.map('Warning.TButton',
              background=[('active', '#e0a800'), ('pressed', '#d39e00')])

    style.configure('Danger.TButton', background='#dc3545', foreground='white')
    style.map('Danger.TButton',
              background=[('active', '#c82333'), ('pressed', '#bd2130')])
