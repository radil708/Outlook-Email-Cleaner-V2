import tkinter as tk
from tkinter import ttk
from model.cleanup_model import cleanup_model
from model.outlook_connection import outlook_connection
from time import sleep
class email_deletion_progress_window(tk.Tk):
  def __init__(self,  oc: outlook_connection, m: cleanup_model):
    tk.Tk.__init__(self)
    self.oc = oc
    self.m = m
    self.title(f"Deleting Emails Matching Your Condition(s)")
    self.all_emails = self.oc.get_all_emails_from_inbox()
    self.email_counter = 0
    self.email_encounter_counter = 0
    self.email_deletion_counter = 0
    self.max_value = len(self.all_emails)
    self.loading_text_reading = "Looked Through " + str(self.email_counter) + " Found " + str(self.email_encounter_counter) + " matches"

    self.bar_increment_value = 100 / self.max_value
    self.current_bar_value = 0
    self.bottom_label_text = str(self.current_bar_value) + " %"

    self.setup()
    self.after(1000, self.increment)


  def setup(self):
    '''
    Must call to place widgets in right place
    :return:
    '''
    label = tk.Label(master=self, text=self.loading_text_reading)
    self.head_label = label
    label.pack(side="top")

    progress_bar = ttk.Progressbar(master=self, length=200)
    self.progress_bar = progress_bar
    progress_bar.pack(side="top")

    label_bottom = tk.Label(master=self, text=self.bottom_label_text)
    label_bottom.pack(side="top")
    self.label_bottom = label_bottom

  def increment(self):
    error_flag = True
    try:
      while self.email_counter < self.max_value:
        current_email = self.all_emails[self.email_counter]

        #TODO DELETE
        #print(current_email.SenderEmailAddress)
        #exit(0)

        if self.m.run_condition_check(current_email) is True:
          #TODO ADD ACTUAL DELETION HERE LAST
          self.oc.add_email_to_deletion_list(current_email)
          self.email_encounter_counter += 1
          #TODO SOME ERROR HERE NO MATCHES FOUND??
          if current_email.SenderEmailAddress == "do-not-reply@northeastern.edu":
            print("FOUND MATCH")


        self.current_bar_value += self.bar_increment_value
        self.progress_bar.step(self.bar_increment_value)
        self.head_label.configure(text="Looked Through " + str(self.email_counter) + " Found " + str(self.email_encounter_counter) + " matches")
        self.label_bottom.configure(text=str(round(self.current_bar_value, 2)) + " %")

        self.update_idletasks()
        self.email_counter += 1

    except KeyboardInterrupt:
      error_flag = True

    sleep(5)
    if error_flag == True:
      self.m.reset_deletion_conditions()
      self.destroy()
    else:
      self.m.reset_deletion_conditions()
      self.destroy()
      #have popup window

