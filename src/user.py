# User object

class User() :
  """This class stores all the data the user can have"""

  def __init__(self, username, password, favouriteGame, mainTheme, textTheme) :
    self.username = username
    self.password = password
    self.favouriteGame = favouriteGame
    self.mainTheme = mainTheme
    self.textTheme = textTheme

  def fileString(self) :
    """Returns the list to be stored in users.csv"""
    return [self.username, self.password, self.favouriteGame, self.mainTheme, self.textTheme]