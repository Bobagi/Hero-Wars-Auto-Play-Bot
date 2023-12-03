import sys

def drawHeader():
  setPrintColor(4)

  print(" ___       _              _ ")
  print("| . > ___ | |_  ___  ___ <_>")
  print("| . \/ . \| . \<_> |/ . || |")
  print("|___/\___/|___/<___|\_. ||_|")
  print("                    <___'   ")
  print("                    Presents")
  print("\nHeroWars Time Saver")

  resetPrintColor()

def closeApp(msg, color = 0):
    if color == 1:
      setPrintColor(1)
    elif color == 2:
      resetPrintColor()
    else:
      setPrintColor(2)
    
    print(msg, "... ending application")
    resetPrintColor()
    
    if getattr(sys, 'frozen', False):
      input()
    
    sys.exit()

def setPrintColor(value):
  color = ""
  if value == 1:
    color = "\033[92m" #green
  elif value == 2:
    color = "\033[91m" #red
  elif value == 3:
    color = "\033[96m" #cyan
  elif value == 4:
    color = "\033[93m" #yellow
  else:
    color = "\033[0m" #white

  print(color)
   
def resetPrintColor():
  reset_color = "\033[0m"
  print(reset_color)