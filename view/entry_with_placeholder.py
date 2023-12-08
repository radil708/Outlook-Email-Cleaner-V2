from tkinter import Entry, END
#TODO SUPER USEFUL ADD TO REPO ON ITS OWN

class entry_with_placeholder(Entry):

  def __init__(self,text_hint: str = "Entry Hint", hint_color: str = "grey", user_input_color: str = "black", *args,**kwargs):
    Entry.__init__(self,*args,**kwargs)
    self.text_hint = text_hint
    self.hint_color = hint_color
    self.user_input_color = user_input_color

    self.bind("<FocusIn>", self.foc_in)
    self.bind("<FocusOut>", self.foc_out)

    self.place_hint()


  def place_hint(self):
    self.insert(0, self.text_hint)
    self['fg'] = self.hint_color

  def foc_in(self, *args): #*args needed to be able to set as a button command
    if self['fg'] == self.hint_color:
      self.delete('0', 'end')
      self['fg'] = self.user_input_color

  def foc_out(self, *args):
    if not self.get():
      self.place_hint()

  def clear_entry(self, *args):#*args needed to be able to set as a button command
    if self['fg'] == self.user_input_color:
      self.delete('0', 'end')
      self.place_hint()
      self.master.focus_set() #remove cursor from entry widget



