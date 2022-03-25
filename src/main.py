from guizero import App, Text, PushButton, Box, Window, TextBox, ButtonGroup, Slider
from random import choice
from user import User
from advertOptions import advertOptions
import csv

THEMEBACKGROUND = "#ffffff"
THEMETEXT = "#000000"
listOfAllText = []
listOfAllBg = []
currentUser = 0

class TextTheme(Text) :
  """Guizero text that automatically appends itself to the list of text objects upon instantiation"""
  def __init__(self, master, text = "", size=13, color=THEMETEXT, bg=None, font=None, grid=None, align=None, visible=True, enabled=None, width=None, height=None):
    listOfAllText.append(self)
    super().__init__(master, text, size, color, bg, font, grid, align, visible, enabled, width, height)
    self.text_color = THEMETEXT

class ButtonTheme(PushButton) :
  """Guizero PushButton that automatically appends itself to the list of text objects"""
  def __init__(self, master, command=None, args=None, text="Button", image=None, pady=10, padx=10, grid=None, align=None, icon=None, visible=True, enabled=None, width=None, height=None) :
    listOfAllText.append(self)
    listOfAllBg.append(self)
    super().__init__(master, command, args, text, image, pady, padx, grid, align, icon, visible, enabled, width, height)
    self.text_color = THEMETEXT
    self.bg = THEMEBACKGROUND
    self.text_size = 13;

app = App(title = "Wordle Rip Off", layout = "grid", width = 400, height = 540, bg = THEMEBACKGROUND)
listOfAllBg.append(app)
row = 0
word = ""
end = False

# create list of words
with open("data/fiveLetterWords.txt", "r") as file:
  options = file.readlines()
  for line in options :
    newLine = [x for x in line if x.isalpha()]
    options[options.index(line)] = ''.join(newLine)
solution = choice(options)

def changeTheme() :
  """update theme of all elements"""
  for i in listOfAllText :
    i.text_color = THEMETEXT

  for j in listOfAllBg :
    j.bg = THEMEBACKGROUND

def exitGame() :
  """Close down game after checking with user that that is what they want to do"""
  if app.yesno("Quit?", "Are you sure you want to quit?") :
    app.destroy()
    
def howToPlay() :
  """Provide the user with instructions on how to play"""
  app.info("How to Play", "Guess the Wordle Rip Off in SIX tries. Each guess must be a 5 letter word.\nAfter each guess, the tile colours will change. Green means the letter is correct, and in the right spot. Yellow means the letter is right, but not in the right spot. Dark grey means the letter is wrong.\nClick anywhere and start typing to play.")

def checkWord() :
  """Check if the user word is in the list of 5 letter words, and also check if it is right"""
  global end
  colours = [0 for x in range(5)]
  if solution == word :
    # Win
    colours = ["green" for x in range(5)]
    end = True
    updateColour(colours)
    return 1
  
  for i in range(len(word)) :
    if word[i] == solution[i] :
      colours[i] = "green"
    elif word[i] in solution :
      colours[i] = "yellow"
    else :
      colours[i] = "grey"

  updateColour(colours)
  return 0

def updateText(eventData) :
  """Change text to show letters user is typing in."""
  global word, row, listOfButtons, end
  # if the game is over, don't do anything
  if end :
    return
  
  # Backspace
  if eventData.key == '\b' :
    word = word[:-1]
  elif eventData.key == '\r' :
    
    if len(word) == 5 :
      # is word valid?
      if word not in options :
        return
    
      isRight = checkWord()
      if isRight :
        app.info("Win!", f"You guessed the correct word in {row+1} tries!")
        end = True
      elif row == 5 and not isRight:
        app.info("Fail!", f"You failed at guessing the answer {solution.upper()}. :(")
        end = True
      if row == 5 or isRight == 1 :
        advert = advertOptions[currentUser.favouriteGame]
        app.info(advert[0], advert[1])
        if app.yesno("Play again?", "Would you like to play again?") :
          restart(False)
      else :
        row += 1
        word = ''
      return
  elif len(word) == 5 :
    return
  else :
    if eventData.key.isalpha() : 
      word += eventData.key

  # fill word with whitespace
  while len(word) < 5 :
    word += ' '

  # update text
  for i in range(5) :
    listOfButtons[i][row].text = word[i].upper()

  word = word.strip()

def addWord() :
  newWord = app.question("New Word", "Type new word: ")
  with open("data/fiveLetterWords.txt", "a") as file :
    if (len(newWord) == 5 and newWord.isalpha()) and (newWord not in options):
      file.write(newWord + '\n')
      app.info("Word Added", f"Your word {newWord} has been successfully added.")
    else :
      app.warn("Invalid Word", "Word is not alpha, 5 lettered, or is already in the text file.")

def updateColour(colour) :
  """Change button background to show users progress in getting the word."""
  global listOfButtons, row
  for i in range(5) :
    listOfButtons[i][row].bg = colour[i]
    alphabetText[alphabet.index(word[i].upper())].bg = colour[i]
    if colour[i] == "green" or colour[i] == "grey" :
      listOfButtons[i][row].text_color = "white"
      alphabetText[alphabet.index(word[i].upper())].text_color = "white"
    else :
      listOfButtons[i][row].text_color = "black"
      alphabetText[alphabet.index(word[i].upper())].text_color = "black"

def restart(logout = True) :
  """Restart game and/or log out user"""
  global THEMEBACKGROUND, THEMETEXT, end, solution, row, word
  end = False
  for i in range(5) :
    for j in range(6) :
      listOfButtons[i][j].bg = THEMEBACKGROUND
      listOfButtons[i][j].text_color = THEMETEXT
      listOfButtons[i][j].text = ""
      
  for i in alphabetText :
    i.bg = THEMEBACKGROUND
    i.text_color = THEMETEXT

  row = 0
  word = ""
  solution = choice(options)
  if logout :
    app.hide()
    THEMEBACKGROUND = "#ffffff"
    THEMETEXT = "#000000"
    changeTheme()
    loginWindow.show()

def login() :
  """Check if the user has valid login"""
  global THEMEBACKGROUND, THEMETEXT, currentUser
  with open("data/userCred.csv", "r") as file :
    userInfo = csv.reader(file)
    possibleCred = {row[0] : [row[1], row[2], row[3], row[4]] for row in userInfo}
  if (usernameInput.value in possibleCred) and (possibleCred[usernameInput.value][0] == passwordInput.value) :
    currentUser = User(usernameInput.value, possibleCred[usernameInput.value][0], possibleCred[usernameInput.value][1], possibleCred[usernameInput.value][2], possibleCred[usernameInput.value][3])
    THEMEBACKGROUND = currentUser.mainTheme
    THEMETEXT = currentUser.textTheme
    changeTheme()
    usernameInput.value = ""
    passwordInput.value = ""
    loginWindow.hide()
    app.show()
  else :
    app.warn("Incorrect Username or Password", "Your username or password was incorrect.")

def initSingupWindow() :
  """Open signup window"""
  loginWindow.hide()
  signupWindow.show()

def signup() :
  """Sign the user up"""
  with open("data/userCred.csv", "r") as file :
    userInfo = csv.reader(file)
    possibleCred = {row[0] : row[1] for row in userInfo}
  if (newUsernameInput.value in possibleCred) :
    app.warn("Username already used", "This username is taken")
  elif (newPasswordInput.value != confirmPasswordInput.value) :
    app.warn("Passwords don't match", "Your passwords did not match")
    newPasswordInput.value = ""
    confirmPasswordInput.value = ""
  elif (len(newPasswordInput.value) < 4) :
    app.warn("Password too Short", "Password must be longer than 3 characters")
    newPasswordInput.value = ""
    confirmPasswordInput.value = ""
  else :
    updateBackground(True, True)
    updateBackground(False, True)
    newUser = User(newUsernameInput.value, newPasswordInput.value, favouriteGameChoice.value, THEMEBACKGROUND, THEMETEXT)
    with open("data/userCred.csv", "a") as file :
      csvFile = csv.writer(file)
      csvFile.writerow(newUser.fileString())
    newUsernameInput.value = ""
    newPasswordInput.value = ""
    confirmPasswordInput.value = ""
    loginWindow.show()
    signupWindow.hide()

def updateBackground(isBg = True, isPermenant = False) :
  """Update background of body widget."""
  global THEMEBACKGROUND, THEMETEXT

  if isBg :
    r = hex(mainRed.value).strip("0x")
    g = hex(mainGreen.value).strip("0x")
    b = hex(mainBlue.value).strip("0x")
  else :
    r = hex(textRed.value).strip("0x")
    g = hex(textGreen.value).strip("0x")
    b = hex(textBlue.value).strip("0x")

  # format hex values
  if len(r) == 1 :
    r += str(r[0])
    r = r.replace(r[0], '0')
  if len(g) == 1 :
    g += str(g[0])
    g = g.replace(g[0], '0')
  if len(b) == 1 :
    b += str(b[0])
    b = b.replace(b[0], '0')
  if len(r) == 0 :
    r = "00"
  if len(g) == 0 :
    g = "00"
  if len(b) == 0 :
    b = "00"

  # create hex code with the rgb values
  finalColour = f"#{r}{g}{b}"
  if isPermenant : 
    if isBg :
      THEMEBACKGROUND = finalColour
    else :
      THEMETEXT = finalColour
  else :
    if isBg :
      mainExperimentBox.bg = finalColour
    else :
      textExperimentBox.bg = finalColour

def textTempUpdate() :
  """Call updateBackground properly eventhough sliders can't pass arguments"""
  updateBackground(False)

def mainTempUpdate() :
  """Call updateBackground as the temporary background colour"""
  updateBackground()

def loginEnter(eventData) :
  """Call the function the submit button does"""
  if eventData.key == "\r" :
    login()

def signupEnter(eventData) :
  """Call the function the submit button does"""
  if eventData.key == "\r" :
    signup()
  
# Login Window
loginWindow = Window(app, title = "Log In", width = 400, height = 440, bg = THEMEBACKGROUND)
listOfAllBg.append(loginWindow)

# Title and quit box
logTitleBox = Box(loginWindow, width = 400, height = 40, border = True)
logExitButton = ButtonTheme(logTitleBox, align = "left", command = exitGame, text = "Quit")
logSignupButton = ButtonTheme(logTitleBox, align = "left", command = initSingupWindow, text = "Signup")
logTitle = TextTheme(logTitleBox, align = "right", width = "fill", text = "Log In")

# Log in form
logFormBox = Box(loginWindow, width = 400, height = 300, layout = "grid")
usernamePrompt = TextTheme(logFormBox, text = "Username:", grid = [0,0])
usernameInput = TextBox(logFormBox, grid = [1,0])
usernameInput.text_size = 13;
passwordPrompt = TextTheme(logFormBox, text = "Password:", grid = [0,1])
passwordInput = TextBox(logFormBox, grid = [1,1], hide_text = True)
passwordInput.text_size = 13;
submitLog = ButtonTheme(logFormBox, grid = [0,2], command = login, text = "Submit")

# // Signup Window \\
signupWindow = Window(app, title = "Sign Up", height = 540, width = 400, bg = THEMEBACKGROUND)
listOfAllBg.append(signupWindow)

# Title and quit
signTitleBox = Box(signupWindow, width = 400, height = 40, border = True)
signExitButton = ButtonTheme(signTitleBox, align = "left", command = exitGame, text = "Quit")
signTitle = TextTheme(signTitleBox, align = "right", width = "fill", text = "Signup")

# Sign up form
signFormBox = Box(signupWindow, width = 400, height = 500, layout = "grid")

newUsernamePrompt = TextTheme(signFormBox, text = "Username:", grid = [0,0])
newUsernameInput = TextBox(signFormBox, grid = [1,0])
newUsernameInput.text_size = 13;
newPasswordPrompt = TextTheme(signFormBox, text = "Password:", grid = [0,1])
newPasswordInput = TextBox(signFormBox, grid = [1,1], hide_text = True)
newPasswordInput.text_size = 13;
confirmPasswordPrompt = TextTheme(signFormBox, text = "Confirm Password:", grid = [0,2])
confirmPasswordInput = TextBox(signFormBox, grid = [1,2], hide_text = True)
confirmPasswordInput.text_size = 13;

# favourite game
favouriteGamePrompt = TextTheme(signFormBox, grid = [0,3], text = "Select favourite video game:")
favouriteGameChoice = ButtonGroup(signFormBox, grid = [0,4], options = [["Minecraft", "min"], ["Halo", "hal"], ["Sea of Thieves", "sot"], ["Apex Legends", "apx"]])

# main theme
themePrompt = TextTheme(signFormBox, grid = [0,5], text = "Theme colours:")
redPrompt = TextTheme(signFormBox, grid = [0,6], text = "Red:")
mainRed = Slider(signFormBox, grid = [1,6], end = 255, command = mainTempUpdate)
mainExperimentBox = Box(signFormBox, grid = [2,6,1,3], border = True, width = 50, height = 120)
mainExperimentBox.bg = "black"
greenPrompt = TextTheme(signFormBox, grid = [0,7], text = "Green:")
mainGreen = Slider(signFormBox, grid = [1,7], end = 255, command = mainTempUpdate)
bluePrompt = TextTheme(signFormBox, grid = [0,8], text = "Blue:")
mainBlue = Slider(signFormBox, grid = [1,8], end = 255, command = mainTempUpdate)

# text theme
textPrompt = TextTheme(signFormBox, grid = [0,9], text = "Text colours:")
textRedPrompt = TextTheme(signFormBox, grid = [0,10], text = "Red:")
textRed = Slider(signFormBox, grid = [1,10], end = 255, command = textTempUpdate)
textExperimentBox = Box(signFormBox, grid = [2,10,1,3], border = True, width = 50, height = 120)
textExperimentBox.bg = "black"
textGreenPrompt = TextTheme(signFormBox, grid = [0,11], text = "Green:")
textGreen = Slider(signFormBox, grid = [1,11], end = 255, command = textTempUpdate)
textBluePrompt = TextTheme(signFormBox, grid = [0,12], text = "Blue:")
textBlue = Slider(signFormBox, grid = [1,12], end = 255, command = textTempUpdate)

submitSign = ButtonTheme(signFormBox, grid = [0,13], command = signup, text = "Submit")

#// Game Window \\
  
# Title and help button box
titleBox = Box(app, grid = [0,0], width = 400, height = 40, border = True)
exitButton = ButtonTheme(titleBox, align = "left", command = exitGame, text = "Quit")
logButton = ButtonTheme(titleBox, align = "left", command = restart, text = "Log Out")
helpButton = ButtonTheme(titleBox, align = "right", command = howToPlay, text = "How to Play")
addWordButton = ButtonTheme(titleBox, align = "right", command = addWord, text = "Add Word")

# Buttons that display letters
mainBox = Box(app, grid = [0,1], width = 300, height = 310, layout = "grid")
blankSpace = TextTheme(mainBox, grid = [0,0], height = 1)

# store buttons in list
listOfButtons = [[],[],[],[],[],[]]
for i in range(5) :
  for j in range(6) :
    newButton = ButtonTheme(mainBox, grid = [i+1,j+1], height = 2, width = 2, text = "")
    listOfButtons[i].append(newButton)

# Detect user typing
app.when_key_pressed = updateText

# When user presses enter, it causes the same effect as pressing the submit button
loginWindow.when_key_pressed = loginEnter
signupWindow.when_key_pressed = signupEnter

# Letter Status - alphabet at the bottom
usedLetter = Box(app, grid = [0,2], width = 400, height = 50)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabetText = []
for i in range(26) :
  newText = TextTheme(usedLetter, align = "left", text = alphabet[i], size = 12)
  alphabetText.append(newText)

signupWindow.hide()
app.hide()

app.display()