import tkinter
from tkinter import filedialog
import os
from model.date_handler import date_handler
import win32com.client as client
from model.email_item_data_extractor import email_item_data_extractor
from model.cleanup_custom_exceptions import *
from model.constants import *

class cleanup_model():

    def __init__(self):

        self.data_extractor_utility = email_item_data_extractor()

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

    def print_conditions(self):
        '''
        Helper functions for tests, not used in model
        :return:
        '''
        print(f"Target Names: {self.target_sender_names}")
        print(f"Target Emails: {self.target_sender_emails}")
        print(f"Target Keywords: {self.target_subject_keyphrases}")
        print(f"Target Start Date: {self.target_start_date}")
        print(f"Target End Date: {self.target_end_date}")
        print("--------------------------")

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
            try:
                self.target_start_date = self.date_utility.convert_string_to_date(date_input)
            except ValueError:
                raise DateConversionError

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
            try:
                self.target_end_date = self.date_utility.convert_string_to_date(date_input,endtime=True)
            except ValueError:
                raise DateConversionError
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

    def check_email_address(self,email_item: client.CDispatch) -> bool:
        # TODO Test
        return self.is_address_in_target_list(self.data_extractor_utility.extract_sender_address(email_item))

    def is_name_in_target_list(self, sender_name: str) -> bool:
        '''
        Checks to see if the param sender_name is in the list of target_sender_names list i.e.
        Returns true if the email address belongs to an email that should be deleted.
        Helper function to check_email_name
        :param sender_name: @str the name of a peron/org who sent an email.
        :return: @bool True if the email is in the target_sender_names list, false otherwise
        '''
        sender_name = sender_name.lower().strip()
        if sender_name in self.target_sender_names:
            return True
        else:
            return False

    def check_email_name(self,email_item: client.CDispatch) -> bool:
        #TODO Test
        '''

        :param email_item:
        :return:
        '''
        return self.is_name_in_target_list(self.data_extractor_utility.extract_sender_name(email_item))

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

    def check_subject(self, email_item: client.CDispatch) -> bool:
        return self.is_any_key_word_in_subject(self.data_extractor_utility.extract_subject(email_item))

    def is_email_between_dates(self, email_item: client.CDispatch) -> bool:
        if self.are_both_date_conditions_filled() is False:
            raise RuntimeError("Both dates must be set")
        email_date = self.data_extractor_utility.extract_timestamp(email_item)
        return self.date_utility.is_between_dates(self.target_start_date, self.target_end_date, email_date)


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

        folder_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")

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
        # TODO Test
        if user_input.isspace() or user_input == "" or user_input == None:
            return
        delimited_user_choices = self.digest_input(user_input, delimiter=',', apply_lower=True)
        for choice in delimited_user_choices:
            self.add_individual_subject_keyword(choice)

    def add_raw_user_data(self, user_input : dict) -> None:
        '''
        Takes in user input in the form of a dictionary and splits it
        into specific condition lists used by this program to determine
        what to check against when searching for emails.
        :param user_input: @list the output of get_all_entries from tkinter_main_window.py
        :return: None
        '''

        self.add_all_sender_names(user_input["names"])
        self.add_all_sender_emails(user_input["email addresses"])
        self.add_all_keywords(user_input["keywords"])
        self.set_start_date(user_input["start date"])
        self.set_end_date(user_input["end date"])

    def are_conditions_empty(self) -> bool:
        '''
        Returns True if no conditions were added by the user. This function
        is used as a flag to prevent the user from accidentally deleting
        all emails in their inbox.
        :return: @bool True if no conditions are set, False otherwise
        '''

        if self.target_sender_emails == [] and self.target_start_date == None \
            and self.target_end_date == None  and self.target_subject_keyphrases == [] \
            and self.target_sender_names == []:
            return True
        else:
            return False

    def is_only_one_date_condition_filled(self) -> bool:
        '''
        Helper function to run_condition_check.
        This function is used to check if only one date condition was filled.
        In order for the program to run, either both date conditions must be
        set or no date conditions must be set.
        :return: @bool True if only one date condition (start or end) was filled,
                    False otherwise
        '''
        if (self.target_start_date != None and self.target_end_date == None) \
            or (self.target_end_date != None and self.target_start_date == None):
            return True
        else:
            return False



    def are_both_date_conditions_filled(self):
        '''
        Helper function to  run_condition_check.
        :return:
        '''
        if self.target_start_date == None or self.target_end_date == None:
            return False
        else:
            return True

    def setup_condition_checks(self):
        #TODO Test and run before run_condition_check
        '''
        This function determines which functions are used to check the
        attributes of an email when finding emails that match user set conditions.
        This MUST be called before calling run_condition_checks
        :return:
        '''
        if self.target_sender_emails != []:
            self.or_conditions_to_check.append(self.check_email_address)
        if self.target_sender_names != []:
            self.or_conditions_to_check.append(self.check_email_name)
        if self.target_subject_keyphrases != []:
            self.or_conditions_to_check.append(self.check_subject)

    def run_condition_check(self, email_item) -> bool:
        '''
        This is the actual function used to check if an email matches
        any user set conditions.
        :param email_item: @client.CDispatch the email the program is looking at to see
                                it matches the the conditions set by the user
        :return: @bool True if the email contains attributes that match
                    the target conditions for deletion as set by the user.
        '''
        or_match = False
        date_match = False

        #If only dates are used then ignore names, address, keywords
        if len(self.or_conditions_to_check) == 0:
            or_match = True
        else:
            for each in self.or_conditions_to_check:
                or_match = each(email_item)
                if or_match == True:
                    break

        #If no dates are used then ignore dates as a conditions
        if self.are_both_date_conditions_filled() is False:
            date_match = True
        else:
            #TODO need to have a date check function
            date_match = self.is_email_between_dates(email_item)

        return or_match and date_match

    def extract_info_from_analysis_file(self, filepath: str) -> tuple:
        #filepath = self.select_file()
        #Todo add a loading??
        list_keep = []
        line_counter = 0
        type= ''
        with open(filepath, "r") as filereader:
            for line in filereader.readlines():
                if line_counter == 0:
                    line_split = line.split(":")
                    type = line_split[0].strip()
                else:
                    line_split = line.split(":")
                    list_keep.append(line_split[0].strip())
                line_counter+= 1

        output = ''

        if type == SENDER_NAME_C:
            output = ' | '.join(list_keep)
        else:
            output = ' , '.join(list_keep)

        return type, output

















