from model.constants import *

class inbox_analyzer():

    def __init__(self):
        self.unique_address_list = []
        self.unique_name_list = []
        self.address_tracker_dict = {}
        self.name_tracker_dict = {}

    def clear_trackers(self) -> None :
        '''
        Resets values stored in the tracker to empty.
        Run this after every analysis
        :return: None
        '''
        self.unique_address_list = []
        self.unique_name_list = []
        self.address_tracker_dict = {}
        self.name_tracker_dict = {}


    def record_individual_sender(self, sender_name: str) -> None:
        '''
        Stores sender names of an email item and counts how many times
        that sender has been encountered in the search. Sender names
        that match the email address will be ignored.
        :param sender_name: @str sender name of an email item
        :return: None
        '''
        #check if @ in name
        if '@' in sender_name:
            return
        if sender_name not in self.unique_name_list:
            self.unique_name_list.append(sender_name)
            self.name_tracker_dict[sender_name] = 1
        else:
            self.name_tracker_dict[sender_name] += 1

    def record_individual_email_address(self, email_address: str) -> None:
        '''
        Stores sender email addresses of an email item and counts how many times
        that email address has been encountered in the search
        :param email_address: @str sender email address.
        :return: None
        '''
        if email_address not in self.unique_address_list:
            self.unique_address_list.append(email_address)
            self.address_tracker_dict[email_address] = 1
        else:
            self.address_tracker_dict[email_address] += 1

    def write_sender_file(self,filename: str = 'sender_name_analysis.txt'):
        #sort dictionary by value
        self.name_tracker_dict = dict(sorted(self.name_tracker_dict.items(),key=lambda item: item[1],reverse=True))

        with open(filename, 'w') as file_writer:
            file_writer.write(SENDER_NAME_C + " : Qty Emails\n")
            for key, value in self.name_tracker_dict.items():
                file_writer.write(key + ' : ' + str(value) + '\n')

    def write_email_address_file(self, filename: str = 'sender_address_analysis.txt'):
        # sort address by value
        self.address_tracker_dict = dict(sorted(self.address_tracker_dict.items(), key=lambda item: item[1],reverse=True))

        with open(filename, 'w') as file_writer:
            file_writer.write(SENDER_ADDRESS_C + " : Qty Emails\n")
            for key, value in self.address_tracker_dict.items():
                file_writer.write(key + ' : ' + str(value) + '\n')




