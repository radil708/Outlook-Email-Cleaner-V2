import tkinter as tk
from tkinter import ttk
from model.inbox_analyzer import inbox_analyzer
from model.outlook_connection import outlook_connection
from time import sleep
class progress_bar_window(tk.Tk):

  def __init__(self, oc: outlook_connection, ia: inbox_analyzer):
    tk.Tk.__init__(self)
    self.title("Analyzing Emails By Sender Name")
    self.head_label_text = ""
    self.oc = oc
    self.ia = ia
    self.ia.clear_trackers()
    self.all_emails = self.oc.get_all_emails_from_inbox()
    self.email_counter = 0
    self.max_value = len(self.all_emails)
    self.after(1000, self.increment)
    self.loading_text = f"Analyzed {self.email_counter} of {self.max_value}"
    self.load_text_var = tk.StringVar()
    self.load_text_var.set("TEST")

    #self.progress_bar['value'] <-- this is what needs to be incremented

  def set_head_label(self, label: str) -> None:
    self.head_label_text = label

  def setup(self):
    label = tk.Label(master=self, text=self.head_label_text)
    self.head_label = label
    label.pack(side="top")

    progress_bar = ttk.Progressbar(master=self, maximum=self.max_value, length=self.max_value)
    self.progress_bar = progress_bar
    progress_bar.pack(side="top")

    label_bottom = tk.Label(master=self, textvariable=self.load_text_var)
    label_bottom.pack(side="top")

  def increment(self):
    while self.email_counter < self.max_value:
      try:
        current_email = self.all_emails[self.email_counter]
        current_email_name = self.oc.extract_sender_name_from_email(current_email)
        print(current_email_name)
        self.progress_bar.step(1)
        self.email_counter += 1
        self.load_text_var.set(self.loading_text)
        self.update_idletasks()
        sleep(1)
      except KeyboardInterrupt:
        exit(0)
    self.destroy()
