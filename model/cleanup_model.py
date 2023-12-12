import tkinter
from tkinter import filedialog
import os
from model.date_handler import date_handler


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

        self.or_conditions_to_check = []
        self.and_conditions_to_check = []

    def reset_deletion_conditions(self):
        '''
        Clears out all deletion parameters. This will be called after every round of deletion.
        :return: None
        '''
        self.target_sender_emails = []
        self.target_start_date = None
        self.target_end_date = None
        self.target_subject_keyphrases = []
        self.target_sender_names = []

        self.or_conditions_to_check = []
        self.and_conditions_to_check = []

    def add_individual_sender_email(self, sender_email_in : str) -> None:
        '''
        Adds one individual email to the the target_sender_emails list attribute.
        Ignores empty spaces or input WITHOUT "@" symbol and converts input to lower case. This is done
        because emails ignore casing.
        :param sender_email_in: @str A single email to delete
        :return:None
        '''
        if sender_email_in.isspace() or sender_email_in == "" or "@" not in sender_email_in:
            return
        if sender_email_in.lower() not in self.target_sender_emails:
            self.target_sender_emails.append(sender_email_in.lower())

    def add_individual_sender_name(self, sender_name_in : str) -> None:
        '''
        Adds one individual sender name to the target_sender_names list attribute.
        Ignores empty spaces or names WITH "@" symbol. This is because some emails
        have an email address and name that are the same.
        :param sender_name_in: @str the name of the sender of an email you want to delete
        :return: None
        '''
        if sender_name_in.isspace() or sender_name_in == "" or "@" in sender_name_in:
            return
        if sender_name_in.lower() not in self.target_sender_names:
            self.target_sender_names.append(sender_name_in.lower())

    def add_individual_subject_keyword(self, keyword_in: str) -> None:
        '''
        Adds one individual keyword to the target_subject_keyphrases list. It ignores
        empty spaces.
        :param keyword_in: @str a word to that will be searched for in the subject line of an email
        :return: None
        '''
        #TODO consider removing this feature??
        if keyword_in.isspace() or keyword_in == "":
            return
        if keyword_in not in self.target_subject_keyphrases:
            self.target_subject_keyphrases.append(keyword_in.lower())


    def set_start_date(self, date_input: str) -> None:
        '''
        Sets the target_start_date attribute. Takes a date as a string and converts
        it to datetime where the time is at 00:00 of that particular day.
        :param date_input: @str A representation of a date in the format mm/dd/yyyy
        :return: None
        '''
        if date_input.isspace() or date_input == "" or date_input == None:
            return
        else:
            self.target_start_date = self.date_utility.convert_string_to_date(date_input)


    def set_end_date(self, date_input: str) -> None:
        '''
        Sets the target_end_date attribute. Takes a date as a string and converts it to datetime
        where the time is at 23:59 of that particular day.
        :param date_input: @str A representation of a date in the format mm/dd/yyyy
        :return: None
        '''
        if date_input.isspace() or date_input == "" or date_input == None:
            return
        else:
            self.target_end_date = self.date_utility.convert_string_to_date(date_input,endtime=True)

    def is_address_in_target_list(self, email_address: str) -> bool:
        '''
        Checks to see if the param email_address is in the list of target_sender_emails list i.e.
        Returns true if the email address belongs to an email that should be deleted.
        :param email_address: @str the email address of the sender of an email
        :return: @bool True if the email is in the target_sender_emails list, false otherwise
        '''
        email_address = email_address.lower().strip()
        if email_address in self.target_sender_emails:
            return True
        else:
            return False

    def is_name_in_target_list(self, sender_name: str) -> bool:
        '''
        Checks to see if the param sender_name is in the list of target_sender_names list i.e.
        Returns true if the email address belongs to an email that should be deleted.
        :param sender_name: @str the name of a peron/org who sent an email.
        :return: @bool True if the email is in the target_sender_names list, false otherwise
        '''
        sender_name = sender_name.lower().strip()
        if sender_name in self.target_sender_names:
            return True
        else:
            return False

    def is_any_key_word_in_subject(self, subject_str: str) -> bool:
        '''
        Splits a subject of an email by space. Checks if any word in the subject line
        matches a word in the target_subject_keyphrases attribute.
        :param subject_str: @str the subject of an email
        :return: @bool True is any word in the subject matches a word in the target_subject_keyphrases, false otherwise
        '''
        #breakdown subject into a sentence i.e. split by space
        subject_as_list = self.digest_input(subject_str, ' ', apply_lower=True)
        #returns True if any element in target keyphrases exist in the subject
        return any(element in self.target_subject_keyphrases for element in subject_as_list)


    def digest_input(self, user_input: str, delimiter: str, apply_lower: bool = False) -> list:
        '''
        Will be used to convert a long string of user input into a list of individual string elements.
        i.e. 'Tony@eduroam.net, Steve@umass.edu, Natasha@russia.gov' -> ['Tony@eduroam.net','Steve@umass.edu','Natasha@russia.gov']
        It is a helper function that will be used in processing user input.
        Split by delimiter and removes leading and lagging spaces.
        :param user_input: @str A string containing some delimiter char that is placed between words.
        :param delimiter: @str the char that marks how the elements will be split. For email addresses and keywords
            it will be comma. For names, it will be the pipe char i.e. "|".
        :return: @list list of strings representing individual elements of the user input.
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
        Grabs the filepath of selected file. Helper function to import_setting_file.
        :return: @str string representation of file to path
        '''

        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing

        folder_path = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file")

        return folder_path

    def import_setting_file(self, filepath : str) -> list:
        '''
        Opens selected file and grabs relevant info. I.e.
        split by ":", strips leading and lagging spaces and returns
        list of element (all to the left of ":")
        :param filepath: @str file path
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

        if user_input.isspace() or user_input == "" or user_input == None:
            return
        delimited_user_choices = self.digest_input(user_input, delimiter=',', apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_sender_email(choice)

    def add_all_sender_names(self, user_input: str):
        if user_input.isspace() or user_input == "" or user_input == None:
            return
        delimited_user_choices = self.digest_input(user_input,delimiter="|", apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_sender_name(choice)


    def add_all_keywords(self, user_input: str):
        # TODO test
        if user_input.isspace() or user_input == "" or user_input == None:
            return
        delimited_user_choices = self.digest_input(user_input, delimiter=',', apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_subject_keyword(choice)

    def add_raw_user_date(self, user_input : dict):
        #TODO test
        '''

        :param user_input: @list the output of get_all_entries from tkinter_main_window.py
        :return:
        '''

        self.add_all_sender_names(user_input["names"])
        self.add_all_sender_emails(user_input["email addresses"])
        self.add_all_keywords(user_input["keywords"])
        self.set_start_date(user_input["start date"])
        self.set_end_date(user_input["end date"])






