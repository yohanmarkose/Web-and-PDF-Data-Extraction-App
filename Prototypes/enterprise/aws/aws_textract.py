import boto3

def extract_text_from_local_pdf(file_path):
    """
    Extract text from a local PDF file using Amazon Textract's synchronous API.
    Note: This works only for single-page PDFs.
    """
    # Initialize the Textract client

    textract = boto3.client('textract', region_name='us-east-1') 

    # Read the PDF file as binary
    with open(file_path, 'rb') as document:
        document_bytes = document.read()

    # Call Textract's detect_document_text API
    response = textract.detect_document_text(Document={'Bytes': document_bytes})

    # Extract and print text from the response
    extracted_text = ""
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            extracted_text += block['Text'] + "\n"

    return extracted_text


def extract_tables_from_pdf(file_path):
    """
    Extract tables from a PDF using Amazon Textract.
    Works only for single-page PDFs in synchronous mode.
    """
    textract = boto3.client('textract', region_name='us-east-1')

    # Read the PDF file
    with open(file_path, 'rb') as document:
        document_bytes = document.read()

    # Call Textract API
    response = textract.detect_document_text(Document={'Bytes': document_bytes})

    # Extract tables
    tables = []
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'TABLE':
            table_cells = [
                {
                    "row": cell["RowIndex"],
                    "col": cell["ColumnIndex"],
                    "text": cell.get("Text", "")
                }
                for cell in response["Blocks"] if cell["BlockType"] == "CELL"
            ]
            tables.append(table_cells)

    return tables if tables else "No tables found in document."

# Replace with the path to your local PDF file
file_path = "sample-layout.pdf"

try:
    text = extract_text_from_local_pdf(file_path)
    tables = extract_tables_from_pdf(file_path)
    print("Extracted Text:\n", text)
    print("Extracted Text:\n", text)
    with open("document_analysis_result.md", "w") as file:
        file.write(text)
except Exception as e:
    print("Error:", str(e))