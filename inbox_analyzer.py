

class inbox_analyzer():

    def __init__(self):
        self.unique_address_list = []
        self.unique_name_list = []
        self.address_tracker_dict = {}
        self.name_tracker_dict = {}

    def clear_trackers(self):
        self.unique_address_list = []
        self.unique_name_list = []
        self.address_tracker_dict = {}
        self.name_tracker_dict = {}

    """
    check name, if @ in then ignore else add to name
    """

    def track_sender(self, sender_name: str):
        #check if @ in name
        if '@' in sender_name:
            return
        if sender_name not in self.unique_name_list:
            self.unique_name_list.append(sender_name)
            self.name_tracker_dict[sender_name] = 1
        else:
            self.name_tracker_dict[sender_name] += 1

    def track_email_address(self, email_address: str):
        if email_address not in self.unique_address_list:
            self.unique_address_list.append(email_address)
            self.address_tracker_dict[email_address] = 1
        else:
            self.address_tracker_dict[email_address] += 1

    def write_sender_file(self,filename: str = 'sender_name_analysis.txt'):
        #sort dictionary by value
        self.name_tracker_dict = dict(sorted(self.name_tracker_dict.items(),key=lambda item: item[1],reverse=True))

        with open(filename, 'w') as file_writer:
            for key, value in self.name_tracker_dict.items():
                file_writer.write(key + ' : ' + str(value) + '\n')

    def write_email_address_file(self, filename: str = 'sender_address_analysis.txt'):
        # sort address by value
        self.address_tracker_dict = dict(sorted(self.address_tracker_dict.items(), key=lambda item: item[1],reverse=True))

        with open(filename, 'w') as file_writer:
            for key, value in self.address_tracker_dict.items():
                file_writer.write(key + ' : ' + str(value) + '\n')




