import cv2
import numpy as np
import pyautogui
import os
import time
import sys
from desktopmagic.screengrab_win32 import getRectAsImage, getScreenAsImage
from collections import OrderedDict
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

save_path = 'images/screenshots'

showImgs = False
saveScreenshots=False

def capture_screen():
    screenshot = getScreenAsImage()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Use RGB2BGR for OpenCV

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
        y, x = loc[0][0], loc[1][0]

        return x, y, template_width, template_height  # Return coordinates of the match
    return None

def find_all_images_on_screen(template_image_path):
    # Find all occurrences of a particular image on the screen
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

    matches = []

    threshold = 0.8
    while True:
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        if loc[0].size > 0:
            # Get the coordinates of the match
            y, x = loc[0][0], loc[1][0]

            # Get the width and height of the template image
            template_width, template_height = template.shape[1], template.shape[0]

            matches.append((x, y, template_width, template_height))

            # Update the region around the found match to ignore it in the next iteration
            screen[y:y + template_height, x:x + template_width] = 0
        else:
            break

    return matches

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

def choose_power_up(power_ups_types, images):
    desired_order = ['damage', 'armor', 'magicDefense']
    power_ups_types = OrderedDict((key, power_ups_types[key]) for key in desired_order)
    # power_ups_types = [damage, armor, magicDefense]
    max_attempts = 3
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
                    newYpos = location[1] + location[3] # Repositioning the pivot below the founded image
                    newWidth = location[2] + correctionWidth
                    description = read_text_from_region(location[0] - (correctionWidth // 2), newYpos, newWidth, location[3])
                    if "Comprou" in description:
                        print(f"Upgrade {power_up} already bought.")
                        continue

                    print(f"Upgrade {power_up} powerUp chosen.")
                    click_location(location[0], location[1], location[2], location[3])

                    # Check if the message of not enoght skulls appeared
                    if find_image(max_attempts, images['okButton']):
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

def read_text_from_region(x, y, width, height):
    # Capture the region around the clicked button
    screenshot = capture_screen()
    roi = screenshot[y:y + height, x:x + width]
    # cv2.imwrite("roi_image.png", roi)

    roi = cv2.resize(roi, (507, 444)) # four times bigger than the original
    
    # Convert the ROI to grayscale
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("roi_gray_image.png", roi_gray)

    text = pytesseract.image_to_string(roi_gray)

    return text.strip()

def main():
    print("HeroWars bot - Tower -> starting in 2 seconds!")
    time.sleep(2)
    print("HeroWars bot - Tower -> bot ready!")

    global takePowerUp
    takePowerUp = False
    attacking = False
    towerComplete = False

    images = find_image_paths('images/HeroWars')
    powerUpsImages = find_image_paths('images/HeroWars/powerUps')
    
    max_attempts = 3
    defaultWait = 1

    if find_image(max_attempts, images['tower']):
        print("Entering the tower...")
    else:
        print("Already in tower!")

    while True:
        print(f"Awaiting {defaultWait} seconds for next command...")
        time.sleep(defaultWait)

        if towerComplete:
            if find_image(max_attempts, images['changeSkull']):
                if find_image(max_attempts, images['changeSkullIntoCoin']):
                    if find_image(max_attempts, images['towerPoints']):
                        if find_image(max_attempts, images['collectAll']):
                            if find_image(max_attempts, images['exitFinal']):
                                find_image(max_attempts, images['exitFinal'])
                                closeApp("Tower Completed!")
                            else:
                                continue
                        else:
                            find_image(max_attempts, images['exitFinal'])
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                if find_image(max_attempts, images['towerPoints']):
                    if find_image(max_attempts, images['collectAll']):
                        if find_image(max_attempts, images['exitFinal']):
                            find_image(max_attempts, images['exitFinal'])
                            closeApp("Tower Completed!")
                        else:
                            continue
                    else:
                        find_image(max_attempts, images['exitFinal'])
                        find_image(max_attempts, images['exitFinal'])
                        closeApp("Tower Completed!")
                else:
                    continue

        if attacking:
            while True:
                time.sleep(2)
                if find_image(max_attempts, images['okBattleButton']):
                    find_image(max_attempts, images['okBattleButton']) # Double Check
                    attacking = False
                    break

        # PowerUps
        if takePowerUp:
            power_up_done = choose_power_up(powerUpsImages, images)

            if not power_up_done:
                print("Problem choosing a power up...")
                break
            else:
                takePowerUp = False
                if find_image(max_attempts, images['exitButton']):
                    if find_image(max_attempts, images['arrowRight']):
                        print("Going to next floor...")
                        time.sleep(2)
                    else:
                        if find_image(max_attempts, images['arrowLeft']):
                            print("Going to next floor...")
                            time.sleep(2)
                        else:
                            print("Problem going to the next floor after power up... ending application")
                            sys.exit()
                else:
                    print("Problem closing power up window... ending application")
                    sys.exit()

        if find_image(max_attempts, images['battleDoor']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click battleDoor, but not works!")
            else:
                if find_image(max_attempts, images['skipButton']):
                    continue
                else:
                    if find_image(max_attempts, images['attackButton']):                        
                        if find_image(max_attempts, images['toBattleButton']):
                            time.sleep(2)
                            if find_image(max_attempts, images['autoButton']):
                                 if find_image(max_attempts, images['x5Button']):
                                    attacking = True
                                    continue
                                 else:
                                    closeApp("Problem activating x5")
                            else:
                                closeApp("Problem activating auto")
                        else:
                            closeApp("Problem going to battle")
                    else:
                        closeApp("Problem trying to attack")

        if find_image(max_attempts, images['blueChest']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click blueChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image(max_attempts, images['continueButton']):
                    continue
                else:
                    if find_image(max_attempts, images['chestReward']):
                        time.sleep(2) # Time for chest run animation
                        if find_image(max_attempts, images['continueButton']):
                            continue
                        else:
                            print("Problem closing chest reward... ending application")
                            sys.exit()
                    else:
                        print("Problem getting a chest reward... ending application")
                        sys.exit()

        if find_image(max_attempts, images['purpleChest']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click purpleChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image(max_attempts, images['continueButton']):
                    continue
                else:
                    if find_image(max_attempts, images['chestReward']):
                        time.sleep(2) # Time for chest run animation
                        if find_image(max_attempts, images['continueButton']):
                            continue
                        else:
                            print("Problem closing chest reward... ending application")
                            sys.exit()
                    else:
                        print("Problem getting a chest reward... ending application")
                        sys.exit()

        if find_image(max_attempts, images['finalChest']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click finalChest, but not works!")
            else:
                # First check if the reward inst already picked
                if find_image_noClick(max_attempts, images['buyButton']):
                    if find_image(max_attempts, images['exitFinal']):
                        towerComplete = True
                        continue
                    else:
                        closeApp("Problem closing chest reward")  
                else:
                    if find_image(max_attempts, images['chestReward']):
                        time.sleep(2) # Time for chest run animation
                        if find_image(max_attempts, images['exitFinal']):
                            towerComplete = True
                            continue
                        else:
                            closeApp("Problem closing chest reward")                    
                    else:                        
                        closeApp("Problem getting a chest reward")                        

        if find_image(max_attempts, images['energySphere']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click energySphere, but not works!")
            else:
                takePowerUp = True
                continue

        if find_image(max_attempts, images['energyBase']):
            if is_in_floor_scene(max_attempts, images['menuButtons']):
                print("Tried to click energyBase, but not works!")
            else:
                takePowerUp = True
                continue

def is_in_floor_scene(max_attempts, image):
    time.sleep(1)
    return find_image(max_attempts, image)

def find_image_noClick(max_attempts, image, name = '', wait = 0):
    return find_image(max_attempts, image, False, name, wait)

def find_image(max_attempts, image, click = True, name = '', wait = 0):
    time.sleep(wait)
    if name == '':
        filename = os.path.basename(image) # Get the filename from the path
        name = os.path.splitext(filename)[0] # remove extension
    
    attempts = 0
    while attempts < max_attempts:
        # Look for tower
        location = find_image_on_screen(image)
        if location:
            print(f"{name} found.")
            if click: 
                click_location(location[0], location[1], location[2], location[3])
            return True
        # If none of the images are found, increment attempts and try again
        attempts += 1
        print(f"No relevant image found for {name}. Retrying...")

    if attempts == max_attempts:
        print(f"Max attempts reached. Exiting.")
        return False

def find_image_paths(folder_path):
    images = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_name = os.path.splitext(file)[0]
                images[image_name] = os.path.join(root, file)
    return images

def closeApp(msg):
    print(msg, "... ending application")
    sys.exit()

if __name__ == "__main__":
    main()
