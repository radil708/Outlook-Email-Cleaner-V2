import tkinter as tk
from tkinter import ttk
from entry_with_placeholder import entry_with_placeholder

class main_window(tk.Tk):

  def __init__(self):
    tk.Tk.__init__(self)
    self.title("Ramzi's Email Deleter V2")
    self.geometry('600x300')
    self.eval('tk::PlaceWindow . center')
    self.header_label = tk.Label(master=self, text="Please Enter Deletion Conditions")
    self.header_label.pack(side="top")

    self.setup_toolbar()

    self.name_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Name(s):","Doe, Jane | linkedIn | Advertising Company"))

    self.address_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Email\nAddress(es):","ex@aol.com, state@us.gov, uni@eduroam.net")
    )

    self.keywords_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Keyword(s):", "hello, world, foo, bar")
    )

    self.date_start_widgets_dict = self.create_date_frame_dict(
      self.make_text_input_date_frame("Date Lower Boundary", "mm/dd/yyy")
    )

    self.date_end_widgets_dict = self.create_date_frame_dict(
      self.make_text_input_date_frame("Date Upper Boundary", "mm/dd/yyy")
    )

    # ["Sender Name(s)", "Doe, Jane | linkedIn | Advertising Company"], \
    # ["Sender Email Address(es):", "example@aol.com, state@us.gov, school@eduroam.net"],
    # ["Sender Key Word(s):", ]



  def setup_toolbar(self):
    self.toolbar_menu = tk.Menu()
    self.configure(menu=self.toolbar_menu)

    self.file_dropdown = tk.Menu(master=self.toolbar_menu, tearoff=False)
    self.toolbar_menu.add_cascade(label="File", menu=self.file_dropdown)
    self.file_dropdown.add_command(label="Export Current Conditions", command= self.quit) #TODO change command
    self.file_dropdown.add_command(label="Import Conditions", command=self.quit)

    self.analyze_dropdown = tk.Menu(master=self.toolbar_menu, tearoff=False)
    self.toolbar_menu.add_cascade(label="Analyze", menu=self.analyze_dropdown)
    self.analyze_dropdown.add_command(label="By Sender Address", command=self.quit) #maybe add these settings after somehow?
    self.analyze_dropdown.add_command(label="By Sender Name", command= self.quit)

  def make_text_input_frames(self, left_side_label : str, text_gray_hint: str):
    frame = tk.Frame(master=self)
    label = tk.Label(master=frame, text=left_side_label)
    button_upload = tk.Button(master=frame, text="Upload")
    button_clear = tk.Button(master=frame, text="Clear")
    string_var = tk.StringVar()

    entry = entry_with_placeholder(text_hint=text_gray_hint, master=frame, width=45)

    label.pack(side=tk.LEFT,padx=5)
    entry.pack(side=tk.LEFT, padx = 5,)
    button_clear.pack(side=tk.LEFT, padx=5)
    button_upload.pack(side=tk.LEFT, padx=5)
    frame.pack(pady=5)

    # label.grid(row=0, column=0, padx=5,pady=5)
    # entry.grid(row=0, column=1,padx=5, pady=5)
    # button_clear.grid(row=0, column=2,padx=5,pady=5)
    # button_upload.grid(row=0, column=3,padx=5,pady=5)
    # frame.grid(row=0, column=0, sticky="")
    # frame.grid_columnconfigure(0, weight=1)

    return [frame, label, entry, string_var, button_clear, button_upload]

  def create_input_frame_dict(self, input_frame_vars : list) -> dict:
    '''
    Used to create dictionary used to access widgets inside input frames.
    :param input_frame_vars: @list output of make_text_input_frames function
    :return: @dict dictionary used to access widgets of each input frame where key is a string
              and value is the widget. i.e. temp_dict["label"] returns the label widget
    '''
    dict_inputs_keys = ["frame", "label", "entry", "string_var", "button_clear", "button_upload"]
    temp_dict = {}
    for i in range(len(dict_inputs_keys)):
      temp_dict[dict_inputs_keys[i]] = input_frame_vars[i]
    return temp_dict

  def make_text_input_date_frame(self,left_side_label : str, text_gray_hint: str):
    '''
    Used to make the date condition input frames
    :param left_side_label: @str the label denoting what entry will be
    :param text_gray_hint: @str hint showing intended input format
    :return: @list list of containing widgets
    '''

    frame = tk.Frame(master=self)
    label = tk.Label(master=frame, text=left_side_label)
    entry = entry_with_placeholder(text_hint=text_gray_hint, master=frame, width=45)
    string_var = tk.StringVar()
    button_clear = tk.Button(master=frame, text="Clear")

    label.pack(side=tk.LEFT, padx=5)
    entry.pack(side="left", padx=5)
    button_clear.pack(side="left", padx=5)
    frame.pack(pady=5)

    # label.place(relx=0, rely=1.0)
    # entry.place(relx=5)
    # button_clear.place(relx=10)
    # frame.pack(pady=5)

    return [frame, label, entry, string_var, button_clear]

  def create_date_frame_dict(self, date_frame_widgets: list):
    dict_inputs_keys = ["frame", "label", "entry", "string_var", "button_clear"]
    temp_dict = {}
    for i in range(len(dict_inputs_keys)):
      temp_dict[dict_inputs_keys[i]] = date_frame_widgets[i]
    return temp_dict





def main():
  x = main_window()
  x.mainloop()

if __name__ == "__main__":
  main()