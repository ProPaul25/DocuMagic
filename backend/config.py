import os

UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'pdf_ocr_uploads')
ALLOWED_EXTENSIONS = {
    'pdf': {'pdf'},
    'image': {'jpg', 'jpeg', 'png', 'bmp', 'tiff'}
}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# Uncomment and modify for Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'