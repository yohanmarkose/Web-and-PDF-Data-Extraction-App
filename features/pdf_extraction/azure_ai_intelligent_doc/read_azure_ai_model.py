import os
from fastapi import UploadFile
from azure.core.exceptions import HttpResponseError
from dotenv import find_dotenv, load_dotenv

load_dotenv()

def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def analyze_read(input_pdf_path):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # how to obtain the endpoint and check .azure-env file for key
    # endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    # key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    endpoint = "https://azuredocumentcheck.cognitiveservices.azure.com/"
    key = "CVkcoUUmNSmtKX4A2UKMhoFF7MBLPPRBo4BHqZvuHXA2vMKNix1eJQQJ99BAACYeBjFXJ3w3AAALACOGLdf2"

    if not endpoint or not key:
        raise EnvironmentError("Azure environment variables are not set.")
        print(f"Endpoint: {endpoint}, Key: {key}")

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(input_pdf_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",
            body=f,
            features=[DocumentAnalysisFeature.LANGUAGES],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()

    markdown_content = "## Document Extracted Content\n"
    if result.languages is not None:
        for language in result.languages:
            markdown_content += (f"### Language code: \n'{language.locale}' with confidence {language.confidence}")
    
    # Text content
    markdown_content = "### Text Content:\n\n"
    if result.paragraphs is not None:
        for paragraph in result.paragraphs:
            markdown_content += f"{paragraph.content}\n\n"
    else:
        markdown_content += "No paragraphs found.\n\n"

    # Pages Details
    markdown_content = "### Pages:\n\n"
    for page in result.pages:
        markdown_content = f"**Page number**: {page.page_number}\n**Width**: {page.width}\n**Height**: {page.height}\n**Unit**: {page.unit}\n\n"

    return markdown_content

def read_azure_ai_model(input_pdf_path):
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv
    try:
        load_dotenv(find_dotenv())
        print(f"input_pdf_path: {input_pdf_path}")
        analyze_read(input_pdf_path)
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise