import cv2
import numpy as np
import pyautogui
import os
import time
from desktopmagic.screengrab_win32 import getRectAsImage, getScreenAsImage
import win32api
import pytesseract
import imutils

save_path = 'images/screenshots'
#template_path = 'images/bot/countButton1.png'
template_path = 'images/bot/teste.png'
template_test = 'images/HeroWars/powerUps/magicDefense.png'
# template_path = template_test

doClick = False

showImgs = False
saveScreenshots = False

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen():
    screenshot = getScreenAsImage()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    print("screenshot data: ", screenshot.dtype, screenshot.shape)

    if save_path and saveScreenshots:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_filename = os.path.join(save_path, f"screenshot_{int(time.time())}.png")
        cv2.imwrite(save_filename, screenshot)
        print(f"Screenshot saved at {save_filename}")

    return screenshot

def find_image_on_screen(template_image_path):
    screen = capture_screen()
    template = cv2.imread(template_image_path)
    # print("template img data: ", template.dtype, template.shape)

    print('Screenshot Original Dimensions: ', screen.shape)
    img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("screen", img_gray)

    print('Template Original Dimensions: ', template.shape)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("template", template_gray)
    # cv2.waitKey(0)
    img_gray = cv2.bilateralFilter(img_gray,11,17,17)
    template_gray = cv2.bilateralFilter(template_gray,11,17,17)

    if showImgs:
        cv2.imshow('Screen', screen)
        cv2.imshow('Template', template)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if template is None:
        print("Error: Unable to read the template image.")
        return None
    
    for scale in np.linspace(0.2,1.0,20)[::-1]:
        print("resizing: ", scale)
        resized = imutils.resize(template_gray, width = int(template_gray.shape[1] * scale))
        w, h = resized.shape[::-1]

        res = cv2.matchTemplate(img_gray, resized, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        found = False
        if loc:
             for pt in zip(*loc[::-1]):
                found = True
                print("Found")
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

                template_width, template_height = template.shape[1], template.shape[0]
                y, x = loc[0][0], loc[1][0]

                click_location(loc[1][0], loc[0][0], template_width, template_height)
                time.sleep(3)
                break
        
        if not found:
            cv2.imshow("resize", resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
        # if loc[0].size > 0:
        #     template_width, template_height = template.shape[1], template.shape[0]
        #     y, x = loc[0][0], loc[1][0]

        #     # Ensure that coordinates are integers
        #     x, y, template_width, template_height = map(int, (x, y, template_width, template_height))

        #     # Get monitor information for the specified point
        #     # monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((x, y)))

        #     # Get the screen resolution where the template was found
        #     # screen_width, screen_height = (
        #     #     monitor_info["Monitor"][2] - monitor_info["Monitor"][0],
        #     #     monitor_info["Monitor"][3] - monitor_info["Monitor"][1],
        #     # )
            
        #     # print("resolution: ",screen_width, "x", screen_height)


            
        #     return loc[0][0], loc[1][0], template_width, template_height
        # return None


def click_location(x, y, template_width, template_height):
    center_x = x + template_width // 2
    center_y = y + template_height // 2

    (x, y) = pyautogui.position()

    if doClick:
        pyautogui.click(center_x, center_y, _pause=False)
        pyautogui.moveTo(x, y)
        pyautogui.moveTo(x, y)  # Double check
    else:
        pyautogui.moveTo(center_x, center_y)

def read_text_from_region(x, y, width, height):
    # Capture the region around the clicked button
    screenshot = capture_screen()
    roi = screenshot[y:y + height, x:x + width]

    roi = cv2.resize(roi, (600, 360))
    
    # Convert the ROI to grayscale
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(roi_gray)
    print("teste 3: ", text)
    return text.strip()

def main():
    print("bot started!")

    find_image_on_screen(template_path)
    # location = find_image_on_screen(template_path)
    # if location:
    #     print("Image founded.")
    #     click_location(location[1], location[0], location[2], location[3])

    #     # Wait for a moment to ensure the button click has taken effect
    #     time.sleep(1)

    #     # Read the text from the clicked region
    #     text = read_text_from_region(location[1], location[0], location[2], location[3])
    #     print(f"Read text: {text}")
    # else:
    #     print("Image not found on screen.")

if __name__ == "__main__":
    main()
