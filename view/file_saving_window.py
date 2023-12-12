import tkinter as tk
from tkinter import ttk
from model.inbox_analyzer import inbox_analyzer
from model.outlook_connection import outlook_connection
from view.entry_with_placeholder import entry_with_placeholder
from datetime import datetime as dt
from model.constants import *
class file_saving_window(tk.Tk):

  def __init__(self, ia: inbox_analyzer, emails_actually_analyzed: int, save_cond_str):
    tk.Tk.__init__(self)

    self.ia = ia
    self.emails_actually_analyzed = emails_actually_analyzed
    self.save_cond_str = save_cond_str
    self.title("Saving Results From Analysis By " + self.save_cond_str)
    self.unique_modifier = dt.today().strftime("%Y-%m-%d_%H%M%S")
    self.default_file_name = self.save_cond_str + " Analysis " + self.unique_modifier + ".txt"
    self.setup()
    self.save_button.configure(command=self.button_command)




  def button_command(self):
    #TODO add path to a folder of results, #invalid char check????
    user_entry = self.file_name_entry.get()

    if user_entry.isspace() or self.file_name_entry['fg'] == self.file_name_entry.hint_color:
      filepath = self.default_file_name
    else:
      filepath = user_entry

    #TODO can add ../ to go one folder up
    filepath = "../" + filepath.strip()

    if not filepath.endswith(".txt"):
      filepath += ".txt"

    if self.save_cond_str == SENDER_NAME_C:
      self.ia.write_sender_file(filepath)
    if self.save_cond_str == SENDER_ADDRESS_C:
      self.ia.write_email_address_file(filepath)

    self.quit()

  def setup(self):
    label = tk.Label(master=self, text=f"Save Results From Analysis of {self.emails_actually_analyzed} Emails")
    label.pack(pady=5)

    input_frame = tk.Frame(master=self)
    input_label = tk.Label(master=input_frame, text="File Name")
    input_label.pack(side="left")
    self.file_name_entry = entry_with_placeholder(master=input_frame, text_hint=self.default_file_name, width=50)
    self.file_name_entry.pack(side="left", padx=5)
    self.save_button = tk.Button(master=input_frame, text="Save")
    self.save_button.pack(side="left", padx=5)
    input_frame.pack(pady=(5,20))





