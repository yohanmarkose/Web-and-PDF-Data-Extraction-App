import boto3
import json
from datetime import datetime, timedelta
import boto3.s3.transfer as transfer
import os

# AWS S3 Configurations
AWS_ACCESS_KEY_ID = "AKIAYKFQQUN54HLOMPMN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = "pdfparserdataset"

# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )

# def upload_to_s3(file_name, content):
#     s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=content)


class S3FileManager:
    def __init__(self, bucket_name, base_path=''):
        self.s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, 
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,)
        self.bucket_name = bucket_name
        self.base_path = base_path.strip('/')
    
    def list_files(self, prefix=''):
        full_prefix = f'{self.base_path}/{prefix}'.strip('/')
        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=full_prefix
        )
        return [obj['Key'] for obj in response.get('Contents', [])]
    
    def upload_file(self, bucket_name, file_name, content):
        # if not object_name:
        #     object_name = os.path.basename(file_path)
        # full_path = f'{self.base_path}/{object_name}'.strip('/')
        # return self.upload_with_retry(file_path, self.bucket_name, full_path)
        self.s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)
    
    def get_presigned_url(self, object_name, expiration=3600):
        full_path = f'{self.base_path}/{object_name}'.strip('/')
        return self.generate_presigned_url(self.bucket_name, full_path, expiration)
    
    def generate_presigned_url(self, bucket_name, object_name, expiration=3600):
        try:
            url = self.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            print(f'Presigned URL: {url}')
            return url
        except Exception as e:
            print(f'Error generating presigned URL: {str(e)}')
            return None
    
    def upload_with_retry(self, file_path, bucket_name, object_name=None, max_attempts=3):
        config = transfer.TransferConfig(
            multipart_threshold=1024 * 25,  # 25MB
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True
        )
        
        for attempt in range(max_attempts):
            try:
                self.s3.upload_file(
                    file_path,
                    bucket_name,
                    object_name or file_path,
                    Config=config
                )
                print(f'File uploaded successfully on attempt {attempt + 1}')
                return True
            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'Final attempt failed: {str(e)}')
                    return False
                print(f'Attempt {attempt + 1} failed, retrying...')
    
# # Usage


# # Initialize file manager
# file_manager = S3FileManager('your-bucket-name', 'path/to/files')

# # List files
# files = file_manager.list_files()
# print('Files in bucket:', files)

# # Upload a file
# file_manager.upload_file('local_file.txt', 'remote_file.txt')

# # Generate presigned URL
# url = file_manager.get_presigned_url('remote_file.txt')
# print('Presigned URL:', url)