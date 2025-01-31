from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.gcp.compute import Run
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.programming.framework import FastAPI
from diagrams.digitalocean.compute import Docker

# Create the diagram
with Diagram("Websites & PDF Extractor Application Architecture", show=False, filename="data_extractor", direction="LR"):
    # User interaction
    user = User("User")
    
    # Input Mechanism Cluster
    with Cluster("User Input"):
        url_input = Custom("Web URL Input", "./src/website.png")  # Replace with an appropriate local or online icon for URL input
        pdf_input = Custom("PDF File Upload", "./src/pdf.png")  # Replace with an appropriate local or online icon for PDF upload
    
    # Streamlit Frontend Cluster (Generic Node)
    with Cluster("Frontend (Streamlit)"):
        frontend = Custom("Streamlit UI", "./src/streamlit.png")  # Use a custom icon for Streamlit
    
    # Backend Cluster
    with Cluster("Backend (FastAPI)"):
        # Docker Image for Backend Services
        docker_image = Docker("Docker Image") 
        backend = FastAPI("FastAPI Service")
        processing_tools = [
            Custom("Open Source Tool", "./src/open-source.png"),
            Custom("Enterprise Tool", "./src/enterprise.png"),
            Custom("Docling Tool", "./src/docling.png")
        ]
    

    # Cloud Services
    cloud_run = Run("Google Cloud Run")
    s3_storage = S3("Amazon S3")
    
    # Connections
    user >> [url_input, pdf_input] >> frontend  # User provides input via URL or PDF upload to Streamlit UI
    frontend >> backend  # Streamlit communicates with Google Cloud Run backend
    cloud_run >> docker_image >> backend  # Google Cloud Run runs the Docker image containing backend services
    backend >> processing_tools  # Backend uses selected processing tools
    processing_tools >> s3_storage  # Processed data is saved to Amazon S3
    # s3_storage >> backend  # Processed data is displayed to the user via Streamlit UI
    backend >> frontend  # Backend sends messages to the frontend for user feedback