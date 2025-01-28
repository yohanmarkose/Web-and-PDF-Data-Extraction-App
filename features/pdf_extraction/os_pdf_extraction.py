from PIL import Image
import io
import pymupdf


def extract_pdf_to_markdown(pdf_path, output_md_path):
    # Give output path as s3 bucket path
    
    doc = pymupdf.open(pdf_path)
    
    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text and headings
            text = page.get_text("dict")
            for block in text["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["size"] > 12:  # Assuming headings have larger font size
                                md_file.write(f"## {span['text']}\n\n")
                            else:
                                md_file.write(f"{span['text']}\n\n")
            
            # Extract images
            for img_index, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_path = f"images/page{page_num+1}_img{img_index}.{image_ext}"
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                md_file.write(f"![Image](/{image_path})\n\n")
            
            # Extract links
            links = page.get_links()
            for link in links:
                if "uri" in link:
                    md_file.write(f"[Link]({link['uri']})\n\n")
            
            # Extract tables
            tables = page.find_tables()
            try:
                for table in tables:
                    for row in table.extract():
                        md_file.write(" | ".join(row) + "\n")
                    md_file.write("\n")
            except Exception as e:
                print(f"Error processing Tables: {e}")