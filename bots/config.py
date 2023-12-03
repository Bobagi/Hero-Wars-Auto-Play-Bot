import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def setTesseractPath(path):
    global tesseract_cmd
    tesseract_cmd = path