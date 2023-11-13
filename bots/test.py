import cv2
import numpy as np
import pyautogui
import os
import time
from screeninfo import get_monitors

save_path = 'images/screenshots'
template_path = 'images/bot/countButton.jpg'
showImgs = False

def capture_and_save_screenshots(show_image=False):
    # Create the screenshots folder if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for monitor in get_monitors():
        # Set the current monitor
        pyautogui.moveTo(monitor.x + 1, monitor.y + 1)

        # Take a screenshot of the current monitor
        screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Save the screenshot with a timestamp as the filename
        save_filename = os.path.join(save_path, f"screenshot_{int(time.time())}_monitor{monitor.x}_{monitor.is_primary}.png")
        cv2.imwrite(save_filename, screenshot)

        print(f"Screenshot saved at {save_filename} - Monitor: {monitor.name}")

        # Optionally show the screenshot
        if show_image:
            cv2.imshow('Screenshot', screenshot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_save_screenshots()