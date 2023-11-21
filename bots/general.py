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

def closeApp(msg):
    print(msg, "... ending application")
    
    if getattr(sys, 'frozen', False):
        input()
    
    sys.exit()