import cv2
import numpy as np
import pyautogui
import time
import os

save_path = 'images/screenshots'
template_path = 'images/bot/countButton.jpg'
def capture_screen():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Use RGB2BGR for OpenCV
    print("screenshot data: ", screenshot.dtype, screenshot.shape)

     # Save the screenshot
    if save_path:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_filename = os.path.join(save_path, f"screenshot_{int(time.time())}.png")
        cv2.imwrite(save_filename, screenshot)
        print(f"Screenshot saved at {save_filename}")

    return screenshot

def find_image_on_screen(template_image_path):
    # Find a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path)
    print("template img data: ",template.dtype, template.shape)

    if template is None:
        print("Error: Unable to read the template image.")
        return None

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
    location = find_image_on_screen(template_path)
    if location:
        print("Image founded.")
        click_location(location[1], location[0])
    else:
        print("Image not found on screen.")

if __name__ == "__main__":
    main()
