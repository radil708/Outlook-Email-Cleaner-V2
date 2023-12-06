import tkinter as tk
from tkinter import ttk


class tkinter_view():

    def __init__(self):
        self.user_email_choice = None

    def set_user_email_choice(self, user_email_choice_in: str):
        self.user_email_choice = user_email_choice_in
        # TODO Delete
        print(self.user_email_choice)

    def build_welcome_window(self, user_email_choices: list):
        window = tk.Tk()
        window.title('Ramzi\'s Email Deleter Version 2')
        window.geometry('400x200')

        user_selection = tk.StringVar()

        input_frame = ttk.Frame(master=window)
        combo = ttk.Combobox(
            master=input_frame,
            state="readonly",
            values=user_email_choices,
            textvariable=user_selection
        )
        select_button = ttk.Button(master=input_frame,
                                   text="Select",
                                   command=lambda: self.set_user_email_choice(user_selection.get()))
        combo.pack(side="left", padx=5)
        select_button.pack(side="right")
        header_label = ttk.Label(master=window,
                                 text="Select the Email You Want To Cleanup",
                                 font="Bold")

        header_label.pack(pady=10)
        input_frame.pack(pady=15)
        window.mainloop()


def main():
    welcome = tkinter_view()
    welcome.build_welcome_window(["email_1", "email_2"])


if __name__ == "__main__":
    main()
