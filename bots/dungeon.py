from imageFind import *
from general import *

max_attempts: int = 3
images = {}
oracleCards: int = 0

def enterDungeon():
    global max_attempts, images
    if find_image(max_attempts, images['guild']):
        print("Entering the Guild isle...")
        time.sleep(1)

        while True:
            if find_image_noClick(max_attempts, images['city']):
                break
        
        if find_image_noClick(max_attempts, images['city']) and find_image(max_attempts, images['dungeonEntry1']):
            print("Entering the Titan's hall...")
            if find_image(max_attempts, images['dungeonEntry2']):
                print("Entering the Dungeon...")
                time.sleep(2)
            else:
                closeApp("Failed to enter the Dungeon")
        else:
            closeApp("Failed to enter the Titan's hall")
    elif find_image_noClick(max_attempts, images['city']):
        if find_image(max_attempts, images['dungeonEntry1']): 
            print("Entering the Titan's hall...")
            if find_image(max_attempts, images['dungeonEntry2']):
                print("Entering the Dungeon...")
                time.sleep(2)
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

    alreadyGotTheOracle: bool = False

    global images
    images = find_image_paths('Dungeon')
    setResolutionScreenshots(1920, 1080)

    resWidth, resHeigth = get_monitor_resolution(max_attempts, images['headerIcon'])
    if not (resWidth and resHeigth):
        closeApp("Can't find a web browser with the Hero Wars Domination Era logo at the header")
    else:
        if resWidth == 1920 and resHeigth == 1080:
            print("Using original resolution, threshold set to 80%")
            setThreshold(0.8)
        else:
            print("Not using 1920x1080 resolution, threshold set to 50%")
            setThreshold(0.55)

    if not enterDungeon():
        closeApp('Cannot enter the Dungeon!')

    while True:
        print(f"Awaiting {1} seconds for next command...")
        time.sleep(1)

        setShowImgs(False)
        if not alreadyGotTheOracle and find_image(max_attempts, images['oracle']):
            while True:
                if not find_image(max_attempts, images['oracleButton']):
                    if not find_image(max_attempts, images['exitButton']) and not find_image(max_attempts, images['exitButton2']):
                        closeApp("Failed close Oracle window")
                    break

            if find_image(max_attempts, images['battleDoor']):
                if find_image_noClick(max_attempts, images['oracleCardIcon']):
                    location = get_image_location_on_screen(images['oracleCardIcon'])
                    if location:
                        # (x, y, template_width, template_height)
                        newXpos = location[0] + location[2] # Repositioning the pivot below the founded image
                        newWidth = 3 * location[2]
                        description = read_text_from_region(newXpos, location[1] + (location[3] // 4), newWidth, location[3] // 2, True)
                        if description:
                            print(f"You have {description} Oracle Cards!")
                            global oracleCards
                            oracleCards = int(description)
                            alreadyGotTheOracle = True

                            if not find_image(max_attempts, images['exitButton']) and not find_image(max_attempts, images['exitButton2']):
                                closeApp("Failed returning to Dungeon")
                        else:
                            closeApp("Failed reading Oracle Cards")
                    else:
                        closeApp("Error getting location of amount of Oracle cards")
                else:
                    closeApp("Failed to detect the Oracle card icon")
            else:
                closeApp("Failed to read amount of Oracle cards")

        if not alreadyGotTheOracle:
            continue

        kindOfDoorFound = 0
        if find_image(max_attempts, images['titanBattleDoor']):
            kindOfDoorFound = 1
        elif find_image(max_attempts, images['heroBattleDoor']):
            kindOfDoorFound = 2
        elif find_image(max_attempts, images['battleDoor']):
            kindOfDoorFound = 3

        if kindOfDoorFound > 0:
            if kindOfDoorFound == 1:
                attempts = 0
                locations = {}
                i = 0
                while attempts < max_attempts:
                    locatedImages = find_all_images_on_screen(images['swords'])
                    if len(locatedImages) > 0:
                        print("locatedImages: ", locatedImages)
                        for location in locatedImages:
                            # (x, y, template_width, template_height)
                            newXpos = location[0] + location[2] # Repositioning the pivot below the founded image
                            newWidth = 3 * location[2]
                            powerValue = read_text_from_region(newXpos, location[1] + (location[3] // 4), newWidth, location[3] // 2, True)
                            if powerValue:
                                print(f"The team have {powerValue} of power level!")
                                locations[i] = [int(powerValue), location]
                                i+=1
                            else:
                                closeApp("Failed reading titan's power level")
                        break
                    else:
                        attempts += 1
                        print(f"No relevant image found for titan's power level. Retrying...")
                
                min_entry = min(locations.items(), key=lambda x: x[1][0])
                key_with_lowest_power = min_entry[0]
                value_with_lowest_power = min_entry[1]

                attempts = 0
                i = 0
                while attempts < max_attempts:
                    locatedImages = find_all_images_on_screen(images['attack'])
                    if len(locatedImages) > 0:
                        print("locatedImages: ", locatedImages)
                        for location in locatedImages:
                            if i == key_with_lowest_power:
                                click_location(location[0],location[1],location[2],location[3])
                            else:
                                i+=1
                                continue
                        break
                    else:
                        attempts += 1
                        print(f"No relevant image found for titan's power level. Retrying...")

            if find_image(max_attempts, images['fightForYourOwn']):
                time.sleep(2)
                if find_image(max_attempts, images['toTheBattle']):
                    while True:
                        if find_image(max_attempts, images['auto']):
                            break
                    
                    while True:
                        if find_image(max_attempts, images['ok']):
                            break          
                else:
                    closeApp("Can't go to battle")
            else:
                closeApp("Can't fight for your own ;-;")
        else:
            closeApp("Can't find a battle door")
        
if __name__ == "__main__":
    main()