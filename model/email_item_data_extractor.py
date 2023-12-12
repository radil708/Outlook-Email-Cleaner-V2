import win32com.client as client
from datetime import datetime

class email_item_data_extractor():

  def extract_sender_address(self,email_item: client.CDispatch) -> str:
    address = email_item.SenderEmailAddress
    # TODO this might hit error if no string returned by attribute
    if address == None or address.isspace() or address == "":
      return " "
    else:
      return address.lower().strip()


  def extract_sender_name(self,email_item: client.CDispatch) -> str:
    name = email_item.SenderName
    if name == None or name.isspace() or name == "":
      return " "
    else:
      return name

  def extract_subject(self,email_item: client.CDispatch) -> str:
    email_subject = email_item.Subject

    if email_subject == None or email_subject.isspace() or email_subject == "":
      return " "
    else:
      return email_subject.lower().strip()

  def extract_timestamp(self,email_item: client.CDispatch) -> datetime:
    return datetime.fromtimestamp(email_item.SentOn.timestamp(), email_item.SentOn.tzinfo)