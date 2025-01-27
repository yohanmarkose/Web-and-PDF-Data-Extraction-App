import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
import os

load_dotenv()
# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

def list_objects_in_bucket():
    """List all objects in the S3 bucket."""
    try:
        # Create an S3 client with explicit credentials
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" in response:
            print(f"Objects in bucket '{BUCKET_NAME}':")
            for obj in response["Contents"]:
                print(f"- {obj['Key']}")
        else:
            print(f"No objects found in bucket '{BUCKET_NAME}'.")
    except ClientError as e:
        print(f"Error: {e}")
    except NoCredentialsError:
        print("AWS credentials not available.")

def put_file_to_bucket(file_path, bucket_name, object_name=None):
    """Put a file into S3 bucket."""
    try:
        # Create an S3 client with explicit credentials
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_path
        
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except ClientError as e:
        print(f"Error: {e}")
    except NoCredentialsError:
        print("AWS credentials not available.")

def delete_from_bucket(object_name, bucket_name):
    """Delete an object from an S3 bucket."""
    try:
        # Create an S3 client with explicit credentials
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # Delete the object
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"Object '{object_name}' deleted from bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error: {e}")
    except NoCredentialsError:
        print("AWS credentials not available.")        

def get_object_from_bucket(bucket_name, object_name, download_path):
    """Get an object from an S3 bucket and save it locally."""
    try:
        # Create an S3 client with explicit credentials
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # Download the object
        s3_client.download_file(bucket_name, object_name, download_path)
        print(f"Object '{object_name}' downloaded from bucket '{bucket_name}' to '{download_path}'.")
    except ClientError as e:
        print(f"Error: {e}")
    except NoCredentialsError:
        print("AWS credentials not available.")

if __name__ == "__main__":
    list_objects_in_bucket()
    #put_file_to_bucket("INSTALL.md", BUCKET_NAME)
    delete_from_bucket("INSTALL.md", BUCKET_NAME)
    #get_object_from_bucket(BUCKET_NAME, "path/to/object/in/bucket", "path/to/download/location")