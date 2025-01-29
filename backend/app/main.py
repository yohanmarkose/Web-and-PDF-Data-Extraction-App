from fastapi import FastAPI, UploadFile, Form, File
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import boto3
import os, io
from features.web_extraction.datascraper import WikiSpider, scrape_url 
from fastapi.responses import JSONResponse, FileResponse
from features.pdf_extraction.doclingextractor import docling_converter

app = FastAPI()

# AWS S3 Configurations
AWS_ACCESS_KEY_ID = "AKIAYKFQQUN54HLOMPMN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = "pdfparserdataset"
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


class URLInput(BaseModel):
    url: str


def upload_to_s3(file_name, content):
    s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=content)

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

@app.post("/open-source-scrape-url/")
def process_os_url(url_input: URLInput):
    response = requests.get(url_input.url)
    soup = BeautifulSoup(response.content, "html.parser")
    input_html_path = f"temp_{soup.title.string}.html"
    with open(input_html_path, "wb") as f:
        f.write(soup.prettify("utf-8"))
    markdown_file_path = docling_converter(input_html_path)
    return FileResponse(markdown_file_path, media_type="text/markdown", filename="data_ex.md")
    
    
@app.post("/docling-scrape-url/")
def process_docling_url(url_input: URLInput):
    markdown_file_path = docling_converter(url_input)
    return FileResponse(markdown_file_path, media_type="text/markdown", filename="data_ex.md")

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
    pdf_stream = await file.read()
    # with open(input_pdf_path, "wb") as f:
    #     f.write(await file.read())
    markdown_file_path = docling_converter(io.BytesIO(pdf_stream))
    print(markdown_file_path)
    # os.remove(input_pdf_path)
    return FileResponse(markdown_file_path, media_type="text/markdown", filename="data_ex.md")

# @app.post("/process-pdf")
# async def process_pdf(file: UploadFile):
#     with pdfplumber.open(file.file) as pdf:
#         text = "\n".join([page.extract_text() for page in pdf.pages])
#     markdown_content = markdown.markdown(text)
#     file_name = f"{file.filename}.md"
#     # upload_to_s3(file_name, markdown_content)
#     return {"message": f"File {file_name} saved to S3"}

# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

