import datetime
import unittest
from cleanup_model import cleanup_model
from date_handler import date_handler

class test_cleanup_model(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		'''
    Since the model is a singleton we will only
    run these methods once as opposed to running
    them before every test is run
    :return: None
    '''
		cls.model = cleanup_model()

	def tearDown(self) -> None:
		self.model.reset_deletion_conditions()

	def test_add_sender_email(self) -> None:
		'''
		Test adding emails. Must follow restrictions
		1.) NO duplicate emails added
		2.) No input accepted if input does NOT have '@' symbol
		3.) Ignores empty char or spaces as input
		:return:
		'''

		model = self.model
		sender_email_list_inputs = ["tEst@example.com", "Test@example.com","MissingAtSymbol","foO@bar.com", "\t",""," ","\n"]
		for email in sender_email_list_inputs:
			model.add_sender_email(email)

		self.assertEqual(2,len(model.target_sender_emails))
		self.assertEqual(['test@example.com', 'foo@bar.com'], model.target_sender_emails)

	def test_add_sender_name(self) -> None:
		'''
		Test adding sender names.
		Must follow restrictions:
		1.) NO duplicate names added
		2.) No input accepted if input DOES have '@' symbol
		3.) Ignores empty char or spaces as input
		:return:
		'''

		model = self.model
		sender_name_inputs = ["tEst", "Test", "John, Smith", "foO@bar.com", "\t", "",
																" ",
																"\n"]
		for sender in sender_name_inputs:
			model.add_sender_name(sender)

		self.assertEqual(2, len(model.target_sender_names))
		self.assertEqual(['test', 'john, smith'], model.target_sender_names)

	def test_add_subject_keyword(self):
		'''
		Testing adding subject keywords.
		Words with different casing will NOT count as different words
		:return:
		'''
		model = self.model

		example_words = "Hello World hello foobar I'm happy clap along dancing on quick sand"
		example_list = example_words.split(' ')

		for word in example_list:
			model.add_subject_keyword(word)

		self.assertEqual(11, len(model.target_subject_keyphrases))

		actual_list = ['hello', 'world', 'foobar', "i'm", 'happy', 'clap', 'along', 'dancing', 'on', 'quick', 'sand']
		self.assertEqual(actual_list, model.target_subject_keyphrases)


	def test_set_start_date(self):
		model = self.model
		model.set_start_date("01/01/1981")
		expected = datetime.datetime(1981, 1, 1, hour=0, minute=0, second=0,tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
		self.assertEqual(expected, model.target_start_date)

	def test_end_date(self):
		model = self.model
		model.set_end_date("7/14/2023")
		expected = datetime.datetime(2023, 7, 14, hour=23, minute=59, second=59,tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
		self.assertEqual(expected, model.target_end_date)

	def test_reset_deletion_conditions(self):
		model = self.model

		sender_email_list_inputs = ["tEst@example.com", "Test@example.com", "MissingAtSymbol", "foO@bar.com", "\t", "",
																" ",
																"\n"]
		for email in sender_email_list_inputs:
			model.add_sender_email(email)

		sender_name_inputs = ["tEst", "Test", "John, Smith", "foO@bar.com", "\t", "",
													" ",
													"\n"]

		for sender in sender_name_inputs:
			model.add_sender_name(sender)

		example_words = "Hello World hello foobar I'm happy clap along dancing on quick sand"
		example_list = example_words.split(' ')

		for word in example_list:
			model.add_subject_keyword(word)

		model.set_start_date("01/01/1981")
		model.set_end_date("7/14/2023")

		model.reset_deletion_conditions()

		self.assertEqual([],model.target_sender_emails)  # list of emails
		self.assertEqual(None, model.target_start_date)  # datetime obj
		self.assertEqual(None, model.target_end_date)  # datetime obj
		self.assertEqual([], model.target_subject_keyphrases)  # list of keyphrases
		self.assertEqual([], model.target_sender_names)  # list of sender names













def main():
	unittest.main(verbosity=3)

if __name__ == '__main__':
	main()

