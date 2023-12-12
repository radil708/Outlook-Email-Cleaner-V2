import tkinter as tk
from tkinter import ttk
from model.inbox_analyzer import inbox_analyzer
from model.outlook_connection import outlook_connection
from view.file_saving_window import file_saving_window
from model.constants import *

from time import sleep
class progress_bar_window(tk.Tk):

  def __init__(self, oc: outlook_connection, ia: inbox_analyzer, label_input: str):
    tk.Tk.__init__(self)
    self.title(f"Analysis of Emails By {label_input}")
    self.head_label_text = f"Analyzing Emails By: {label_input}"
    self.oc = oc
    self.ia = ia
    self.label_input = label_input
    self.ia.clear_trackers()
    self.all_emails = self.oc.get_all_emails_from_inbox()
    self.email_counter = 0
    self.max_value = len(self.all_emails)
    self.loading_text = "Analyzed" + " " + str(self.email_counter) + " of " + str(self.max_value)
    self.bar_increment_value = 100/self.max_value
    self.after(1000, self.increment)

  def setup(self):
    label = tk.Label(master=self, text=self.head_label_text)
    self.head_label = label
    label.pack(side="top")

    progress_bar = ttk.Progressbar(master=self, maximum=self.max_value, length=100)
    self.progress_bar = progress_bar
    progress_bar.pack(side="top")

    label_bottom = tk.Label(master=self, text=self.loading_text)
    label_bottom.pack(side="top")
    self.label_bottom = label_bottom

  def increment(self):
    error_flag = False

    try:
      while self.email_counter < self.max_value:
          current_email = self.all_emails[self.email_counter]
          if self.label_input == SENDER_NAME_C:
            current_email_name = self.oc.extract_sender_name_from_email(current_email)
            self.ia.record_individual_sender(current_email_name)
          self.progress_bar.step(self.bar_increment_value)
          self.email_counter += 1
          self.loading_text = "Analyzed" + " " + str(self.email_counter) + " of " + str(self.max_value)
          self.label_bottom.configure(text=self.loading_text)
          self.update_idletasks()
    except KeyboardInterrupt:
      #pass
      error_flag = True

    if error_flag == True:
      self.ia.clear_trackers()
      self.destroy()
    else:
      self.destroy()
      save_window = file_saving_window(self.ia,self.email_counter,self.label_input)
      save_window.mainloop()
