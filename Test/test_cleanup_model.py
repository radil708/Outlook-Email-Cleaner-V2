import datetime
import unittest
from model.cleanup_model import cleanup_model
from model.cleanup_custom_exceptions import *
from Test.email_item_test_class import email_item_test_class


class test_cleanup_model(unittest.TestCase):

  @classmethod
  def setUpClass(cls) -> None:
    '''
    Since the model is a singleton we will only
    run these methods once as opposed to running
    them before every Test is run
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
    sender_email_list_inputs = ["tEst@example.com", "Test@example.com", "MissingAtSymbol", "foO@bar.com", "\t", "", " ",
                                "\n"]
    for email in sender_email_list_inputs:
      model.add_individual_sender_email(email)

    self.assertEqual(2, len(model.target_sender_emails))
    self.assertEqual(['Test@example.com', 'foo@bar.com'], model.target_sender_emails)

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
      model.add_individual_sender_name(sender)

    self.assertEqual(2, len(model.target_sender_names))
    self.assertEqual(['Test', 'john, smith'], model.target_sender_names)

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
      model.add_individual_subject_keyword(word)

    self.assertEqual(11, len(model.target_subject_keyphrases))

    actual_list = ['hello', 'world', 'foobar', "i'm", 'happy', 'clap', 'along', 'dancing', 'on', 'quick', 'sand']
    self.assertEqual(actual_list, model.target_subject_keyphrases)

  def test_set_start_date(self):
    model = self.model
    model.set_start_date("01/01/1981")
    expected = datetime.datetime(1981, 1, 1, hour=0, minute=0, second=0,
                                 tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
    self.assertEqual(expected, model.target_start_date)

  def test_end_date(self):
    model = self.model
    model.set_end_date("7/14/2023")
    expected = datetime.datetime(2023, 7, 14, hour=23, minute=59, second=59,
                                 tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
    self.assertEqual(expected, model.target_end_date)

  def test_reset_deletion_conditions(self):
    model = self.model

    sender_email_list_inputs = ["tEst@example.com", "Test@example.com", "MissingAtSymbol", "foO@bar.com", "\t", "",
                                " ",
                                "\n"]
    for email in sender_email_list_inputs:
      model.add_individual_sender_email(email)

    sender_name_inputs = ["tEst", "Test", "John, Smith", "foO@bar.com", "\t", "",
                          " ",
                          "\n"]

    for sender in sender_name_inputs:
      model.add_individual_sender_name(sender)

    example_words = "Hello World hello foobar I'm happy clap along dancing on quick sand"
    example_list = example_words.split(' ')

    for word in example_list:
      model.add_individual_subject_keyword(word)

    model.set_start_date("01/01/1981")
    model.set_end_date("7/14/2023")

    model.reset_deletion_conditions()

    self.assertEqual([], model.target_sender_emails)  # list of emails
    self.assertEqual(None, model.target_start_date)  # datetime obj
    self.assertEqual(None, model.target_end_date)  # datetime obj
    self.assertEqual([], model.target_subject_keyphrases)  # list of keyphrases
    self.assertEqual([], model.target_sender_names)  # list of sender names

  def test_is_address_in_list(self):
    model = self.model

    sender_email_list_inputs = ["tEst@example.com", "Test@example.com", "MissingAtSymbol", "foO@bar.com", "\t", "",
                                " ",
                                "\n"]
    for email in sender_email_list_inputs:
      model.add_individual_sender_email(email)

    self.assertTrue(model.is_address_in_target_list('teSt@example.com'))
    self.assertTrue(model.is_address_in_target_list('Foo@Bar.com'))

    self.assertFalse(model.is_address_in_target_list("Kylo@StarWars.net"))

  def test_is_name_in_list(self):
    model = self.model

    sender_name_inputs = ["tEst", "Test", "John, Smith", "foO@bar.com", "\t", "",
                          " ",
                          "\n"]
    for sender in sender_name_inputs:
      model.add_individual_sender_name(sender)

    self.assertTrue(model.is_name_in_target_list('john, smith'))
    self.assertTrue(model.is_name_in_target_list('teSt'))
    self.assertFalse(model.is_name_in_target_list('John, Connor'))

  def test_is_any_key_word_in_subject(self):
    model = self.model

    example_words = "Theresa thought that I ate the apple"
    example_list = example_words.split(' ')

    for word in example_list:
      model.add_individual_subject_keyword(word)

    # Check that "There" is not mistaken for similarly spelled words like "Theresa"
    self.assertFalse(model.is_any_key_word_in_subject("There once was a sailor"))
    self.assertTrue(model.is_any_key_word_in_subject("Theresa saw the sailor"))

  def test_add_all_sender_emails(self):
    model = self.model
    test_input = "tEst@example.com, Test@example.com, MissingAtSymbol, foO@bar.com, \t, \"\", \" \", \"\n, email_2@aol.net"

    model.add_all_sender_emails(test_input)
    expected_list = ["Test@example.com", "foo@bar.com", "email_2@aol.net"]
    self.assertEqual(expected_list, model.target_sender_emails)
    self.assertTrue("Test@example.com" in model.target_sender_emails)
    self.assertTrue("email_2@aol.net" in model.target_sender_emails)
    self.assertTrue("foo@bar.com" in model.target_sender_emails)

  def test_add_all_sender_names(self):
    model = self.model
    sender_name_inputs = "tEst | Test| John, Smith |foO@bar.com| Alice\t|\nlinkedIn |\t|| |\n"
    model.add_all_sender_names(sender_name_inputs)
    expected_list = ["Test", "john, smith", "alice", "linkedin"]

    self.assertTrue("Test" in model.target_sender_names)
    self.assertTrue("john, smith" in model.target_sender_names)
    self.assertTrue("linkedin" in model.target_sender_names)
    self.assertTrue("alice" in model.target_sender_names)
    self.assertEqual(expected_list, model.target_sender_names)

  def test_add_all_keywords(self):
    model = self.model
    keyword_inputs = "Hello, world , foo,bar "
    expected_list = ["hello", "world", "foo", "bar"]
    model.add_all_keywords(keyword_inputs)
    self.assertTrue("hello" in model.target_subject_keyphrases)
    self.assertTrue("world" in model.target_subject_keyphrases)
    self.assertTrue("foo" in model.target_subject_keyphrases)
    self.assertTrue("bar" in model.target_subject_keyphrases)
    self.assertEqual(expected_list, model.target_subject_keyphrases)

  def test_add_raw_user_data_empty(self):
    '''
    Test when user input is all blank/empty
    :return:
    '''
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    model.add_raw_user_data(user_input)

    self.assertEqual([], model.target_sender_names)
    self.assertEqual(None, model.target_start_date)
    self.assertEqual(None, model.target_end_date)
    self.assertEqual([], model.target_subject_keyphrases)
    self.assertEqual([], model.target_sender_emails)

  def test_add_raw_user_data_single_name(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["names"] = "Swanson, Joe"

    model.add_raw_user_data(user_input)

    self.assertEqual(["swanson, joe"], model.target_sender_names)  # should be lower case here
    # everything else should be blank
    self.assertEqual(None, model.target_start_date)
    self.assertEqual(None, model.target_end_date)
    self.assertEqual([], model.target_subject_keyphrases)
    self.assertEqual([], model.target_sender_emails)

  def test_add_raw_user_data_multiple_names(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["names"] = "Swanson, Joe | Griffin, Peter | linkedIn"

    model.add_raw_user_data(user_input)
    self.assertEqual(["swanson, joe", "griffin, peter", "linkedin"], model.target_sender_names)

  def test_add_raw_user_data_single_email_address(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["email addresses"] = "Jane@Doe.Gov"
    model.add_raw_user_data(user_input)
    self.assertEqual(["jane@doe.gov"], model.target_sender_emails)
    self.assertEqual([], model.target_sender_names)
    self.assertEqual(None, model.target_start_date)
    self.assertEqual(None, model.target_end_date)
    self.assertEqual([], model.target_subject_keyphrases)

  def test_add_raw_user_data_multiple_email_address(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["email addresses"] = "Jane@Doe.Gov, Doctor@Who.com , cAts@cool.edu "
    model.add_raw_user_data(user_input)
    self.assertEqual(["jane@doe.gov", "doctor@who.com", "cats@cool.edu"], model.target_sender_emails)

  def test_add_raw_user_single_keyword(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["keywords"] = "hElLo"

    model.add_raw_user_data(user_input)
    self.assertEqual(["hello"], model.target_subject_keyphrases)
    self.assertEqual([], model.target_sender_names)
    self.assertEqual(None, model.target_start_date)
    self.assertEqual(None, model.target_end_date)
    self.assertEqual([], model.target_sender_emails)

  def test_add_raw_user_multiple_keywords(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    # TODO allow punctuation??? - Probably Not.. might have to apply when reading subjects though
    user_input["keywords"] = "hElLo, woRld , sushi,is,my, Fave"

    model.add_raw_user_data(user_input)
    self.assertEqual(["hello", "world", "sushi", "is", "my", "fave"], model.target_subject_keyphrases)

  def test_add_raw_user_start_date(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''
    user_input["start date"] = "03/23/1970"
    model.add_raw_user_data(user_input)
    expected_date = model.date_utility.convert_string_to_date("03/23/1970")

    self.assertEqual(expected_date, model.target_start_date)

  def test_add_raw_user_start_date_invalid_input(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    # missing both '/'
    user_input["start date"] = "03231970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # missing either '/'
    user_input["start date"] = "03/231970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # missing both '/'
    user_input["start date"] = "0323/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months o
    user_input["start date"] = "0/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months empty
    user_input["start date"] = "/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months negative
    user_input["start date"] = "-1/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day 0
    user_input["start date"] = "5/0/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day empty
    user_input["start date"] = "5//1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day beyond 31
    user_input["start date"] = "5/32/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year empty
    user_input["start date"] = "5/32/"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year less than 4 digits
    user_input["start date"] = "5/32/01"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year greater than 4 digits
    user_input["start date"] = "5/32/20001"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

  def test_add_raw_user_end_date_invalid_input(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    # missing both '/'
    user_input["end date"] = "03231970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # missing either '/'
    user_input["end date"] = "03/231970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # missing both '/'
    user_input["end date"] = "0323/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months o
    user_input["end date"] = "0/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months empty
    user_input["end date"] = "/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid months negative
    user_input["end date"] = "-1/23/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day 0
    user_input["end date"] = "5/0/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day empty
    user_input["end date"] = "5//1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid day beyond 31
    user_input["end date"] = "5/32/1970"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year empty
    user_input["end date"] = "5/32/"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year less than 4 digits
    user_input["end date"] = "5/32/01"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

    # invalid year greater than 4 digits
    user_input["end date"] = "5/32/20001"
    with self.assertRaises(DateConversionError):
      model.add_raw_user_data(user_input)

  # TODO make a check to see if end date earlier than start date

  def test_are_conditions_empty_no_conditions(self):
    model = self.model
    self.assertTrue(model.are_conditions_empty())

  def test_are_conditions_empty_all_conditions_met(self):
    model = self.model

    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    expected_values = ["Mr. Pants", "yomama@whatever.com", "word to your mama", "02/28/2010", "5/18/2011"]
    for i in range(len(expected_keys)):
      user_input[expected_keys[i]] = expected_values[i]
    model.add_raw_user_data(user_input)

    self.assertFalse(model.are_conditions_empty())

  def test_are_conditions_empty_single_conditions(self):
    print_conditions = False
    model = self.model

    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    expected_values = ["Mr. Pants", "yomama@whatever.com", "word to your mama", "02/28/2010", "5/18/2011"]
    counter = 0
    for i in range(len(expected_keys)):
      for j in range(len(expected_values)):
        if j == counter:
          user_input[expected_keys[j]] = expected_values[j]
        else:
          user_input[expected_keys[j]] = ''

      model.add_raw_user_data(user_input)
      self.assertFalse(model.are_conditions_empty())
      counter += 1
      if print_conditions is True:
        model.print_conditions()
      model.reset_deletion_conditions()

  # TODO Test combination of conditions for are conditions empty
  # maybe write a loop similar to before to get first 3 conditions in varying
  # configs
  # also need to do combo with dates

  def test_are_conditions_empty_combo(self):
    print_conditions = False
    model = self.model

    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    expected_values = ["Mr. Pants", "yomama@whatever.com", "word to your mama", "02/28/2010", "5/18/2011"]
    counter = 0
    for i in range(len(expected_keys)):
      for j in range(len(expected_values)):
        if j <= counter:
          user_input[expected_keys[j]] = expected_values[j]
        else:
          user_input[expected_keys[j]] = ''

      model.add_raw_user_data(user_input)
      self.assertFalse(model.are_conditions_empty())
      counter += 1
      if print_conditions is True:
        model.print_conditions()
      model.reset_deletion_conditions()

  def test_is_only_one_date_condition_filled(self):
    # only start date filled
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["start date"] = "10/10/2020"
    model.add_raw_user_data(user_input)

    self.assertTrue(model.is_only_one_date_condition_filled())

    # only end date filled
    model.reset_deletion_conditions()
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''
    user_input["end date"] = "10/11/2020"
    model.add_raw_user_data(user_input)
    self.assertTrue(model.is_only_one_date_condition_filled())

    # both dates are filled
    model.reset_deletion_conditions()
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''
    user_input["start date"] = "10/10/2020"
    user_input["end date"] = "10/11/2020"
    model.add_raw_user_data(user_input)
    self.assertFalse(model.is_only_one_date_condition_filled())

    # neither dates filled
    model.reset_deletion_conditions()
    self.assertFalse(model.is_only_one_date_condition_filled())

  def test_are_both_date_conditions_filled(self):
    # only start date filled
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    user_input["start date"] = "10/10/2020"
    model.add_raw_user_data(user_input)

    self.assertFalse(model.are_both_date_conditions_filled())

    # only end date filled
    model.reset_deletion_conditions()
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''
    user_input["end date"] = "10/11/2020"
    model.add_raw_user_data(user_input)
    self.assertFalse(model.are_both_date_conditions_filled())

    # both dates are filled
    model.reset_deletion_conditions()
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''
    user_input["start date"] = "10/10/2020"
    user_input["end date"] = "10/11/2020"
    model.add_raw_user_data(user_input)
    self.assertTrue(model.are_both_date_conditions_filled())

    # neither dates filled
    model.reset_deletion_conditions()
    self.assertFalse(model.are_both_date_conditions_filled())


  def test_setup_condition_check(self):
    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    model.add_raw_user_data(user_input)
    model.setup_condition_checks()

    #empty condition check, no func added
    self.assertEqual([], model.or_conditions_to_check)

    #only a name added
    model.reset_deletion_conditions()
    user_input["names"] = "Jotaro Kujo"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertEqual([model.check_email_name], model.or_conditions_to_check)

    #only a sender email added
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = "joseph@joestar.com"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertEqual([model.check_email_address], model.or_conditions_to_check)

    # only a sender keyword added
    model.reset_deletion_conditions()
    user_input["email addresses"] = ""
    user_input["keywords"] = "it was me Dio"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertEqual([model.check_subject], model.or_conditions_to_check)

    # name + email combo
    model.reset_deletion_conditions()
    user_input["keywords"] = ""
    user_input["names"] = "Jotaro Kujo"
    user_input["email addresses"] = "joseph@joestar.com"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertTrue(model.check_email_name in model.or_conditions_to_check)
    self.assertTrue(model.check_email_address in model.or_conditions_to_check)
    self.assertFalse(model.check_subject in model.or_conditions_to_check)

    #name + keyword combo
    model.reset_deletion_conditions()
    user_input["names"] = "Jotaro Kujo"
    user_input["email addresses"] = ''
    user_input["keywords"] = "it was me Dio"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertTrue(model.check_email_name in model.or_conditions_to_check)
    self.assertTrue(model.check_subject in model.or_conditions_to_check)
    self.assertFalse(model.check_email_address in model.or_conditions_to_check)

    #email address + keyword combo
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = "joseph@joestar.com"
    user_input["keywords"] = "it was me Dio"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertTrue(model.check_email_address in model.or_conditions_to_check)
    self.assertTrue(model.check_subject in model.or_conditions_to_check)
    self.assertFalse(model.check_email_name in model.or_conditions_to_check)

    # name + address + keyword
    model.reset_deletion_conditions()
    user_input["names"] = "Jotaro Kujo"
    user_input["email addresses"] = "joseph@joestar.com"
    user_input["keywords"] = "it was me Dio"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    self.assertTrue(model.check_email_address in model.or_conditions_to_check)
    self.assertTrue(model.check_subject in model.or_conditions_to_check)
    self.assertTrue(model.check_email_name in model.or_conditions_to_check)

  def test_run_condition_check(self):
    item = email_item_test_class()
    item.set_string_attributes(name="Giovanna, Giorno")
    item.set_date()

    model = self.model
    user_input = {}
    expected_keys = ["names", "email addresses", "keywords", "start date", "end date"]
    for each_key in expected_keys:
      user_input[each_key] = ''

    #name match
    user_input["names"] = "Giovanna, Giorno"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)

    self.assertTrue(is_match)

    #name mismatch
    model.reset_deletion_conditions()
    user_input["names"] = "Giorno"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertFalse(is_match)

    #address, even lower case is ok!
    item.clear_all_attributes()
    item.set_string_attributes(address="dio@bizarre.net")
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = "Dio@bizarre.net"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    #keyword
    item.clear_all_attributes()
    item.set_string_attributes(subject="It was I Dio!")
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = ""
    user_input["keywords"] = "was"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    #keyword mismatch
    item.clear_all_attributes()
    item.set_string_attributes(subject="It was I Dio!")
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = ""
    user_input["keywords"] = "Nope it"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertFalse(is_match)

    #only name matches, should be true
    item.clear_all_attributes()
    user_input["names"] = "Giovanna, Giorno"
    user_input["email addresses"] = "Dio@bizarre.net"
    user_input["keywords"] = "was"

    item.set_string_attributes(name="Giovanna, Giorno", address="star@platinum.edu", subject="what a pain")
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    #only address matches, should be true
    item.clear_all_attributes()
    user_input["names"] = "Giovanna, Giorno"
    user_input["email addresses"] = "Dio@bizarre.net"
    user_input["keywords"] = "was"

    item.set_string_attributes(name="Jake from StateFarm", address="Dio@bizarre.net", subject="what a pain")
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    # only keyword matches, should be true
    item.clear_all_attributes()
    user_input["names"] = "Giovanna, Giorno"
    user_input["email addresses"] = "Dio@bizarre.net"
    user_input["keywords"] = "was"

    item.set_string_attributes(name="Jake from StateFarm", address="star@platinum.edu", subject="he was a vampire")
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    #No string attribute matches, should be false
    item.clear_all_attributes()
    user_input["names"] = "Giovanna, Giorno"
    user_input["email addresses"] = "Dio@bizarre.net"
    user_input["keywords"] = "was"

    item.set_string_attributes(name="Jake from StateFarm", address="star@platinum.edu", subject="what a pain")
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertFalse(is_match)

    #check date match only
    item.clear_all_attributes()
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = ""
    user_input["keywords"] = ""
    item.set_date(year=2022, month=2,day=22)
    user_input["start date"] = "2/21/2022"
    user_input["end date"] = "2/22/2022"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    # check date does not match
    item.clear_all_attributes()
    model.reset_deletion_conditions()
    user_input["names"] = ""
    user_input["email addresses"] = ""
    user_input["keywords"] = ""
    item.set_date(year=2022, month=3, day=22)
    user_input["start date"] = "2/21/2022"
    user_input["end date"] = "2/22/2022"
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertFalse(is_match)

    #check date and name match
    item.clear_all_attributes()
    item.set_string_attributes(name="Giovanna, Giorno")
    user_input["names"] = "Giovanna, Giorno"
    item.set_date(year=2022, month=2, day=22)
    user_input["start date"] = "2/21/2022"
    user_input["end date"] = "2/22/2022"
    model.reset_deletion_conditions()
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertTrue(is_match)

    #check if name matches but date does not, should be false
    item.clear_all_attributes()
    item.set_string_attributes(name="Giovanna, Giorno")
    user_input["names"] = "Giovanna, Giorno"
    item.set_date(year=2022, month=3, day=22)
    user_input["start date"] = "2/21/2022"
    user_input["end date"] = "2/22/2022"
    model.reset_deletion_conditions()
    model.add_raw_user_data(user_input)
    model.setup_condition_checks()
    is_match = model.run_condition_check(item)
    self.assertFalse(is_match)














def main():
  unittest.main(verbosity=3)


if __name__ == '__main__':
  main()
