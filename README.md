# DocuMagic - PDF and Image Conversion Tool

**DocuMagic** is a powerful web application that converts PDFs to editable DOC files with OCR (Optical Character Recognition) and bulk images to PDFs. It supports multiple languages for OCR and provides a user-friendly interface for seamless file conversion.

&#x20;

---

## Features

- **PDF to DOC Conversion:**

  - Convert PDF files to editable DOC files.
  - Supports OCR for text extraction (Bangla, English, and more).
  - Preserves document structure and formatting.

- **Image to PDF Conversion:**

  - Convert multiple images (JPG, PNG, BMP, TIFF) into a single PDF.
  - Automatically sorts images by filename.

- **User-Friendly Interface:**

  - Drag-and-drop file upload.
  - Real-time progress tracking with a progress bar.
  - Download results as a ZIP file.

- **Multi-Language Support:**

  - OCR supports Bangla, English, and bilingual documents.

- **Error Handling:**

  - Clear error messages for invalid files or processing issues.

---

## Installation

### Prerequisites

- Python 3.7+
- Tesseract OCR (with Bengali language support)
- Flask
- Other dependencies listed in `requirements.txt`

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/ProPaul25/DocuMagic.git
   cd DocuMagic
   ```

2. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Install Tesseract OCR:

   - **Windows:** Download from UB-Mannheim.
   - **Linux:**
     ```bash
     sudo apt install tesseract-ocr tesseract-ocr-ben
     ```
   - **Mac:**
     ```bash
     brew install tesseract tesseract-lang
     ```

4. Run the application:

   ```bash
   cd backend
   python app.py
   ```

5. Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

---

## Usage

1. **Select Conversion Mode:**

   - Choose between "PDF to DOC" or "Images to PDF".

2. **Upload Files:**

   - Drag and drop files or use the file picker.

3. **Select OCR Language (for PDF to DOC):**

   - Choose Bangla, English, or bilingual.

4. **Convert:**

   - Click "Convert" and wait for processing to complete.

5. **Download Results:**

   - Once processing is done, click "Download Results" to get a ZIP file.

---

## Project Structure

```
DocuMagic/
├── backend/
│   ├── app.py                # Flask application
│   ├── processor.py          # File processing logic
│   ├── config.py             # Configuration settings
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── static/
│   │   ├── css/              # CSS files
│   │   └── js/               # JavaScript files
│   └── templates/            # HTML templates
└── README.md                 # Project documentation
```

---

## Technologies Used

### Backend:

- Python
- Flask (Web Framework)
- PyMuPDF (PDF processing)
- Tesseract OCR (Text extraction)
- img2pdf (Image to PDF conversion)

### Frontend:

- HTML5
- CSS3 (Bootstrap)
- JavaScript (jQuery)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- **Tesseract OCR** for OCR support.
- **PyMuPDF** for PDF processing.
- **img2pdf** for image-to-PDF conversion.

---

## Contact

For questions or feedback, feel free to reach out:

- **GitHub:** ProPaul25

---

© 2024 Invisipaul. All rights reserved.

