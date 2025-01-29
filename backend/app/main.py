from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from mistune import markdown
from features.web_extraction.datascraper import WikiSpider, scrape_url
from pydantic import BaseModel
import requests
import pdfplumber
from bs4 import BeautifulSoup
import boto3
import os


#Diffbot imports
from features.web_extraction.diffbot_python_client.diffbot_client import DiffbotClient,DiffbotCrawl,DiffbotSpecificExtraction
from features.web_extraction.diffbot_python_client.config import API_TOKEN
import pprint
import time
from datetime import datetime
import ast

# Aure AI imports
from features.pdf_extraction.azure_ai_intelligent_doc.read_azure_ai_model import read_azure_ai_model
import base64
from io import BytesIO

app = FastAPI()

AWS_BUCKET_NAME = "pdfparserdataset"
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
) 


class URLInput(BaseModel):
    url: str
class PdfInput(BaseModel):
    file: str
    file_name: str

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

@app.post("/diffbot-scrape-url")
def diffbot_process_url(url_input: URLInput):
    diffbot = DiffbotClient()
    token = API_TOKEN
    url = url_input.url
    api = "analyze"
    response = diffbot.request(url, token, api, fields=['title', 'text', 'images', 'pageUrl', 'type'])
    if isinstance(response, str):
        try:
            response = ast.literal_eval(response)
        except Exception as e:
            print(f"Error converting response: {e}")
        exit()
    objects = response.get("objects", [])
    extracted_data = extract_for_markdownrender(objects)
    # Generate Markdown content
    markdown_content = f"# Diffbot Extracted Content\n\n" 
    markdown_content += f"**Date:** {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p %Z')}\n\n"
    for item in extracted_data:
        markdown_content += f"### Title : \n{item['title']}\n"
        markdown_content += f"### Page URL\n[{item['pageUrl']}]({item['pageUrl']})\n"
        markdown_content += f"### Identified Page Type\n[{item['type']}]({item['type']})\n"
        markdown_content += f"### Text Extracts \n{item['text']}\n"
        if 'images' in item and isinstance(item['images'], list):
            for image in item['images']:
                image_url = image['url']
                image_title = image['title']
                markdown_content += f"### Image URL: [{image_title}]({image_url})\n"
        else:
            markdown_content += f"## Images Extracts : \n No Images Found\n"
    file_name = "diffbot_scraped_url.md"
    return {
        "message": f"File {file_name} ",
        "scraped_content": markdown_content  
    }

def extract_for_markdownrender(data):
    extracted_data = []
    for obj in data:
        title = obj.get("title", "No Title Found")
        page_url = obj.get("pageUrl", "No URL Found")
        type = obj.get("type", "No Type Found")
        text = obj.get("text", "No Text Found")
        images = obj.get("images", [])

        # Extract image titles and URLs
        image_data = []
        if isinstance(images, list):
            for image in images:
                image_url = image.get("url", "No URL Found")
                image_title = image.get("title", "No Title Found")
                image_data.append({"url": image_url, "title": image_title})

        extracted_data.append({
            "title": title,
            "pageUrl": page_url,
            "type": type,
            "text": text,
            "images": image_data
        })
    return extracted_data

@app.post("/azure-intdoc-read-process-pdf")
async def azure_int_doc_process_pdf(file: UploadFile = File(...)):
    input_pdf_path = f"./temp_{file.filename}"
    with open(input_pdf_path, "wb") as f:
        f.write(await file.read())
    # print(f"Saving uploaded file to: {input_pdf_path}")
    markdown_file_path = read_azure_ai_model(input_pdf_path)
    os.remove(input_pdf_path)
    return FileResponse(markdown_file_path, media_type="text/markdown", filename="data_ex.md")

@app.post("/process-pdf")
async def process_pdf(file: UploadFile):
    with pdfplumber.open(file.file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])
    markdown_content = markdown.markdown(text)
    file_name = f"{file.filename}.md"
    # upload_to_s3(file_name, markdown_content)
    return {"message": f"File {file_name} saved to S3"}

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