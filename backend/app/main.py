from fastapi import FastAPI, UploadFile, Form, File
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
# import boto3
import os
from features.web_extraction.datascraper import WikiSpider, scrape_url, convert_json_to_markdown, convert_table_to_markdown
from fastapi.responses import JSONResponse, FileResponse
from features.pdf_extraction.doclingextractor import pdf_docling_converter
from features.pdf_extraction.os_pdf_extraction import pdf_os_converter

from io import BytesIO

import re
from datetime import datetime

import base64

from dotenv import load_dotenv
load_dotenv()

# Read values
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
# from services import s3
from services.s3 import S3FileManager

app = FastAPI()

class URLInput(BaseModel):
    url: str
class PdfInput(BaseModel):
    file: str
    file_name: str

@app.post("/scrape_url_os")
def process_url(url_input: URLInput):
    json_result = scrape_url(url_input.url)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = url_to_folder_name(url_input.url)
    base_path = f"web/os/{folder_name}_{timestamp}/"
    s3_obj = S3FileManager(AWS_BUCKET_NAME, base_path)
    s3_obj.upload_file(AWS_BUCKET_NAME, f"{s3_obj.base_path}/web_url.txt", str(url_input.url))

    md_result = convert_json_to_markdown(json_result) # Scrape the URL
    s3_obj.upload_file(AWS_BUCKET_NAME, f"{s3_obj.base_path}/extracted_data.md", str(md_result))
    # upload_to_s3(file_name, result)

    return {
        "message": f"Data Scraped and stored in https://{s3_obj.bucket_name}.s3.amazonaws.com/{s3_obj.base_path}/extracted_data.md",
        "scraped_content": md_result  # Include the original scraped content in the response
    }

@app.post("/scrape_pdf_os")
def process_pdf_os(uploaded_pdf: PdfInput):
    pdf_content = base64.b64decode(uploaded_pdf.file)
    # Convert pdf_content to a BytesIO stream for pymupdf
    pdf_stream = BytesIO(pdf_content)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    base_path = f"pdf/os/{uploaded_pdf.file_name.replace('.', '')}_{timestamp}/"
    s3_obj = S3FileManager(AWS_BUCKET_NAME, base_path)
    s3_obj.upload_file(AWS_BUCKET_NAME, f"{s3_obj.base_path}/{uploaded_pdf.file_name}", pdf_content)
    file_name, result = pdf_os_converter(pdf_stream, base_path, s3_obj)
    return {
        "message": f"File {file_name} ",
        "scraped_content": result  # Include the original scraped content in the response
    }

@app.post("/pdf-docling-converter/")
async def process_pdf_to_docling(file: UploadFile = File(...)):
    """
    Asynchronously processes an uploaded PDF file and converts it to a markdown file.

    Args:
        file (UploadFile): The uploaded PDF file to be processed.

    Returns:
        FileResponse: A response containing the converted markdown file with a media type of "text/markdown".

    Raises:
        Exception: If there is an error during file processing or conversion.
    """
    input_pdf_path = f"temp_{file.filename}"
    with open(input_pdf_path, "wb") as f:
        f.write(await file.read())
    markdown_file_path = pdf_docling_converter(input_pdf_path)
    os.remove(input_pdf_path)
    return FileResponse(markdown_file_path, media_type="text/markdown", filename="data_ex.md")

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def url_to_folder_name(url):
    # Extract the main domain
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        domain = match.group(1).replace("www.", "")
    else:
        return None
    safe_folder_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", domain)
    
    return safe_folder_name