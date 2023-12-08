import tkinter as tk
from tkinter import ttk


class tkinter_view():

  def __init__(self):
    self.title_for_all_windows = 'Ramzi\'s Email Deleter Version 2'
    self.user_email_choice = None
    self.welcome_window = None
    self.main_gui_window = None

    #Need to access condition widgets
    self.name_entry_widget = None
    self.name_entry_upload_button_widget = None
    self.name_entry_clear_button_widget = None

    self.address_entry_widget = None
    self.address_entry_upload_button_widget = None
    self.address_entry_clear_button_widget = None

    self.subject_keywords_entry_widget = None
    self.subject_keywords_entry_upload_button_widget = None
    self.subject_keywords_entry_clear_button_widget = None

    self.subject_keywords_entry_widget = None
    self.subject_keywords_entry_upload_button_widget = None
    self.subject_keywords_entry_clear_button_widget = None



  def get_user_email_choice(self) -> str:
    if self.user_email_choice == None:
      raise ValueError("No User Email Assigned")

    return self.user_email_choice

  def set_user_email_choice(self, user_email_choice_in: str):
    self.user_email_choice = user_email_choice_in
    # TODO Delete
    print(self.user_email_choice)
    self.build_main_window()

    #TODO use quit or destroy??

  def build_welcome_window(self, user_email_choices: list):
    #TODO have raise error if user_email_choices is blank
    #maybe make an error window?
    window = tk.Tk()
    window.title(self.title_for_all_windows)
    window.geometry('400x200')
    window.eval('tk::PlaceWindow . center')

    user_selection = tk.StringVar()

    input_frame = ttk.Frame(master=window)
    combo = ttk.Combobox(
      master=input_frame,
      state="readonly",
      values=user_email_choices,
      textvariable=user_selection
    )
    select_button = ttk.Button(master=input_frame,
                               text="Select",
                               command=lambda: self.set_user_email_choice(user_selection.get()))
    combo.pack(side="left", padx=5)
    select_button.pack(side="right")
    header_label = ttk.Label(master= window,
                             text="Select the Email You Want To Cleanup",
                             font="Bold")

    header_label.pack(pady=10)
    input_frame.pack(pady=15)
    self.welcome_window = window

    #TODO probably have controller manage mainloop
    #window.mainloop()

  def build_condition_input_frames(self, condition_name_label: str, entry_hint_text : str):

  def build_main_window(self):
    self.welcome_window.destroy()  # hide window to show other one
    main_window = tk.Tk()
    main_window.title(self.title_for_all_windows)
    main_window.geometry('500x250')
    main_window.eval('tk::PlaceWindow . center')
    #menu_bar_frame = tk.Frame(master=main_window)
    #menu_bar_frame.pack(side="top")


    #Create Toolbar
    toolbar = tk.Menu() # make menu class instance/top level menu
    main_window.configure(menu=toolbar) #set menu instance as value of menu attribute, can NOT pack

    # Create inner menu widget that goes into toolbar
    file_dropdown = tk.Menu(master=toolbar, tearoff=False) # make inner menu widget and place in toolbar
    toolbar.add_cascade(label="File", menu=file_dropdown) #Need to add label to menu in order to be visibile.
    file_dropdown.add_command(label="Export Current Conditions", command=main_window.quit) #TODO change command
    file_dropdown.add_command(label="Import Conditions", command=main_window.quit)

    analyze_dropdown = tk.Menu(master=toolbar, tearoff=False)  # make inner menu widget and place in toolbar
    toolbar.add_cascade(label="Analyze", menu=analyze_dropdown)  # Need to add label to menu in order to be visibile.
    analyze_dropdown.add_command(label="By Sender Address", command=main_window.quit)  # TODO change command
    analyze_dropdown.add_command(label="By Sender Name", command=main_window.quit)


    #Name input frame
    name_input_frame = tk.Frame(master=main_window)



    main_window.mainloop()



def main():
  welcome = tkinter_view()
  welcome.build_welcome_window(["email_1", "email_2"])
  welcome.welcome_window.mainloop()


if __name__ == "__main__":
  main()
