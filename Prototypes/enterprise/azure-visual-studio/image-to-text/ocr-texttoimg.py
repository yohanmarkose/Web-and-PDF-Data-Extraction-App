# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
DESCRIPTION:
    This sample demonstrates how to extract printed or hand-written text for the image file sample.jpg
    using a synchronous client.

    The synchronous (blocking) `analyze` method call returns an `ImageAnalysisResult` object.
    Its `read` property (a `ReadResult` object) includes a list of `TextBlock` objects. Currently, the
    list will always contain one element only, as the service does not yet support grouping text lines
    into separate blocks. The `TextBlock` object contains a list of `DocumentLine` object. Each one includes: 
    - The text content of the line.
    - A `BoundingPolygon` coordinates in pixels, for a polygon surrounding the line of text in the image.
    - A list of `DocumentWord` objects.
    Each `DocumentWord` object contains:
    - The text content of the word.
    - A `BoundingPolygon` coordinates in pixels, for a polygon surrounding the word in the image.
    - A confidence score in the range [0, 1], with higher values indicating greater confidences in
      the recognition of the word. 

USAGE:
    python sample_ocr_image_file.py

    Set these two environment variables before running the sample:
    1) VISION_ENDPOINT - Your endpoint URL, in the form https://your-resource-name.cognitiveservices.azure.com
                         where `your-resource-name` is your unique Azure Computer Vision resource name.
    2) VISION_KEY - Your Computer Vision key (a 32-character Hexadecimal number)
"""

   

def sample_ocr_image_file():
    import os
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential

    # Set the values of your computer vision endpoint and computer vision key
    # as environment variables:
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # [START read]
    # Load image to analyze into a 'bytes' object
    import fitz
    from PIL import Image
    import io
    pdf_document = fitz.open("D:/BigData/DAMG7245_Assignment01/Prototypes/enterprise/azure-visual-studio/OGS-Pre-Arrival-Handbook/wikipedia_example.pdf")

    for page_num in range(2):
        # Convert page to an image
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        
        # Save the image as a byte stream (in-memory)
        image_stream = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(image_stream, format="PNG")
        image_stream.seek(0)  # Reset stream position

    # Extract text (OCR) from an image stream. This will be a synchronously (blocking) call.
    markdown_file = "ocr_results.md"
    
    with open(markdown_file, "w", encoding="utf-8") as md_file:
        # Iterate over pages (e.g., first 2 pages)
        for page_num in range(2):
            # Convert page to an image
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            
            # Save the image as a byte stream (in-memory)
            image_stream = io.BytesIO()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(image_stream, format="PNG")
            image_stream.seek(0)  # Reset stream position

            # Extract text (OCR) from the image stream
            result = client.analyze(
                image_data=image_stream.read(),
                visual_features=[VisualFeatures.READ]
            )

            # Write OCR results to Markdown file
            md_file.write(f"# Results for Page {page_num + 1}\n\n")
            
            if result.read is not None:
                md_file.write("## Extracted Paragraphs\n\n")
                for block in result.read.blocks:
                    paragraph_text = " ".join([line.text for line in block.lines])
                    md_file.write(f"{paragraph_text}\n\n")

            # Write image details and model version
            md_file.write("## Image Details\n\n")
            md_file.write(f"- **Image Height**: {result.metadata.height}\n")
            md_file.write(f"- **Image Width**: {result.metadata.width}\n\n")

            md_file.write("## Model Version\n\n")
            md_file.write(f"- **Model Version**: {result.model_version}")
            
        print(f"Results saved to '{markdown_file}'")

if __name__ == "__main__":
    sample_ocr_image_file() 