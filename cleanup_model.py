import datetime
import tkinter
from tkinter import filedialog
import os
from date_handler import date_handler
from cleanup_custom_exceptions import *

class cleanup_model():

    def __init__(self):

        self.date_utility = date_handler()

        ################ variables relating to deleting conditions ################
        self.target_sender_emails = [] # list of emails
        self.target_start_date = None  # datetime obj
        self.target_end_date = None  # datetime obj
        self.target_subject_keyphrases = []  # list of keyphrases
        self.target_sender_names = []  # list of sender names

        """
        NOTE*: target_sender_name and target_sender_email are not the same. For example,
        an email can have the sender be LinkedIn but that same sender could be linked
        to multiple email addresses like linkedinjobs@linkedin.com & linkedinnotifications@linkedin.com
        for example. So targeting by the sender would remove the need to search for two 
        different addresses
        """

    def reset_deletion_conditions(self):
        self.target_sender_emails = []
        self.target_start_date = None
        self.target_end_date = None
        self.target_subject_keyphrases = []
        self.target_sender_names = []

    def add_individual_sender_email(self, sender_email_in : str) -> None:
        '''
        Adds one individual email to the the target_sender_emails list attribute.
        Ignores empty spaces or input WITHOUT "@" symbol and converts input to lower case. This is done
        because emails ignore casing.
        :param sender_email_in:
        :return:
        '''
        if sender_email_in.isspace() or sender_email_in == "" or "@" not in sender_email_in:
            return
        if sender_email_in.lower() not in self.target_sender_emails:
            self.target_sender_emails.append(sender_email_in.lower())

    def add_individual_sender_name(self, sender_name_in : str):
        '''
        Adds one individual sender name to the target_sender_emails list attribute.
        Ignores empty spaces or names WITH "@" symbol. This is because some emails
        have an email address and name that are the same.
        :param sender_name_in:
        :return:
        '''
        if sender_name_in.isspace() or sender_name_in == "" or "@" in sender_name_in:
            return
        if sender_name_in.lower() not in self.target_sender_names:
            self.target_sender_names.append(sender_name_in.lower())

    def add_individual_subject_keyword(self, keyword_in: str):
        #TODO consider removing this feature??
        if keyword_in.isspace() or keyword_in == "":
            return
        if keyword_in not in self.target_subject_keyphrases:
            self.target_subject_keyphrases.append(keyword_in.lower())


    def set_start_date(self, date_input: str) -> None:
        self.target_start_date = self.date_utility.convert_string_to_date(date_input)


    def set_end_date(self, date_input: str) -> None:
        self.target_end_date = self.date_utility.convert_string_to_date(date_input,endtime=True)

    def is_address_in_target_list(self, email_address: str) -> bool:
        email_address = email_address.lower().strip()
        if email_address in self.target_sender_emails:
            return True
        else:
            return False

    def is_name_in_target_list(self, sender_name: str) -> bool:
        sender_name = sender_name.lower().strip()
        if sender_name in self.target_sender_names:
            return True
        else:
            return False

    def is_any_key_word_in_subject(self, subject_str: str) -> bool:
        #breakdown subject into a sentence i.e. split by space
        subject_as_list = self.digest_input(subject_str, ' ', apply_lower=True)
        #returns True if any element in target keyphrases exist in the subject
        return any(element in self.target_subject_keyphrases for element in subject_as_list)


    def digest_input(self, user_input: str, delimiter: str, apply_lower: bool = False):
        '''
        Will be used to convert a long string of user input into a list.
        Split by delimiter and removes leading and lagging spaces.
        :param user_input:
        :param delimiter:
        :return:
        '''

        digested_list = []

        split_input = user_input.split(delimiter)

        for input_element in split_input:
            input_element = input_element.strip()

            if apply_lower is True:
                input_element = input_element.lower()

            digested_list.append(input_element)

        return digested_list

    def select_file(self) -> str:
        '''
        Grabs the filepath of selected file
        :return:
        '''

        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing

        folder_path = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file")

        return folder_path

    def import_setting_file(self, filepath : str):
        '''
        Opens selected file and grabs relevant info. I.e.
        split by ":", strips leading and lagging spaces and returns
        list of element (all to the left of ":")
        :param filepath:
        :return:
        '''

        setting_as_list = []

        with open(filepath, "r") as setting_reader:
            for line in setting_reader.readlines():
                processed_line_list = line.split(":")
                setting_as_list.append(processed_line_list[0].strip())

        return setting_as_list

    def convert_list_to_user_input(self, setting_input_list: list, join_char: str) -> str:
        #TODO make one specifically for name and email address?
        return join_char.join(setting_input_list)

    def add_all_sender_emails(self, user_input: str):
        '''
        User input will be a string coming from user
        in format email_1, email_2, ... etc.
        :param user_input:
        :return:
        '''

        delimited_user_choices = self.digest_input(user_input, delimiter=',', apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_sender_email(choice)

    def add_all_sender_names(self, user_input: str):
        delimited_user_choices = self.digest_input(user_input,delimiter="|", apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_sender_name(choice)








