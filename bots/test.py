from screeninfo import get_monitors
from desktopmagic.screengrab_win32 import getRectAsImage, getScreenAsImage
import os
import time

save_path = 'images/screenshots'
show_images = False

def capture_and_save_screenshots(show_image=False):
    # Create the screenshots folder if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("monitors: ",get_monitors())

    for i, monitor in enumerate(get_monitors()):
        # Take a screenshot of the current monitor
        print(monitor.x, monitor.y, monitor.width, monitor.height)
        screenshot = getRectAsImage((monitor.x, monitor.y, monitor.width, monitor.height))
        # screenshot = getScreenAsImage()

        # Save the screenshot with a timestamp as the filename
        save_filename = os.path.join(save_path, f"screenshot_{int(time.time())}_monitor{i + 1}_{monitor.is_primary}.png")
        screenshot.save(save_filename)

        print(f"Screenshot saved at {save_filename} - Monitor: {monitor.name}")

        # Optionally show the screenshot
        if show_image:
            screenshot.show()

if __name__ == "__main__":
    capture_and_save_screenshots(show_images)
