import fitz
from PIL import Image
import io
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def sample_ocr_image_file():
    # Set the values of your computer vision endpoint and computer vision key
    # how to obtain the endpoint and check .env file for key
    endpoint = os.getenv("VISION_ENDPOINT")
    key = os.getenv("VISION_KEY")


    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Load the PDF document
    pdf_path = "cesa-marketing team certi.pdf"
    pdf_document = fitz.open(pdf_path)
    total_pages = pdf_document.page_count
    print(f"Total pages in the PDF: {total_pages}")

    # Validate that the PDF has pages
    if total_pages == 0:
        print("The PDF is empty.")
        return

    # Limit to a maximum of 2 pages or total_pages, whichever is smaller
    max_pages_to_process = min(2, total_pages)

    markdown_file = "ocr_results.md"
    
    with open(markdown_file, "w", encoding="utf-8") as md_file:
        for page_num in range(max_pages_to_process):
            try:
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
                md_file.write(f"- **Model Version**: {result.model_version}\n\n")

            except Exception as e:
                print(f"Error processing page {page_num + 1}: {e}")

        print(f"Results saved to '{markdown_file}'")

if __name__ == "__main__":
    sample_ocr_image_file()