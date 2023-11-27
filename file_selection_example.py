import tkinter
from tkinter import filedialog
import os

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

folder_path = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file" )

print(folder_path)