import fitz
from PIL import Image
import io
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

VISION_ENDPOINT = "CQGUlmrfZcIZRniOrjph1Pi6uCSuDYL1OUszKy5wDe3m2eQiTR8aJQQJ99BAACYeBjFXJ3w3AAAFACOGCQRa"
VISION_KEY="https://azure-visual-studio-instance-ev1.cognitiveservices.azure.com/"

# Initialize the Azure OCR client
credential = AzureKeyCredential(VISION_KEY)

def sample_ocr_image_file():
    pdf_document = fitz.open("D:/BigData/DAMG7245_Assignment01/Prototypes/enterprise/pdf_samples/handwrittend_export_2.pdf")
    total_pages = pdf_document.page_count

    for page_num in range(total_pages):
        # Convert page to an image
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        
        # Save the image as a byte stream (in-memory)
        image_stream = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(image_stream, format="PNG")
        image_stream.seek(0)  # Reset stream position

        text = extract_text_from_image(image_stream)
        print(f"Text from page {page_num + 1}:\n{text}\n")

def extract_text_from_image(image_stream):
    # Implement your OCR extraction logic here
    # For example, using Azure OCR client
    pass

if __name__ == "__main__":
    sample_ocr_image_file()