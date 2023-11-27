import win32com.client as client
from inbox_analyzer import inbox_analyzer
import time


'''
email item properties:
    sender_name = email_item.SenderName
    sender_address = email_item.SenderEmailAddress
    date = email_item.SentOn.timestamp()
'''

class outlook_connection():

    def __init__(self):

        ################## SETTING UP VARIABLES ##################
        self.com_obj = None
        self.outlook_connection = None
        self.user_email = None
        self.mailbox = None

        self.all_available_users = [] #list that will contain all users

        ################## STARTUP FUNCTIONS ##################
        self.connect_to_outlook()
        self.fill_in_all_users_list()



    def __new__(cls):
        """
        This is used to enforce the singleton pattern. If a cleanup_model instance
        has already been created, then it will return the instance and not
        a new instance, otherwise it will create a new instance of cleanup_model
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(outlook_connection, cls).__new__(cls)
        return cls.instance

    def connect_to_outlook(self):
        # Connect to Application
        self.com_obj = client.Dispatch("Outlook.Application")
        self.outlook_connection = self.com_obj.GetNameSpace('MAPI')

    def fill_in_all_users_list(self):

        if self.all_available_users == []:
            for user_email in self.outlook_connection.Folders:
                # filter out non-emails i.e. Internet Calendar
                if '@' in user_email.Name:
                    self.all_available_users.append(user_email.Name)

        return self.all_available_users

    def set_user(self,user_email: str):
        #TODO write error if user_email not in list

        self.user_email = user_email
        self.set_mailbox()

    def set_mailbox(self):
        #Helper function to set_user
        #TODO if user_email is None raise error
        self.mailbox = self.outlook_connection.\
            Folders(self.user_email).Folders('Inbox').Items
        #iterate through this list to get all emails

    def get_all_emails_from_inbox(self):
        pass

    def delete_email(self):
        pass

    def close_connection(self):
        #self.com_obj.Close()
        self.com_obj.Quit()
        del self.com_obj
        self.com_obj = None
        #os.system('taskkill /im outlook.exe /f')

def main():
    x = outlook_connection()
    x.set_user('adil.r@northeastern.edu')
    x.set_mailbox()
    counter = 0
    y = inbox_analyzer()

    inbox_length = len(x.mailbox)

    for email in x.mailbox:
        counter += 1
        item_name = email.SenderName
        item_address = email.SenderEmailAddress
        print(f"{counter} of {inbox_length}", end='')
        y.track_sender(item_name)
        y.track_email_address(item_address)
        if 500 % counter == 0:
            time.sleep(0.1)
        print('\r', end='')

    print(f"Read through {counter} emails")
    print(f"sum of email addresses = {sum(y.address_tracker_dict.values())}")
    y.write_sender_file()
    y.write_email_address_file()

    x.close_connection()
    print("closing")

    exit(0)



if __name__ == '__main__':
    main()