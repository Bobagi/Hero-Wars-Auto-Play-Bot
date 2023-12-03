from imageFind import *
from general import *
from collections import OrderedDict

images = {}

def choose_power_up(power_ups_types):
    global images
    max_attempts = 1
    desired_order = ['damage', 'armor', 'magicDefense']
    power_ups_types = OrderedDict((key, power_ups_types[key]) for key in desired_order)
    max_power_ups = 3
    bought = 0
    correctionWidth = 20

    for power_up in power_ups_types:
        print(f"Looking for {power_up} power up.")
        foundedImages = False
        attempts = 0
        while attempts < max_attempts and foundedImages == False:
            locatedImages = find_all_images_on_screen(power_ups_types[power_up])
            if len(locatedImages) > 0:
                print("locatedImages: ",locatedImages)
                foundedImages = True
                for location in locatedImages:
                    # newYpos = location[1] + location[3] # Repositioning the pivot below the founded image
                    # newWidth = location[2] + correctionWidth
                    # description = read_text_from_region(location[0] - (correctionWidth // 2), newYpos, newWidth, location[3])
                    # if "Comprou" in description:
                    #     print(f"Upgrade {power_up} already bought.")
                    #     continue

                    print(f"Upgrade {power_up} powerUp chosen.")
                    click_location(location[0], location[1], location[2], location[3])

                    # Check if the message of not enoght skulls appeared
                    if find_image(images['okButton']):
                        print("Not enought money!")
                        continue

                    bought += 1
                    if bought >= max_power_ups:
                        print("Max Power Ups bought!")
                        return True
            else:
                attempts += 1
                print(f"No relevant image found for {power_up}. Retrying...")
    
    return True

def enterTower():
    global images
    
    if find_image(images['tower']):
        print("Entering the tower...")
    else:
        if find_image_noClick(images['menuButtons']):
            print("Already in tower!")
        else:
            return False
            
    return True

def main():
    defaultWait = 2

    drawHeader()
    print("\n\nHeroWars bot - Tower")
    print(f"Starting in {defaultWait} seconds...")
    time.sleep(defaultWait)
    print("HeroWars bot - Tower -> bot ready!")
    
    takePowerUp = False
    attacking = False
    exitBattleAttempts = 0
    towerComplete = False

    global images
    images = find_image_paths('Tower')
    powerUpsImages = find_image_paths('Tower/powerUps')

    setThreshold(0.8)
    
    if not enterTower():
        closeApp('Cannot enter the tower!')
    
    while True:
        print(f"Awaiting {defaultWait} seconds for next command...")
        time.sleep(defaultWait)

        if towerComplete:
            if find_image(images['changeSkull']):
                if find_image(images['changeSkullIntoCoin']):
                    if find_image(images['towerPoints']):
                        if find_image(images['collectAll']):
                            if find_image(images['exitButton']):
                                find_image(images['exitButton'])
                                closeApp("Tower Completed!", 1)
                            else:
                                continue
                        else:
                            find_image(images['exitButton'])
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                if find_image(images['towerPoints']):
                    if find_image(images['collectAll']):
                        if find_image(images['exitButton']):
                            find_image(images['exitButton'])
                            closeApp("Tower Completed!", 1)
                        else:
                            continue
                    else:
                        find_image(images['exitButton'])
                        find_image(images['exitButton'])
                        closeApp("Tower Completed!", 1)
                else:
                    continue

        if attacking:
            while True:
                time.sleep(defaultWait)
                if find_image(images['okBattleButton']):
                    find_image(images['okBattleButton']) # Double Check
                    attacking = False
                    exitBattleAttempts = 0
                    break
                else:
                    exitBattleAttempts += 1
                    if exitBattleAttempts > max_attempts:
                        exitBattleAttempts = 0
                        find_image(images["exitEvent"])
                        if not find_image_noClick(images["camButton"]):
                            attacking = False
                            continue

        # PowerUps
        if takePowerUp:
            power_up_done = choose_power_up(powerUpsImages)

            if not power_up_done:
                print("Problem choosing a power up...")
                break
            else:
                takePowerUp = False
                if find_image(images['exitFinal']):
                    if find_image(images['arrowRight']):
                        print("Going to next floor...")
                        time.sleep(defaultWait)
                    else:
                        if find_image(images['arrowLeft']):
                            print("Going to next floor...")
                            time.sleep(defaultWait)
                        else:
                            print("Problem going to the next floor after power up... ending application")
                            sys.exit()
                else:
                    print("Problem closing power up window... ending application")
                    sys.exit()

        if find_image(images['battleDoor']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click battleDoor, but not works!")
            else:
                if find_image(images['skipButton']):
                    print("Skip battle")
                    continue
                else:
                    if find_image(images['attackButton']): 
                        print("Fight battle")                       
                        if find_image(images['toBattleButton']):
                            time.sleep(defaultWait)
                            if find_image(images['autoButton']):
                                 if find_image(images['x5Button']):
                                    time.sleep(defaultWait)
                                    if find_image_noClick(images['camButton']):
                                        attacking = True
                                        continue
                                    else:
                                        find_image(images['exitFinal'])
                                        find_image(images['exitEvent'])
                                        attacking = True
                                        continue
                                 else:
                                    attacking = True
                                    print("Problem activating x5")
                                    continue
                            else:
                                closeApp("Problem activating auto")
                        else:
                            closeApp("Problem going to battle")
                    else:
                        closeApp("Problem trying to attack")

        if find_image(images['blueChest']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click blueChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image(images['proceedButton']):
                    continue
                else:
                    if find_image(images['chestReward']):
                        time.sleep(defaultWait) # Time for chest run animation
                        if find_image(images['proceedButton']):
                            continue
                        else:
                            print("Problem closing chest reward... ending application")
                            sys.exit()
                    else:
                        print("Problem getting a chest reward... ending application")
                        sys.exit()

        if find_image(images['purpleChest']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click purpleChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image(images['proceedButton']):
                    continue
                else:
                    if find_image(images['chestReward']):
                        time.sleep(defaultWait) # Time for chest run animation
                        if find_image(images['proceedButton']):
                            continue
                        else:
                            print("Problem closing chest reward... ending application")
                            sys.exit()
                    else:
                        print("Problem getting a chest reward... ending application")
                        sys.exit()

        if find_image(images['finalChest']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click finalChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image_noClick(images['buyButton']):
                    if find_image(images['exitFinal']):
                        towerComplete = True
                        continue
                    else:
                        closeApp("Problem closing chest reward")  
                else:
                    if find_image(images['chestReward']):
                        time.sleep(defaultWait) # Time for chest run animation
                        if find_image(images['exitFinal']):
                            towerComplete = True
                            continue
                        else:
                            closeApp("Problem closing chest reward")                    
                    else:                        
                        closeApp("Problem getting a chest reward")                        

        if find_image(images['energySphere']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click energySphere, but not works!")
            else:
                takePowerUp = True
                continue

        if find_image(images['energyBase']):
            if find_image_noClick(images['menuButtons']):
                print("Tried to click energyBase, but not works!")
            else:
                takePowerUp = True
                continue

if __name__ == "__main__":
    main()
