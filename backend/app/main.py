from fastapi import FastAPI, UploadFile, Form
from mistune import markdown
from features.web_extraction.datascraper import WikiSpider, scrape_url
from pydantic import BaseModel
import requests
import pdfplumber
from bs4 import BeautifulSoup
import boto3
import ast

#Diffbot imports
from features.web_extraction.diffbot_python_client.diffbot_client import DiffbotClient,DiffbotCrawl,DiffbotSpecificExtraction
from features.web_extraction.diffbot_python_client.config import API_TOKEN
import pprint
import time
from datetime import datetime

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
    markdown_content = f"# Extracted Data\n\n"
    markdown_content += f"**Date:** {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p %Z')}\n\n"
    for item in extracted_data:
        markdown_content += f"## Title : \n{item['title']}\n"
        markdown_content += f"## Page URL\n[{item['pageUrl']}]({item['pageUrl']})\n"
        markdown_content += f"## Identified Page Type\n[{item['type']}]({item['type']})\n"
        markdown_content += f"## Text Extracts \n{item['text']}\n"
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

# @app.post("/process-pdf")
# async def process_pdf(file: UploadFile):
#     with pdfplumber.open(file.file) as pdf:
#         text = "\n".join([page.extract_text() for page in pdf.pages])
#     markdown_content = markdown.markdown(text)
#     file_name = f"{file.filename}.md"
#     # upload_to_s3(file_name, markdown_content)
#     return {"message": f"File {file_name} saved to S3"}

@app.post("/process-pdf")
async def process_pdf(file: UploadFile):
    with pdfplumber.open(file.file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])
    markdown_content = markdown.markdown(text)
    file_name = f"{file.filename}.md"
    # upload_to_s3(file_name, markdown_content)
    return {"message": f"File {file_name} saved to S3"}

# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)