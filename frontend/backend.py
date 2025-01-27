from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

# Initialize FastAPI app
app = FastAPI()

# Define a request model for URL input
class URLInput(BaseModel):
    url: str

# Define an endpoint to process URL input
@app.post("/process-url")
async def process_url(data: URLInput):
    # Simulate some processing logic
    processed_text = f"Processed URL: {data.url}"
    return {"processed_text": processed_text}

# Define an endpoint to process PDF input
@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Simulate some processing logic
    processed_text = f"Processed PDF: {file.filename}"
    return {"processed_text": processed_text}