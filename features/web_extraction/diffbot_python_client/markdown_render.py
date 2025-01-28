def extract_for_markdownrender(data):
    extracted_data = []
    for obj in data.get("objects", []):
        title = obj.get("title", "No Title Found")
        page_url = obj.get("pageUrl", "No URL Found")
        type = obj.get("type", "No Type Found")
        text = obj.get("text", "No Text Found")
        images = obj.get("images", "No images Found")
        extracted_data.append({"title": title, "pageUrl": page_url, "type": type, "text": text, "images": images})
    return extracted_data

# Read and parse the input file
try:
    with open(input_file_path, "r", encoding="utf-8") as txt_file:
        # Use ast.literal_eval to parse Python-like dictionary
        data = ast.literal_eval(txt_file.read())
        
        # Extract title and pageUrl
        extracted_data = extract_for_markdownrender(data)
        
        # Generate Markdown content
        markdown_content = f"# Extracted Data\n\n"
        markdown_content += f"**Date:** {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p %Z')}\n\n"
        
        for item in extracted_data:
            markdown_content += f"## Title : \n{item['title']}\n"
            markdown_content += f"## Page URL\n[{item['pageUrl']}]({item['pageUrl']})\n"
            markdown_content += f"## Identified Page Type\n[{item['type']}]({item['type']})\n"
            markdown_content += f"## Text Extracts \n[{item['text']}]({item['text']})\n"
            if 'images' in item and isinstance(item['images'], list):
                for image in item['images']:
                    if 'url' in image:
                        image_url = image['url']
                        image_title = image['title'] if 'title' in image else "No Title Found"
                        markdown_content += f"## Images Extracts \n[{image_title}]({image_url})\n"
                    else:
                        markdown_content += f"## Images Extracts : \n No Images Found\n"