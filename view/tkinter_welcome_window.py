import tkinter as tk
from tkinter import ttk
from types import FunctionType

class welcome_window(tk.Tk):

  def __init__(self, user_email_choices : list):
    super().__init__()
    self.title("Ramzi's Email Deleter V2")
    self.geometry('400x200')
    self.eval('tk::PlaceWindow . center')
    self.user_choice = None
    self.header_label = ttk.Label(master=self,
                             text="Select the Email You Want To Cleanup",
                             font="Bold")
    self.header_label.pack(pady=10)

    self.user_selection_var = tk.StringVar()

    self.setup_input_frame(user_email_choices)


  def setup_input_frame(self, available_email_choices: list):
    self.input_frame = ttk.Frame(master=self)

    self.combobox_widget = ttk.Combobox(
      master=self.input_frame,
      state="readonly",
      values=available_email_choices,
      textvariable=self.user_selection_var)

    self.select_button = ttk.Button(master=self.input_frame,
                                   text="Select",
                                   command=lambda: self.set_user_email_choice(self.user_selection_var.get()))

    self.combobox_widget.pack(side="left", padx=5)
    self.select_button.pack(side="right")

    self.input_frame.pack(pady=15)


  def set_user_email_choice(self, user_input : str, next_window_func : FunctionType ) -> None:
    self.user_choice = user_input
    print(self.user_choice)
    self.destroy()
    next_window_func()

  def get_user_email_choice(self):
    #todo raise error if no choice selected
    return self.user_choice

def main():
  choices = ["email_1", "email_2"]
  x = welcome_window(choices)
  x.mainloop()

if __name__ == "__main__":
  main()
