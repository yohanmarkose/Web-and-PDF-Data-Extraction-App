# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_layout.py

DESCRIPTION:
    This sample demonstrates how to extract text, tables, figures, selection marks and document structure (e.g., sections) information from a document
    given through a file.
    
PREREQUISITES:
    The following prerequisites are necessary to run the code. For more details, please visit the "How-to guides" link: https://aka.ms/how-to-guide

    -------Python and IDE------
    1) Install Python 3.7 or later (https://www.python.org/), which should include pip (https://pip.pypa.io/en/stable/).
    2) Install the latest version of Visual Studio Code (https://code.visualstudio.com/) or your preferred IDE. 
    
    ------Azure AI services or Document Intelligence resource------ 
    Create a single-service (https://aka.ms/single-service) or multi-service (https://aka.ms/multi-service) resource.
    You can use the free pricing tier (F0) to try the service and upgrade to a paid tier for production later.
    
    ------Get the key and endpoint------
    1) After your resource is deployed, select "Go to resource". 
    2) In the left navigation menu, select "Keys and Endpoint". 
    3) Copy one of the keys and the Endpoint for use in this sample. 
    
    ------Set your environment variables------
    At a command prompt, run the following commands, replacing <yourKey> and <yourEndpoint> with the values from your resource in the Azure portal.
    1) For Windows:
       setx DOCUMENTINTELLIGENCE_API_KEY <yourKey>
       setx DOCUMENTINTELLIGENCE_ENDPOINT <yourEndpoint>
       • You need to restart any running programs that read the environment variable.
    2) For macOS:
       export key=<yourKey>
       export endpoint=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-macOS
    3) For Linux:
       export DOCUMENTINTELLIGENCE_API_KEY=<yourKey>
       export DOCUMENTINTELLIGENCE_ENDPOINT=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-Linux
       
    ------Set up your programming environment------
    At a command prompt,run the following code to install the Azure AI Document Intelligence client library for Python with pip:
    pip install azure-ai-documentintelligence --pre
    
    ------Create your Python application------
    1) Create a new Python file called "sample_analyze_layout.py" in an editor or IDE.
    2) Open the "sample_analyze_layout.py" file and insert the provided code sample into your application.
    3) At a command prompt, use the following code to run the Python code: 
       python sample_analyze_layout.py
"""

import os


def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result


# To learn the detailed concept of "span" in the following codes, visit: https://aka.ms/spans 
def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False


def analyze_layout():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    import os

    # Set up Azure Document Intelligence Client
    # endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    # key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # Analyze a local document
    path_to_sample_document = "D:/BigData/DAMG7245_Assignment01/Prototypes/enterprise/azure-intelligent-document/sample-layout.pdf"
    with open(path_to_sample_document, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", 
            body=f, 
            content_type="application/octet-stream"
        )
    result = poller.result()

    # Prepare markdown content
    markdown_content = "# Document Layout Analysis Results\n\n"

    # Handwritten Content Check
    markdown_content += "## Handwritten Content:\n\n"
    if result.styles and any([style.is_handwritten for style in result.styles]):
        markdown_content += "Document contains handwritten content\n\n"
    else:
        markdown_content += "Document does not contain handwritten content\n\n"

    # Pages
    markdown_content += "## Pages\n\n"
    for page in result.pages:
        markdown_content += f"### Analyzing layout from page #{page.page_number}\n"
        markdown_content += f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}\n\n"

        # Collect words from lines
        page_words = []
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                # markdown_content += (
                #     f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                #     f"within bounding polygon '{line.polygon}'\n"
                # )

                # Analyze words
                for word in words:
                    # markdown_content += f"......Word '{word.content}' has a confidence of {word.confidence}\n"
                    page_words.append(word.content)  # Append word content to the list

        # Add collected words to markdown
        if page_words:
            markdown_content += "**Extracts from the page:**\n"
            markdown_content += " ".join(page_words) + "\n\n"  # Join words with spaces for readability
 
    # Tables
    markdown_content += "## Tables\n\n"
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            markdown_content += f"Table #{table_idx + 1}: {table.row_count} rows x {table.column_count} columns\n"
            for cell in table.cells:
                markdown_content += f"- Cell[{cell.row_index}, {cell.column_index}]: {cell.content}\n"
            markdown_content += "\n"
    else:
        markdown_content += "No tables found in the document.\n\n"

    # Figures
    markdown_content += "## Figures\n\n"
    if result.figures:
        for figure_idx, figure in enumerate(result.figures):
            markdown_content += f"Figure # {figure_idx + 1} has the following spans: {figure.spans}\n"
            markdown_content += f"Figure #{figure_idx + 1}: Found on page {figure.bounding_regions[0].page_number}\n"
            markdown_content += "\n"
            for region in figure.bounding_regions:
                markdown_content += f"Within bounding polygon '{region.polygon}'\n"
    else:
        markdown_content += "No figures found in the document.\n\n"
        
    # Save to Markdown File
    with open("layout_analysis_result_v2.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print("Results saved to layout_analysis_result_v2.md")

if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        analyze_layout()
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

# Next steps:
# Learn more about Layout model: https://aka.ms/di-layout
# Find more sample code: https://aka.ms/doc-intelligence-samples