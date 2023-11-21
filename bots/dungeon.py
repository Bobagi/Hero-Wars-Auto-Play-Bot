from imageFind import *
from general import *

max_attempts = 3
images = {}

def enterDungeon():
  global max_attempts, images
  if find_image(max_attempts, images['guild']):
    print("Entering the Guild isle...")

    if find_image_noClick(max_attempts, images['city']) and find_image(max_attempts, images['dungeonEntry1']):
      print("Entering the Titan's hall...")
      if find_image(max_attempts, images['dungeonEntry2']):
        print("Entering the Dungeon...")
      else:
        closeApp("Failed to enter the Dungeon")
    else:
      closeApp("Failed to enter the Titan's hall")
  elif find_image_noClick(max_attempts, images['city']):
    if find_image(max_attempts, images['dungeonEntry1']): 
      print("Entering the Titan's hall...")
      if find_image(max_attempts, images['dungeonEntry2']):
          print("Entering the Dungeon...")
      else:
          closeApp("Failed to enter the Dungeon")
    else:
      closeApp("Failed to enter the Titan's hall")
  elif find_image(max_attempts, images['dungeonEntry2']):
    print("Entering the Dungeon...")
  elif find_image_noClick(max_attempts, images['menuButtons']):
    print("Already in Dungeon...")
  else:
    return False
      
  return True

def main():
    drawHeader()
    print("\n\nHeroWars bot - Dungeon")
    print("Starting in 2 seconds...")
    time.sleep(2)
    print("HeroWars bot - Dungeon -> bot ready!")

    global images
    images = find_image_paths('Dungeon')

    resWidth, resHeigth = get_monitor_resolution(max_attempts, images['headerIcon'])
    if not (resWidth and resHeigth):
        closeApp("Can't find a web browser with the Hero Wars Domination Era logo at the header")
    else:
        if resWidth == 1920 and resHeigth == 1080:
            print("Using original resolution, threshold set to 80%")
            setThreshold(0.8)
        else:
            print("Not using 1920x1080 resolution, threshold set to 55%")
            setThreshold(0.55)
    
    if not enterDungeon():
        closeApp('Cannot enter the Dungeon!')

if __name__ == "__main__":
    main()