import cv2
import numpy as np
import pyautogui
import os
import time
import sys
from desktopmagic.screengrab_win32 import getScreenAsImage
import pytesseract
import win32api # To detect the monitor resolution for multi-scaling

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

save_path = '../images/screenshots'

monitor_width_originalScreenshot = 1360
monitor_heigth_originalScreenshot = 768

showImgs = False
saveScreenshots = False

takePowerUp = False

resWidth = 0 
resHeight = 0

threshold = 0.8

def setShowImgs(value: bool):
    global showImgs
    showImgs = value
    
# The resolution used to take the screenshots for the module
def setResolutionScreenshots(width: int, heigth: int):
    global monitor_width_originalScreenshot, monitor_heigth_originalScreenshot
    monitor_width_originalScreenshot = width
    monitor_heigth_originalScreenshot = heigth

def setThreshold(value: float):
    global threshold
    threshold = value

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

    global showImgs
    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None

    global resWidth, resHeight
    global monitor_width_originalScreenshot, monitor_heigth_originalScreenshot
    # Calculate scaling factor based on the monitor resolution
    scaling_factor_width = resWidth / monitor_width_originalScreenshot
    scaling_factor_height = resHeight / monitor_heigth_originalScreenshot

    # print("DEBUG: ",resWidth,resHeight,monitor_width_originalScreenshot,monitor_heigth_originalScreenshot)

    template_resized = cv2.resize(template, None, fx=scaling_factor_width, fy=scaling_factor_height)

    # cv2.imshow('Template', template)
    # cv2.imshow('Template_resized', template_resized)
    # cv2.waitKey(0)

    res = cv2.matchTemplate(screen, template_resized, cv2.TM_CCOEFF_NORMED)

    if showImgs:
        cv2.imshow('Template_resized', template_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    global threshold
    loc = np.where(res >= threshold)

    if loc[0].size > 0:
        # Get the width and height of the template image
        template_width, template_height = template_resized.shape[1], template_resized.shape[0]
        y, x = loc[0][0], loc[1][0]

        return x, y, template_width, template_height  # Return coordinates of the match
    return None

def find_image_monitor_resolution(template_image_path):
    # Find a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path)

    global showImgs
    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    global threshold
    loc = np.where(res >= threshold)
    if loc[0].size > 0:
        # Get the width and height of the template image
        template_width, template_height = template.shape[1], template.shape[0]
        y, x = loc[0][0], loc[1][0]

        # Ensure that coordinates are integers
        x, y, template_width, template_height = map(int, (x, y, template_width, template_height))

        # Get monitor information for the specified point
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((x, y)))
       
        # Get the screen resolution where the template was found
        screen_width, screen_height = (
            monitor_info["Monitor"][2] - monitor_info["Monitor"][0],
            monitor_info["Monitor"][3] - monitor_info["Monitor"][1],
        )

        return screen_width, screen_height  # Return monitor resolution
    return None

def get_image_location_on_screen(template_image_path):
    # Find all occurrences of a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path)

    global showImgs
    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None

    global threshold
    while True:
        global resWidth, resHeight
        # Calculate scaling factor based on the monitor resolution
        scaling_factor_width = resWidth / monitor_width_originalScreenshot
        scaling_factor_height = resHeight / monitor_heigth_originalScreenshot

        template_resized = cv2.resize(template, None, fx=scaling_factor_width, fy=scaling_factor_height)
        
        res = cv2.matchTemplate(screen, template_resized, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        if loc[0].size > 0:
            # Get the coordinates of the match
            y, x = loc[0][0], loc[1][0]

            # Get the width and height of the template image
            template_width, template_height = template.shape[1], template.shape[0]

            return (x, y, template_width, template_height)
        else:
            break

def find_all_images_on_screen(template_image_path):
    # Find all occurrences of a particular image on the screen
    screen = capture_screen()
    template = cv2.imread(template_image_path)

    global showImgs
    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None

    matches = []

    global threshold
    while True:
        global resWidth, resHeight
        # Calculate scaling factor based on the monitor resolution
        scaling_factor_width = resWidth / monitor_width_originalScreenshot
        scaling_factor_height = resHeight / monitor_heigth_originalScreenshot

        template_resized = cv2.resize(template, None, fx=scaling_factor_width, fy=scaling_factor_height)
        
        res = cv2.matchTemplate(screen, template_resized, cv2.TM_CCOEFF_NORMED)

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

def read_text_from_region(x, y, width, height, onlyNumbers = False):
    # Capture the region around the clicked button
    screenshot = capture_screen()
    roi = screenshot[y:y + height, x:x + width]
    # cv2.imwrite("roi_image.png", roi)

    # roi = cv2.resize(roi, (507, 444)) # four times bigger than the original

    # Convert the ROI to grayscale
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("roi_gray_image.png", roi_gray)
    
    if onlyNumbers:
        text = pytesseract.image_to_string(roi_gray, config='--psm 6')
        text = text.replace('/', '7').replace('u', '0')
    else:
        text = pytesseract.image_to_string(roi_gray)

    return text.strip()

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
    
def get_monitor_resolution(max_attempts, image, wait = 0):
    time.sleep(wait)
    
    filename = os.path.basename(image) # Get the filename from the path
    name = os.path.splitext(filename)[0] # remove extension
    
    attempts = 0
    while attempts < max_attempts:
        # Look for tower
        resolution = find_image_monitor_resolution(image)
        
        if resolution is not None:
            global resWidth, resHeight
            resWidth, resHeight = resolution
            print(f"{name} found.", "Monitor resolution: ",resWidth,"x",resHeight)
            return resWidth, resHeight
        # If none of the images are found, increment attempts and try again
        attempts += 1
        print(f"No relevant image found for {name}. Retrying...")

    if attempts == max_attempts:
        print(f"Max attempts reached. Exiting.")
        return None, None

def find_image_paths(folder_path = ''):
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller one-file mode
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = 'images/HeroWars' if folder_path == '' else 'images/HeroWars/' + folder_path

    images = {}
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_name = os.path.splitext(file)[0]
                images[image_name] = os.path.join(root, file)

    return images
        