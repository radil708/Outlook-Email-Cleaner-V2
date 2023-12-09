import tkinter as tk
from tkinter import ttk
from view.entry_with_placeholder import entry_with_placeholder
from types import FunctionType

class main_window(tk.Tk):

  def __init__(self):
    tk.Tk.__init__(self)
    self.title("Ramzi's Email Deleter V2")
    self.geometry('600x310')
    self.eval('tk::PlaceWindow . center')
    self.upper_user_frame = tk.Frame(master=self)
    self.upper_user_frame.pack(fill="both", expand=1)
    self.current_user = ""
    self.user_label = tk.Label(master=self.upper_user_frame, text="Current Account: ")
    self.user_label.pack(side=tk.RIGHT, padx= 15, pady=(5,0))

    self.header_label = tk.Label(master=self, text="Please Enter Deletion Conditions")
    self.header_label.pack(side="top")
    #TODO prevent window resizing TODO dummy widget keep?


    self.input_frame_grid = tk.Frame()

    self.setup_toolbar()

    self.name_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Name(s):","Doe, Jane | linkedIn | Advertising Company", row=0))

    self.address_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Email Address(es):","jack@aol.com, Mass@us.gov, uni@eduroam.net", row=1)
    )

    self.keywords_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Keyword(s):", "hello, world, foo, bar", row=2)
    )

    self.date_start_widgets_dict = self.create_date_frame_dict(
      self.make_text_input_date_frame("Date Lower Boundary:", "mm/dd/yyy", row=3)
    )

    self.date_end_widgets_dict = self.create_date_frame_dict(
      self.make_text_input_date_frame("Date Upper Boundary:", "mm/dd/yyy", row=4)
    )

    self.input_frame_grid.pack()

    self.bottom_frame = tk.Frame()
    self.switch_act_button = tk.Button(master=self.bottom_frame, text="Switch Accounts")
    self.run_button = tk.Button(master=self.bottom_frame, text="Run")
    self.switch_act_button.pack(side=tk.LEFT, padx=(0,200), pady=20)
    self.run_button.pack(side=tk.RIGHT, padx=(200,0), pady=20)
    self.bottom_frame.pack()


  def set_current_account_label(self, user_email: str):
    self.user_label.configure(text=f"Current Account: {user_email}")

  def set_function_analyze(self, func_name: FunctionType, func_address: FunctionType):
    """
    Reason Note***:  Unlike Buttons which can be reconfigured after instantiation,
    commands can NOT be reconfigured and must have a command associated at the time
    of instatiation. Since the functions I want to link to this command exist
    in the model, I will have the controller call this function and
    pass the model's function to it.
    :param func_name:
    :param func_address:
    :return:
    """
    self.analyze_dropdown.add_command(label="By Sender Name", command=func_name)
    self.analyze_dropdown.add_command(label="By Sender Address", command=func_address)

  def setup_toolbar(self):
    self.toolbar_menu = tk.Menu()
    self.configure(menu=self.toolbar_menu)

    self.file_dropdown = tk.Menu(master=self.toolbar_menu, tearoff=False)
    self.toolbar_menu.add_cascade(label="File", menu=self.file_dropdown)
    self.file_dropdown.add_command(label="Export Current Conditions", command= self.quit) #TODO change command
    self.file_dropdown.add_command(label="Import Conditions", command=self.quit)
    self.file_dropdown.add_command(label="Exit", command=lambda : exit(0))  # TODO change command

    self.analyze_dropdown = tk.Menu(master=self.toolbar_menu, tearoff=False)
    self.toolbar_menu.add_cascade(label="Analyze", menu=self.analyze_dropdown)
    #self.analyze_dropdown.add_command(label="By Sender Address") #maybe add these settings after somehow?
    #self.analyze_dropdown.add_command(label="By Sender Name")
    #self.analyze_dropdown.ch


  def make_text_input_frames(self, left_side_label : str, text_gray_hint: str, row: int):
    label = tk.Label(master= self.input_frame_grid, text=left_side_label)
    button_upload = tk.Button(master= self.input_frame_grid, text="Upload")
    button_clear = tk.Button(master= self.input_frame_grid, text="Clear")
    string_var = tk.StringVar()

    entry = entry_with_placeholder(text_hint=text_gray_hint, master= self.input_frame_grid, width=45)

    label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
    entry.grid(row=row, column=1, padx=5,pady=5)
    button_clear.grid(row=row, column=2, padx=5,pady=5)
    button_upload.grid(row=row, column=3, padx=5,pady=5)
    #frame.pack(pady=5)

    # label.grid(row=0, column=0, padx=5,pady=5)
    # entry.grid(row=0, column=1,padx=5, pady=5)
    # button_clear.grid(row=0, column=2,padx=5,pady=5)
    # button_upload.grid(row=0, column=3,padx=5,pady=5)
    # frame.grid(row=0, column=0, sticky="")
    # frame.grid_columnconfigure(0, weight=1)

    return [label, entry, string_var, button_clear, button_upload]

  def create_input_frame_dict(self, input_frame_vars : list) -> dict:
    '''
    Used to create dictionary used to access widgets inside input frames.
    :param input_frame_vars: @list output of make_text_input_frames function
    :return: @dict dictionary used to access widgets of each input frame where key is a string
              and value is the widget. i.e. temp_dict["label"] returns the label widget
    '''
    dict_inputs_keys = ["label", "entry", "string_var", "button_clear", "button_upload"]
    temp_dict = {}
    for i in range(len(dict_inputs_keys)):
      temp_dict[dict_inputs_keys[i]] = input_frame_vars[i]
    return temp_dict

  def make_text_input_date_frame(self,left_side_label : str, text_gray_hint: str, row: int):
    '''
    Used to make the date condition input frames
    :param left_side_label: @str the label denoting what entry will be
    :param text_gray_hint: @str hint showing intended input format
    :return: @list list of containing widgets
    '''

    #frame = tk.Frame(master=self)
    label = tk.Label(master=self.input_frame_grid, text=left_side_label)
    entry = entry_with_placeholder(text_hint=text_gray_hint, master=self.input_frame_grid, width=45)

    string_var = tk.StringVar()
    button_clear = tk.Button(master=self.input_frame_grid, text="Clear")

    label.grid(row=row, column=0, sticky="e",padx=5,pady=5)
    entry.grid(row=row, column=1,padx=5,pady=5)
    button_clear.grid(row=row, column=2,padx=5,pady=5)
    #frame.pack(pady=5)

    # label.place(relx=0, rely=1.0)
    # entry.place(relx=5)
    # button_clear.place(relx=10)
    # frame.pack(pady=5)

    return [label, entry, string_var, button_clear]

  def create_date_frame_dict(self, date_frame_widgets: list):
    dict_inputs_keys = ["label", "entry", "string_var", "button_clear"]
    temp_dict = {}
    for i in range(len(dict_inputs_keys)):
      temp_dict[dict_inputs_keys[i]] = date_frame_widgets[i]
    return temp_dict





def main():
  x = main_window()
  x.mainloop()

if __name__ == "__main__":
  main()