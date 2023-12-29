import win32com.client as client

import model.date_handler
from model.email_item_data_extractor import email_item_data_extractor
from model.cleanup_custom_exceptions import *
from model.date_handler import date_handler

class email_item_test_class():
  '''
  This class exists to help Test the capabilities of the model.
  '''

  def __init__(self):
    self.date_util = date_handler()

  def set_string_attributes(self, name='', address ='', subject=''):
    self.SenderName = name
    self.SenderEmailAddress = address
    self.Subject = subject

  def clear_string_attributes(self):
    self.SenderName = ''
    self.SenderEmailAddress = ''
    self.Subject = ''

  def set_date(self, year=2011, month=2, day=22):
    # sent_on_string =''
    # month_str = str(month)
    #
    # if len(month_str) < 2:
    #   month_str = '0' + month_str
    #
    # day_str = str(day)
    # if len(day_str) < 2:
    #   day_str = '0' + day_str
    #
    # self.SentOn = f"{year}-{month_str}-{day_str} 11:35:10+00:00"
    date_str = f"{str(month)}/{str(day)}/{str(year)}"
    self.SentOn = self.date_util.convert_string_to_date(date_str)

  def clear_date_attribute(self):
    self.SentOn = None

  def clear_all_attributes(self):
    self.SenderName = ''
    self.SenderEmailAddress = ''
    self.Subject = ''
    self.SentOn = None
