import sys

def drawHeader():
  # ANSI escape code for yellow text color
  yellow_color = "\033[93m"

  print(yellow_color)
  print(" ___       _              _ ")
  print("| . > ___ | |_  ___  ___ <_>")
  print("| . \/ . \| . \<_> |/ . || |")
  print("|___/\___/|___/<___|\_. ||_|")
  print("                    <___'   ")
  print("                    Presents")
  print("\nHeroWars Time Saver")

   # ANSI escape code for resetting text color
  reset_color = "\033[0m"
  print(reset_color)  # Resetting color to default

def closeApp(msg, color = 0):
    green_color = "\033[92m"
    red_color = "\033[91m"
    reset_color = "\033[0m"

    if color == 1:
      print(green_color)
    elif color == 2:
      print(reset_color)
    else:
      print(red_color)
    
    print(msg, "... ending application")
    print(reset_color)
    
    if getattr(sys, 'frozen', False):
        input()
    
    sys.exit()