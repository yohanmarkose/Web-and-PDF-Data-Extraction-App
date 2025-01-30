import time
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
                                    ["Scrapy (OS)", "Diffbot (Enterprise)", "Docling"])
        text_url = st.text_input("Enter URL here")
        convert = st.button("Convert", use_container_width=True)
    elif input_format == "PDF":
        tool = st.sidebar.selectbox("Choose a method to convert PDF:", 
                                    ["PyMuPDF (OS)", "Azure Document Intelligence (Enterprise)", "Docling"])           
        if tool == "Azure Document Intelligence (Enterprise)":
            radio = st.radio("Choose a model :", ["Read", "Layout"])
        else:
            radio = None
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
    
        elif input_format == "PDF":
            if file_upload:
                st.success(f"File '{file_upload.name}' uploaded successfully!")
                convert_PDF_to_markdown(tool, file_upload,radio)
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
    progress_bar = st.progress(0)  
    progress_text = st.empty()  
    
    progress_text.text("Starting conversion...")
    time.sleep(0.5)
    progress_bar.progress(25)

    if tool == "Scrapy (OS)":
        response = requests.post(f"{API_URL}/scrape_url_os_scrapy", json={"url": text_url})
    elif tool == "Diffbot (Enterprise)":
        response = requests.post(f"{API_URL}/scrape_diffbot_en_url", json={"url": text_url})
    elif tool == "Docling":
        response = requests.post(f"{API_URL}/scrape-url-docling", json={"url": text_url})
    
    progress_text.text("Processing request...")
    progress_bar.progress(50)
    
    if response.status_code == 200:
        data = response.json()
        progress_text.text("Finalizing output...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        st.success("Conversion successful!")
        st.markdown(data["scraped_content"], unsafe_allow_html=True)
    else:
        st.error("An error occurred while processing.")
    
    progress_bar.progress(100)
    time.sleep(0.5)
    progress_bar.empty()
        
def convert_PDF_to_markdown(tool, file_upload, radio):    
    progress_bar = st.progress(0)
    progress_text = st.empty()
    
    progress_text.text("Uploading file...")
    time.sleep(0.5)
    progress_bar.progress(20)

    if file_upload is not None:
        bytes_data = file_upload.read()
        base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
        
        progress_text.text("Sending file for processing...")
        progress_bar.progress(50)
        
        if tool == "Open Source - PyMuPDF":
            response = requests.post(f"{API_URL}/scrape_pdf_os", json={"file": base64_pdf, "file_name": file_upload.name, "model": ""})
        elif tool == "Azure Document Intelligence (Enterprise)":
            model = "read" if radio == "Read" else "layout"
            response = requests.post(f"{API_URL}/azure-intdoc-process-pdf", json={"file": base64_pdf, "file_name": file_upload.name, "model": model})
        elif tool == "Docling":
            response = requests.post(f"{API_URL}/scrape_pdf_docling", json={"file": base64_pdf, "file_name": file_upload.name, "model": ""})
        
        progress_text.text("Processing document...")
        progress_bar.progress(75)
        
        if response.status_code == 200:
            data = response.json()
            progress_text.text("Finalizing output...")
            time.sleep(0.5)
            
            st.success("PDF conversion successful!")
            st.markdown(data["scraped_content"], unsafe_allow_html=True)
        else:
            st.error("An error occurred while processing the PDF.")
    
    progress_bar.progress(100)
    time.sleep(0.5)
    progress_bar.empty()        
    
if __name__ == "__main__":
# Set page configuration
    st.set_page_config(
        page_title="Document Parser",  # Name of the app
        layout="wide",              # Layout: "centered" or "wide"
        initial_sidebar_state="expanded"  # Sidebar: "expanded" or "collapsed"
    )    
    main()