import streamlit as st

import requests

import base64

API_URL = "http://127.0.0.1:8000"

def main():
    # Set the title of the app
    st.title("Document to Markdown Conversion")

    # Add a sidebar
    st.sidebar.header("Main Menu")
    input_format = st.sidebar.selectbox("Choose a format:", ["WebURL", "PDF"])
    
    if input_format == "WebURL":
        tool = st.sidebar.selectbox("Choose a method to convert URL:", 
                                    ["Open Source - Scrapy", "Enterprise - Diffbot", "Docling"])
        text_url = st.text_input("Enter URL here")
        convert = st.button("Convert", use_container_width=True)
    elif input_format == "PDF":
        tool = st.sidebar.selectbox("Choose a method to convert PDF:", 
                                    ["Open Source - PyMuPDF", "Enterprise - Azure Document Intelligence", "Docling"])
        #st.sidebar.file_uploader("Choose a PDF File", type="pdf", accept_multiple_files=False, key="abc")
        file_upload = st.file_uploader("Choose a PDF File", type="pdf", accept_multiple_files=False)
        convert = st.button("Convert", use_container_width=True)
        
    # Define what happens on each page
    if convert:
        if input_format == "WebURL":
            if text_url:
                if check_url(text_url):
                    st.success(f"The URL '{text_url}' exists and is accessible!")
                    convert_web_to_markdown(tool, text_url)
                else:
                    st.error(f"The URL '{text_url}' does not exist or is not accessible.")
            else:
                st.info("Please enter a URL.")
            #show_home_page()
        elif input_format == "PDF":
            if file_upload:
                st.success(f"File '{file_upload.name}' uploaded successfully!")
                convert_PDF_to_markdown(tool, file_upload)
            else:
                st.info("Please upload a PDF file.")
            
    
def check_url(url):
    try:
        response = requests.head(url, timeout=5)  # Send HEAD request
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False

def convert_web_to_markdown(tool, text_url):    
    if tool == "Open Source - Scrapy":
        #do something
        # response = requests.post(f"{API_URL}/scrape-url", json={"url": text_url})
        # if response.status_code == 200:
        #     # Extract the response data
        #     data = response.json()
        #     st.success(data["message"])
            
        #     # Display the scraped content
        #     st.subheader("Scraped Content")
        #     st.text_area("Content", data["scraped_content"], height=300)  # Show the scraped text
        response = requests.post(f"{API_URL}/open-source-scrape-url/", json={"url": text_url})
        if response.status_code == 200:
            markdown_content = response.content.decode("utf-8")
            st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.error("An error occurred while scraping the URL.")

        # st.write(tool, text_url)
    elif tool == "Enterprise - Diffbot":
        #do something
        st.write(tool, text_url)
    elif tool == "Docling":
        response = requests.post(f"{API_URL}/docling-scrape-url/", json={"url": text_url})
        if response.status_code == 200:
            markdown_content = response.content.decode("utf-8")
            st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.error("An error occurred while scraping the URL.")
        
def convert_PDF_to_markdown(tool, file_upload):    
    """
    Converts a PDF file to markdown format using the specified tool.
    Parameters:
    tool (str): The tool to use for conversion. Options are "Open Source - PyMuPDF", 
                "Enterprise - Azure Document Intelligence", and "Docling".
    file_upload (UploadedFile): The uploaded PDF file to be converted.
    Returns:
    None: The function writes the converted markdown content to the Streamlit app or 
          displays an error message if the conversion fails.
    """
    if tool == "Open Source - PyMuPDF":
        #do something
        # response = requests.post(f"{API_URL}/scrape_pdf_os", json={"file": file_upload})
        if file_upload is not None:
        # Convert the file to base64
            bytes_data = file_upload.read()
            base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
            
            # Send to API
            response = requests.post(f"{API_URL}/scrape_pdf_os",
                json={"file": base64_pdf, "file_name": file_upload.name}
            )
            
        if response.status_code == 200:
            # Extract the response data
            data = response.json()
            st.success(data["message"])
            
            # Display the scraped content
            st.subheader("Scraped Content")
            # st.text_area("Content", data["scraped_content"], height=300)  # Show the scraped text
            markdown_content = data["scraped_content"]
            st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.error("An error occurred while scraping the URL.")
        # st.write(tool)
    elif tool == "Enterprise - Azure Document Intelligence":
        #do something
        st.write(tool)
    elif tool == "Docling":
        #do something
        st.write(tool)
        files = {"file": (file_upload.name, file_upload, "application/pdf")}
        try:
            response = requests.post(f"{API_URL}/pdf-docling-converter/", files=files)
            if response.status_code == 200:
                markdown_content = response.content.decode("utf-8")
                st.markdown(markdown_content, unsafe_allow_html=True)
                st.image("frontend/image_000008_5497e7a24d3d5d55b5d3be3f9425535d1b296c43603e2746c04e989b56544960.png")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
    # Show file details
    # st.write("File details:")
    # st.write(f"Filename: {file_upload.name}")
    # st.write(f"File type: {file_upload.type}")
    # st.write(f"File size: {file_upload.size} bytes")
    
    # Optionally read the file content (binary)
    file_content = file_upload.read()
    st.info(f"File content loaded. Size: {len(file_content)} bytes.")
    
if __name__ == "__main__":
# Set page configuration
    st.set_page_config(
        page_title="Document Parser",  # Name of the app
        layout="wide",              # Layout: "centered" or "wide"
        initial_sidebar_state="expanded"  # Sidebar: "expanded" or "collapsed"
    )    
    main()
