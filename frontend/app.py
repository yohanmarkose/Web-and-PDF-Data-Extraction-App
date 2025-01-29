import streamlit as st
import requests
import base64
from io import BytesIO

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
        if tool == "Enterprise - Azure Document Intelligence":
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
            #show_home_page()
        elif input_format == "PDF":
            if file_upload:
                st.success(f"File '{file_upload.name}' uploaded successfully!")
                convert_PDF_to_markdown(tool, file_upload, radio)
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
        response = requests.post(f"{API_URL}/scrape-url", json={"url": text_url})
        if response.status_code == 200:
            # Extract the response data
            data = response.json()
            st.success(data["message"])
            
            # Display the scraped content
            st.subheader("Scraped Content")
            st.text_area("Content", data["scraped_content"], height=300)  # Show the scraped text
        else:
            st.error("An error occurred while scraping the URL.")

        # st.write(tool, text_url)
    elif tool == "Enterprise - Diffbot":
        st.write(tool, text_url)
        response = requests.post(f"{API_URL}/diffbot-scrape-url", json={"url": text_url})
        data = response.json()
        if "scraped_content" in data:
            # Display the Markdown content
            st.markdown(data["scraped_content"], unsafe_allow_html=True)
        else:
            st.error("Failed to extract content")

    elif tool == "Docling":
        #do something
        st.write(tool, text_url)
        
def convert_PDF_to_markdown(tool, file_upload, radio):    
    if tool == "Open Source - PyMuPDF":
        #do something
        st.write(tool)
    elif tool == "Enterprise - Azure Document Intelligence":
        if radio == "Read":
            st.write("Read model selected")
            files = {"file": (file_upload.name, file_upload, "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/azure-intdoc-read-process-pdf", files=files)
                if response.status_code == 200:
                    st.success("PDF processed successfully")
                    data = response.json()
                    st.markdown(data["scraped_content"], unsafe_allow_html=True)
                else:
                    st.error("Failed to extract content")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
        # st.markdown(response.json()["scraped_content"], unsafe_allow_html=True)
        else:
            st.error("Failed to extract content")
                
    elif radio == "Layout":
            st.write("Layout model selected")
            #response = requests.post(f"{API_URL}/azure-int-doc-process-pdf", json={"file": file_upload, "model": "layout"})
            if response.status_code == 200:
                data = response.json()
                st.success(data["message"])
                st.subheader("Extracted Data:")
                markdown_content = data["extracted_data"]
                st.markdown(markdown_content, unsafe_allow_html=True)
    elif tool == "Docling":
        #do something
        st.write(tool)
    # Show file details
    st.write("File details:")
    st.write(f"Filename: {file_upload.name}")
    st.write(f"File type: {file_upload.type}")
    st.write(f"File size: {file_upload.size} bytes")
    
    # Optionally read the file content (binary)
    file_content = file_upload.read()
    st.info(f"File content loaded. Size: {len(file_content)} bytes.")
    
def show_home_page():
    st.header("Welcome to the Home Page")
    st.write("This is a basic Streamlit app. Use the sidebar to navigate between pages.")
    
    # Example of user interaction
    user_input = st.text_input("Enter your name:", "")
    if user_input:
        st.write(f"Hello, {user_input}!")

def show_about_page():
    st.header("About This App")
    st.write("This app demonstrates the basic features of Streamlit, including navigation, user input, and interactivity.")

def show_contact_page():
    st.header("Contact Us")
    st.write("If you have any questions, feel free to reach out!")

    # Example of a form
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Thank you for your message!")
            st.write("We'll get back to you soon.")

def process_url(url):
    response = requests.post(f"{API_URL}/process-url", json={"url": url})
    return response.json()

if __name__ == "__main__":
# Set page configuration
    st.set_page_config(
        page_title="Document Parser",  # Name of the app
        layout="wide",              # Layout: "centered" or "wide"
        initial_sidebar_state="expanded"  # Sidebar: "expanded" or "collapsed"
    )    
    main()
