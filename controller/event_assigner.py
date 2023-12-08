import tkinter as tk
from view.entry_with_placeholder import entry_with_placeholder
class event_assigner():

  def assign_clear_entry(self,entry_widget_to_clear:entry_with_placeholder, clear_button: tk.Button):
    clear_button.configure(command=entry_widget_to_clear.clear_entry)


