import boto3


class S3FileManager:
    def __init__(self, bucket_name, base_path=''):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.base_path = base_path.strip('/')
    
    def list_files(self, prefix=''):
        full_prefix = f'{self.base_path}/{prefix}'.strip('/')
        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=full_prefix
        )
        return [obj['Key'] for obj in response.get('Contents', [])]
    
    def upload_file(self, file_path, object_name=None):
        if not object_name:
            object_name = os.path.basename(file_path)
        full_path = f'{self.base_path}/{object_name}'.strip('/')
        return upload_with_retry(file_path, self.bucket_name, full_path)
    
    def get_presigned_url(self, object_name, expiration=3600):
        full_path = f'{self.base_path}/{object_name}'.strip('/')
        return generate_presigned_url(self.bucket_name, full_path, expiration)
    
# Usage


# Initialize file manager
file_manager = S3FileManager('your-bucket-name', 'path/to/files')

# List files
files = file_manager.list_files()
print('Files in bucket:', files)

# Upload a file
file_manager.upload_file('local_file.txt', 'remote_file.txt')

# Generate presigned URL
url = file_manager.get_presigned_url('remote_file.txt')
print('Presigned URL:', url)