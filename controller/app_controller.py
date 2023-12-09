from model import cleanup_custom_exceptions, cleanup_model, inbox_analyzer, outlook_connection, date_handler
from view import tkinter_view
from view.tkinter_main_window import main_window
from view.tkinter_welcome_window import welcome_window
from event_assigner import event_assigner

TEST = True

class app_controller():

  def __init__(self):
    self.model = cleanup_model.cleanup_model()
    self.main_window = None
    #self.inbox_analyzer = inbox_analyzer.inbox_analyzer()
    #self.outlook_connection = outlook_connection.outlook_connection() #starts connection
    #self.view = tkinter_view.tkinter_view()

    #TODO right code to get users from outlook
    self.outlook_user_test = ["e1","e2"]

    self.welcome_window = None
    self.event_assigner = event_assigner()

  def assign_analyze_by_name(self):
    self.main_window.analyze_dropdown.set

  def assign_clear_buttons(self):
    '''
    Link the clear button widget to function
    :return:
    '''
    input_dicts_list = [self.main_window.name_widgets_dict,
                        self.main_window.address_widgets_dict,
                        self.main_window.keywords_widgets_dict,
                        self.main_window.date_start_widgets_dict,
                        self.main_window.date_end_widgets_dict]
    for widget_dict in input_dicts_list:
      entry_widget = widget_dict["entry"]
      clear_button = widget_dict["button_clear"]
      self.event_assigner.assign_clear_entry(entry_widget, clear_button)

    return

  def open_welcome_window(self):
    '''
    function that starts
    :return:
    '''
    if self.main_window != None:
      self.main_window.destroy()

    self.welcome_window = welcome_window(self.outlook_user_test)
    self.welcome_window.select_button.configure(command=self.pass_user_choice_to_main_window)
    self.welcome_window.mainloop()

  def pass_user_choice_to_main_window(self, *args):
    '''
    Links welcome window to main window
    :param args:
    :return:
    '''
    current_user = self.welcome_window.user_selection_var.get()
    #TODO RIGHT CODE HERE TO PASS INTO OUTLOOK CONNECTION
    self.welcome_window.quit()
    self.welcome_window.destroy()
    self.welcome_window = None
    self.main_window = main_window()
    self.main_window.set_current_account_label(current_user)
    self.assign_clear_buttons()
    self.main_window.switch_act_button.configure(command=self.go_back_to_select_accounts_command)
    self.main_window.mainloop()

  def go_back_to_select_accounts_command(self):
    '''
    links main_window to welcome_window
    :return:
    '''
    if self.main_window != None:
      self.main_window.quit()
    self.open_welcome_window()

  def assign_select_button(self):
    pass

#TODO delete this func
def test_main_window():
  x = app_controller()
  x.assign_clear_buttons()
  x.main_window.mainloop()

def test_link_welcome_to_main():
  y = app_controller()
  y.open_welcome_window()

  #test

def main():
  test_link_welcome_to_main()


if __name__ == "__main__":
  main()
