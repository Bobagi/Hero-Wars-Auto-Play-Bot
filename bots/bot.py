import cv2
import numpy as np
import pyautogui
import time

def capture_screen():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def find_image_on_screen(template_image_path):
    # Find a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path, 0)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if loc[0].size > 0:
        return loc[0][0], loc[1][0]  # Return coordinates of the match
    return None

def click_location(x, y):
    # Click at the provided x, y coordinates
    pyautogui.click(x, y)

def main():
    print("bot started!")
    time.sleep(5)  # Wait for 5 seconds before starting the bot actions
    # Your bot logic here
    # For example, to find an image on the screen and click it:
    location = find_image_on_screen('images/bot/countButton.jpg')
    if location:
        click_location(location[1], location[0])
    else:
        print("Image not found on screen.")

if __name__ == "__main__":
    main()
