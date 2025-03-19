import os
import fitz
import img2pdf
from PIL import Image
import pytesseract
from docx import Document
from tqdm import tqdm
from config import UPLOAD_FOLDER

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_pdf_to_png(pdf_path, output_dir, zoom=4):
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            png_path = os.path.join(output_dir, f"page_{page_num + 1:03d}.png")
            pix.save(png_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False

def ocr_images_to_doc(png_dir, doc_path, lang='ben'):
    try:
        doc = Document()
        png_files = sorted([f for f in os.listdir(png_dir) if f.endswith(".png")])
        
        for png_file in tqdm(png_files, desc=f"OCR processing {os.path.basename(doc_path)}"):
            img_path = os.path.join(png_dir, png_file)
            text = pytesseract.image_to_string(
                Image.open(img_path),
                lang=lang,
                config='--psm 6'
            )
            doc.add_paragraph(text)
        
        doc.save(doc_path)
        return True
    except Exception as e:
        print(f"Error OCR processing {png_dir}: {str(e)}")
        return False

def process_pdfs(input_dir, output_dir, lang='ben', session_id=None):
    png_output = os.path.join(output_dir, "PNGs")
    doc_output = os.path.join(output_dir, "DOCS")
    os.makedirs(png_output, exist_ok=True)
    os.makedirs(doc_output, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    total_files = len(pdf_files)

    # Initialize progress file
    if session_id:
        progress_path = os.path.join(UPLOAD_FOLDER, session_id, 'progress.txt')
        with open(progress_path, 'w') as f:
            f.write(f"0,{total_files}")

    for idx, pdf_file in enumerate(pdf_files, 1):
        try:
            base_name = os.path.splitext(pdf_file)[0]
            pdf_path = os.path.join(input_dir, pdf_file)
            
            png_pdf_dir = os.path.join(png_output, base_name)
            os.makedirs(png_pdf_dir, exist_ok=True)
            
            if convert_pdf_to_png(pdf_path, png_pdf_dir):
                doc_path = os.path.join(doc_output, f"{base_name}.docx")
                ocr_images_to_doc(png_pdf_dir, doc_path, lang=lang)
            
            # Update progress
            if session_id:
                with open(progress_path, 'w') as f:
                    f.write(f"{idx},{total_files}")
                    
        except Exception as e:
            print(f"\nError processing {pdf_file}: {str(e)}")

def process_images_to_pdf(input_dir, output_dir, session_id=None):
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = sorted([
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in image_extensions
    ])
    total_files = len(image_files)

    # Create progress file
    if session_id:
        progress_path = os.path.join(UPLOAD_FOLDER, session_id, 'progress.txt')
        with open(progress_path, 'w') as f:
            f.write(f"0,{total_files}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    output_pdf = os.path.join(output_dir, 'output.pdf')

    try:
        # Convert images to PDF
        with open(output_pdf, "wb") as f:
            images = []
            for idx, img_file in enumerate(image_files, 1):
                img_path = os.path.join(input_dir, img_file)
                images.append(img_path)
                
                # Update progress
                if session_id:
                    with open(progress_path, 'w') as pf:
                        pf.write(f"{idx},{total_files}")

            f.write(img2pdf.convert(images))
            
        return True
    except Exception as e:
        print(f"Error converting images to PDF: {str(e)}")
        return False