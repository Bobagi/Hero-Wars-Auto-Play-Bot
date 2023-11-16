# import pytesseract as tess
# from PIL import Image

# path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# tess.pytesseract.tesseract_cmd = path
# # img = Image.open('images/bot/countButton.png')

# # Example: Grayscale and thresholding
# img = Image.open('images/bot/countButton.png').convert('L')
# img = img.point(lambda x: 0 if x < 128 else 255)
# img.show()
# try:
#     # text = tess.image_to_string(img)
#     text = tess.image_to_string(img, lang='eng')
#     print("Text:", text)
# except Exception as e:
#     print("Error:", e)


import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('images/bot/countButton.png')

img = cv2.resize(img, (600, 360))

print("teste 1: ", pytesseract.image_to_string(img))

roi_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Save the ROI image for debugging
cv2.imwrite("roi_image.png", img)

# Perform text recognition using pytesseract
text = pytesseract.image_to_string(roi_gray)

print("teste 2: ", text)