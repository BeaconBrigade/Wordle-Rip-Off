from guizero import App, Text, PushButton, Box, Window, TextBox
from random import choice
import csv

app = App(title = "Wordle Rip Off", layout = "grid", width = 400, height = 440, bg = "white")
count = 0
row = 0
word = ""
end = False

# create list of words
with open("fiveLetterWords.txt", "r") as file:
  options = file.readlines()
  for line in options :
    newLine = [x for x in line if x.isalpha()]
    options[options.index(line)] = ''.join(newLine)
solution = choice(options)

def exitGame() :
  """Close down game after checking with user that that is what they want to do"""
  isQuit = app.yesno("Quit?", "Are you sure you want to quit?")
  if isQuit :
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
  global count, word, row, listOfButtons, end
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
      if isRight == 1 :
        app.info("Win!", f"You guessed the correct word in {row+1} tries!")
      if row == 5 :
        if isRight == 0 :
          app.info("Fail!", f"You failed at guessing the answer {solution.upper()}. :(")
        end = True
      row += 1
      count = 0
      word = ''
      return
  elif len(word) == 5 :
    return
  else :
    if eventData.key.isalpha() : 
      word += eventData.key
      count += 1

  # fill word with whitespace
  while len(word) < 5 :
    word += ' '

  # update text
  for i in range(5) :
    listOfButtons[i][row].text = word[i].upper()

  word = word.strip()

def addWord() :
  newWord = app.question("New Word", "Type new word: ")
  with open("fiveLetterWords.txt", "a") as file :
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

def initLoginWindow() :
  """Open login window"""
  app.hide()
  loginWindow.show()

def login() :
  """Check if the user has valid login"""
  with open("userCred.csv", "r") as file :
    possibleCred = dict(filter(None, csv.reader(file)))
  if (usernameInput.value in possibleCred) and (possibleCred[usernameInput.value] == passwordInput.value) :
    usernameInput.value = ""
    passwordInput.value = ""
    loginWindow.hide()
    app.show()
  else :
    app.warn("Incorrect Username or Password", "Your username or password was incorrect.")

# Login Window
loginWindow = Window(app, title = "Log In", width = 400, height = 440, bg = "white")

# Title and quit box
logTitleBox = Box(loginWindow, width = 400, height = 40, border = True)
logExitButton = PushButton(logTitleBox, align = "left", command = exitGame, text = "Quit")
logTitle = Text(logTitleBox, align = "right", width = "fill", text = "Log In")

# Log in form
logFormBox = Box(loginWindow, width = 400, height = 300, layout = "grid")
usernamePrompt = Text(logFormBox, text = "Username:", grid = [0,0])
usernameInput = TextBox(logFormBox, grid = [1,0])
passwordPrompt = Text(logFormBox, text = "Password:", grid = [0,1])
passwordInput = TextBox(logFormBox, grid = [1,1], hide_text = True)
submitLog = PushButton(logFormBox, grid = [0,2], command = login, text = "Submit")

#// Game Window \\
  
# Title and help button box
titleBox = Box(app, grid = [0,0], width = 400, height = 40, border = True)
exitButton = PushButton(titleBox, align = "left", command = exitGame, text = "Quit")
logButton = PushButton(titleBox, align = "left", command = initLoginWindow, text = "Log In")
helpButton = PushButton(titleBox, align = "right", command = howToPlay, text = "How to Play")
addWordButton = PushButton(titleBox, align = "right", command = addWord, text = "Add Word")
title = Text(titleBox, align = "right", width = "fill", text = "Wordle")

# Buttons that display letters
mainBox = Box(app, grid = [0,1], width = 300, height = 310, layout = "grid")
blankSpace = Text(mainBox, grid = [0,0], height = 1)

# store buttons in list
listOfButtons = [[],[],[],[],[],[]]
for i in range(5) :
  for j in range(6) :
    newButton = PushButton(mainBox, grid = [i+1,j+1], height = 2, width = 2, text = "")
    listOfButtons[i].append(newButton)

# Detect user typing
app.when_key_pressed = updateText

# Letter Status - alphabet at the bottom
usedLetter = Box(app, grid = [0,2], width = 400, height = 50)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabetText = []
for i in range(26) :
  newText = Text(usedLetter, align = "left", text = alphabet[i], size = 10)
  alphabetText.append(newText)

app.hide()