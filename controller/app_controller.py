from model import cleanup_custom_exceptions, cleanup_model, inbox_analyzer, outlook_connection, date_handler
from view import tkinter_view
from view.tkinter_main_window import main_window
from event_assigner import event_assigner

class app_controller():

  def __init__(self):
    self.model = cleanup_model.cleanup_model()
    #self.inbox_analyzer = inbox_analyzer.inbox_analyzer()
    #self.outlook_connection = outlook_connection.outlook_connection() #starts connection
    #self.view = tkinter_view.tkinter_view()
    self.main_window = main_window()
    self.event_assigner = event_assigner()

  def assign_clear_buttons(self):
    input_dicts_list = [self.main_window.name_widgets_dict,
                        self.main_window.address_widgets_dict,
                        self.main_window.keywords_widgets_dict,
                        self.main_window.date_start_widgets_dict,
                        self.main_window.date_end_widgets_dict]
    for widget_dict in input_dicts_list:
      entry_widget = widget_dict["entry"]
      clear_button = widget_dict["button_clear"]
      self.event_assigner.assign_clear_entry(entry_widget, clear_button)


#TODO delete this func
def test_main_window():
  x = app_controller()
  x.assign_clear_buttons()
  x.main_window.mainloop()

  #test

def main():
  test_main_window()


if __name__ == "__main__":
  main()
