import cv2
import numpy as np
import pyautogui
import os
import time
from desktopmagic.screengrab_win32 import getRectAsImage, getScreenAsImage
import sys

save_path = 'images/screenshots'

door = 'images/HeroWars/battleDoor.png'
arrowRight = 'images/HeroWars/arrowRight.png'
blueChest = 'images/HeroWars/blueChest.png'
blueChestReward = 'images/HeroWars/blueChestReward.png'
continueButton = 'images/HeroWars/continueButton.png'
energySphere = 'images/HeroWars/energySphere.png'
energyBase = 'images/HeroWars/energyBase.png'
exitButton = 'images/HeroWars/exitButton.png'
skipButton = 'images/HeroWars/skipButton.png'

damage1 = 'images/HeroWars/powerUps/damage1.png'
damage2 = 'images/HeroWars/powerUps/damage2.png'
damage3 = 'images/HeroWars/powerUps/damage3.png'
damage4 = 'images/HeroWars/powerUps/damage4.png'
armor1 = 'images/HeroWars/powerUps/armor1.png'
armor2 = 'images/HeroWars/powerUps/armor2.png'
armor4 = 'images/HeroWars/powerUps/armor4.png'
magicDefense1 = 'images/HeroWars/powerUps/magicDefense1.png'
magicDefense3 = 'images/HeroWars/powerUps/magicDefense3.png'
magicDefense4 = 'images/HeroWars/powerUps/magicDefense4.png'

showImgs = False
saveScreenshots=False

TakePowerUp = False

def capture_screen():
    # Take a screenshot of the entire screen
    # screenshot = pyautogui.screenshot()
    screenshot = getScreenAsImage()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Use RGB2BGR for OpenCV

     # Save the screenshot
    if save_path and saveScreenshots:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_filename = os.path.join(save_path, f"screenshot_{int(time.time())}.png")
        cv2.imwrite(save_filename, screenshot)

    return screenshot

def find_image_on_screen(template_image_path):
    # Find a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path)

    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    loc = np.where(res >= threshold)
    if loc[0].size > 0:
        # Get the width and height of the template image
        template_width, template_height = template.shape[1], template.shape[0]

        return loc[0][0], loc[1][0], template.shape[1], template.shape[0]  # Return coordinates of the match
    return None

def click_location(x, y, template_width, template_height):
    # Calculate the center coordinates of the template
    center_x = x + template_width // 2
    center_y = y + template_height // 2

    # Save mouse position
    (x, y) = pyautogui.position()

    # Click at the provided x, y coordinates
    pyautogui.click(center_x, center_y, _pause=False)

    # Move back to where the mouse was before click
    pyautogui.moveTo(x, y)
    pyautogui.moveTo(x, y) # Double check

def powerUp():
    max_attempts = 3
    attempts = 0
    max_powerUps = 3
    powerUpsTaken = 0
    while attempts < max_attempts and powerUpsTaken < max_powerUps:
        
        location = find_image_on_screen(damage4)
        if location:
            print("Upgrade damage IV powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(damage3)
        if location:
            print("Upgrade damage III powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(damage2)
        if location:
            print("Upgrade damage II powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(damage1)
        if location:
            print("Upgrade damage I powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue

        location = find_image_on_screen(armor4)
        if location:
            print("Upgrade armor IV powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(armor2)
        if location:
            print("Upgrade armor II powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(armor1)
        if location:
            print("Upgrade armor I powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        
        location = find_image_on_screen(magicDefense4)
        if location:
            print("Upgrade magic defense IV powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(magicDefense3)
        if location:
            print("Upgrade magic defense III powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue
        location = find_image_on_screen(magicDefense1)
        if location:
            print("Upgrade magic defense I powerUp choosed.")
            click_location(location[1], location[0], location[2], location[3])
            powerUpsTaken += 1
            continue

        # If none of the images are found, increment attempts and try again
        attempts += 1
        print("No relevant image found on PowerUp. Retrying...")
        return False
    
    if attempts == max_attempts:
        print(f"Max attempts to choose a power up. Exiting.")
        return False
    
    return True

def main():
    TakePowerUp = False
    print("HeroWars bot - Tower -> starting in 2 seconds!")
    time.sleep(2)  # Wait for 1 second before starting the bot actions
    print("HeroWars bot - Tower -> bot ready!")

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        print("Awaiting 2 seconds for next command...")
        time.sleep(2)  # Wait for 1 second before starting the bot actions

        # PowerUps
        if TakePowerUp:
            powerUpDone = powerUp()
            if not powerUpDone:
                print("Problem chosing a power up...")
                break
            else:
                TakePowerUp = False
           
                location = find_image_on_screen(exitButton)
                if location:
                    click_location(location[1], location[0], location[2], location[3])

                    location = find_image_on_screen(arrowRight)
                    if location:
                        click_location(location[1], location[0], location[2], location[3])
                    else:
                        print("Problem going to next floor after power up... ending application")
                        sys.exit()
                else:
                    print("Problem closing power up window... ending application")
                    sys.exit()

        # Look for battleDoor
        location = find_image_on_screen(door)
        if location:
            print("Battle Door found.")
            click_location(location[1], location[0], location[2], location[3])
            subAttempts = 0
            time.sleep(1)
            while subAttempts < max_attempts:
                location = find_image_on_screen(skipButton)
                if location:
                    print("Skip Button found.")
                    click_location(location[1], location[0], location[2], location[3])
                    break
            attempts += 1
            continue

        # Look for blueChest, battleDoor, or energySphere
        location = find_image_on_screen(blueChest)
        if location:
            print("Blue Chest found.")
            click_location(location[1], location[0], location[2], location[3])
            continue

        location = find_image_on_screen(energyBase)
        if location:
            print("Energy Base found.")
            TakePowerUp = True
            click_location(location[1], location[0], location[2], location[3])
            continue

        location = find_image_on_screen(energySphere)
        if location:
            print("Energy Sphere found.")
            TakePowerUp = True
            click_location(location[1], location[0], location[2], location[3])
            continue

        # If none of the images are found, increment attempts and try again
        attempts += 1
        print("No relevant image found. Retrying...")

    if attempts == max_attempts:
        print(f"Max attempts reached. Exiting.")

if __name__ == "__main__":
    main()
