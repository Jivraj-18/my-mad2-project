from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
def convert_to_png(image):
    with Image.open(image) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return img

def extract_first_page_as_png(pdf_path, output_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    if images : 
        images[0].save(output_path,'PNG')

def get_num_pages(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
    
            print(file)
            num_pages = len(pdf_reader.pages)
        return num_pages
    except Exception as e:
        print(f"Error counting pages: {e}")
        return None
