import tkinter as tk
from tkinter import ttk
from entry_with_placeholder import entry_with_placeholder

class main_window(tk.Tk):

  def __init__(self):
    tk.Tk.__init__(self)
    self.title("Ramzi's Email Deleter V2")
    self.geometry('550x200')
    self.eval('tk::PlaceWindow . center')

    self.name_widgets_dict = self.create_input_frame_dict(
      self.make_text_input_frames("Sender Name(s)","Doe, Jane | linkedIn | Advertising Company"))



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

    label.pack(side="left", padx=5)
    entry.pack(side="left", padx = 5)
    button_clear.pack(side="left", padx=5)
    button_upload.pack(side="left", padx=5)
    frame.pack(pady=10)

    return [frame, label, entry, string_var, button_clear, button_upload]

  def create_input_frame_dict(self, input_frame_vars : list):
    dict_inputs_keys = ["frame", "label", "entry", "string_var", "button_clear", "button_upload"]
    temp_dict = {}
    for i in range(len(dict_inputs_keys)):
      temp_dict[dict_inputs_keys[i]] = input_frame_vars[i]
    return temp_dict

def main():
  x = main_window()
  x.mainloop()

if __name__ == "__main__":
  main()