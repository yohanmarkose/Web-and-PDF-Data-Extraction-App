from fastapi import FastAPI
# from  models import Todo

# app = FastAPI()

# todos = []

# @app.get("/todos")
# async def get_todo():
#     return {"todos": todos}

# @app.post("/todos")
# async def create_todo(todo: Todo):
#     todos.append(todo)
#     return {"message": "Todo has been added"}

from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
# import pdfplumber
# import boto3
# import markdown
import os
from features.web_extraction.datascraper import WikiSpider, scrape_url 

app = FastAPI()

# AWS S3 Configurations
# AWS_ACCESS_KEY_ID = "your_aws_access_key"
# AWS_SECRET_ACCESS_KEY = "your_aws_secret_key"
# AWS_BUCKET_NAME = "your_bucket_name"
# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )

class URLInput(BaseModel):
    url: str


# def upload_to_s3(file_name, content):
#     s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=content)

@app.post("/scrape-url")
def process_url(url_input: URLInput):
    response = requests.get(url_input.url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    # markdown_content = markdown.markdown(text)
    # result = scrape_url(url_input.url)  # Scrape the URL
    file_name = "scraped_url.md"

    return {
        "message": f"File {file_name} ",
        "scraped_content": text  # Include the original scraped content in the response
    }

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

