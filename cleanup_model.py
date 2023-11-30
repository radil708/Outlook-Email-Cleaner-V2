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

    def add_sender_email(self, sender_email_in : str) -> None:
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

    def add_sender_name(self, sender_name_in : str):
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

    def add_subject_keyword(self, keyword_in: str):
        #TODO consider removing this feature??
        if keyword_in.isspace() or keyword_in == "":
            return
        if keyword_in not in self.target_subject_keyphrases:
            self.target_subject_keyphrases.append(keyword_in)


    def set_start_date(self, date_input: str) -> None:
        self.target_start_date = self.date_utility.convert_string_to_date(date_input)


    def set_end_date(self, date_input: str) -> None:
        self.target_end_date = self.date_utility.convert_string_to_date(date_input,endtime=True)

    def digest_input(self, user_input: str, delimiter: str):
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







