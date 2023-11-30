import win32com.client as client

com_obj = client.Dispatch("Outlook.Application")


outlook_connection = com_obj.GetNameSpace('MAPI')

# for mailbox in outlook_connection.Folders:
#     print(mailbox)

target_mailbox = 'adil.r@northeastern.edu'

selected_directory = outlook_connection.Folders(target_mailbox).Folders('Inbox')

all_emails = selected_directory.Items



counter = 0

for email in all_emails:
    counter += 1
    #TO get name from email below
    print(type(email))
    exit(0)
    print((email.SenderName).replace(" ", "_"))
    #email_class = <class 'win32com.client.CDispatch'>

    #name problem is that some names have commas in them
    #check if name alread in email list so probably check email first
    #lstrip and rstrip any spaces in names

    #email address
    #print(email.SenderEmailAddress)

    if counter == 100:
        break


exit(0)



a = [1,2,3,4]
b = [2,7]
x = any(x in a for x in b)
print(x)