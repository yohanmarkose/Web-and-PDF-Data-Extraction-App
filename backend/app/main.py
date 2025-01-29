from fastapi import FastAPI, UploadFile, Form, File
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
# import boto3
import os
from features.web_extraction.datascraper import WikiSpider, scrape_url 
from fastapi.responses import JSONResponse, FileResponse
from features.pdf_extraction.doclingextractor import pdf_docling_converter
from features.pdf_extraction.os_pdf_extraction import pdf_os_converter

from io import BytesIO

from datetime import datetime

import base64

# from services import s3
from services.s3 import S3FileManager

app = FastAPI()

AWS_BUCKET_NAME = "pdfparserdataset"
class URLInput(BaseModel):
    url: str
class PdfInput(BaseModel):
    file: str
    file_name: str

import logging

logging.basicConfig(
    filename="output_2.log",  # File name where logs will be saved
    level=logging.DEBUG,  # Log level (DEBUG logs everything)
    format="%(message)s",  # Only log the message
)
logger = logging.getLogger()


# def upload_to_s3(file_name, content):
#     s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=content)

@app.post("/scrape-url")
def process_url(url_input: URLInput):
    response = requests.get(url_input.url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    # markdown_content = markdown.markdown(text)
    result = scrape_url(url_input.url)  # Scrape the URL
    file_name = "scraped_url.md"
    # upload_to_s3(file_name, result)

    return {
        "message": f"File {file_name} ",
        "scraped_content": result  # Include the original scraped content in the response
    }

@app.post("/scrape_pdf_os")
def process_pdf_os(uploaded_pdf: PdfInput):
    # pdf_content = uploaded_pdf.read()
    # base_path = "pdf/os"
    pdf_content = base64.b64decode(uploaded_pdf.file)
    # Convert pdf_content to a BytesIO stream for pymupdf
    pdf_stream = BytesIO(pdf_content)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    base_path = f"pdf/os/{uploaded_pdf.file_name.replace('.', '')}_{timestamp}/"

    logger.info(f"base path: {base_path}")

    s3_obj = S3FileManager(AWS_BUCKET_NAME, base_path)

    logger.info(f"initialised s3 object")

    s3_obj.upload_file(AWS_BUCKET_NAME, f"{s3_obj.base_path}/{uploaded_pdf.file_name}", pdf_content)

    logger.info(f"uploaded to s3")

    result = pdf_os_converter(pdf_stream, base_path, s3_obj)

    logger.info(f"Scraped contents")

    file_name = "scraped_pdf_os.md"
    # upload_to_s3(file_name, result)

    # return {
    #     "message": f"File {file_name} ",
    #     "scraped_content": result  # Include the original scraped content in the response
    # }
    return {
            "message": f"File {file_name} "
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

