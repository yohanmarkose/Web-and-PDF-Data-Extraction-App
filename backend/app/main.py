import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import uvicorn
# import pdfplumber

# import markdown
import os
#from features.web_extraction.datascraper import WikiSpider, scrape_url 

app = FastAPI()

#AWS S3 Configurations
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

def put_file_to_bucket(file_path, bucket_name, object_name=None):
    """Put a file into S3 bucket."""
    try:
        # Create an S3 client with explicit credentials
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_path
        
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except ClientError as e:
        print(f"Error: {e}")
    except NoCredentialsError:
        print("AWS credentials not available.")

@app.post("/scrape-url")
def process_url(url_input: URLInput):
    response = requests.get(url_input.url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    # markdown_content = markdown.markdown(text)
    # result = scrape_url(url_input.url)  # Scrape the URL
    file_name = "scraped_url.md"
    bucket_name="pdfparserdataset"
    upload_to_s3(file_name, bucket_name)

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