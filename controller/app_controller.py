from model import cleanup_custom_exceptions, cleanup_model, inbox_analyzer, outlook_connection, date_handler
from view import tkinter_view

class app_controller():

  def __init__(self):
    self.model = cleanup_model.cleanup_model()
    self.inbox_analyzer = inbox_analyzer.inbox_analyzer()
    self.outlook_connection = outlook_connection.outlook_connection() #starts connection
    self.view = tkinter_view.tkinter_view()

  def coordinate_select_user_email(self):
    '''
    First part of program
    :return:
    '''
    self.view.build_welcome_window(self.outlook_connection.all_available_users)
    self.view.welcome_window.mainloop()

  def run(self):
    self.coordinate_select_user_email()
    self.outlook_connection.set_user(self.view.get_user_email_choice())


  #test

def main():
  controller = app_controller()
  controller.coordinate_select_user_email()

if __name__ == "__main__":
  main()
