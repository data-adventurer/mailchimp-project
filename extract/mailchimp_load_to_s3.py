import os
import boto3
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from mailchimp_marketing import Client

# Set up extract time and logging (outside functions)
extract_time = datetime.now().strftime('%Y-%m-%d %H-%M')

log_dir = "extract/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, f"mailchimp_extract_{extract_time}.log"),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

base_path = "extract/data/campaigns"
os.makedirs(base_path, exist_ok=True)

def upload_json_files_to_s3(dir_path: str) -> None:
    # load AWS credentials and configuration from .env file
    load_dotenv()
    
    # directory containing JSON files to upload
    dir_path = "extract/data/campaigns"
    folder_prefix = 'mailchimp-import/'
    
    # retrieve AWS credentials and bucket name from environment variables
    aws_access_key = os.getenv('aws_access_key')
    aws_secret_key = os.getenv('aws_secret_access_key')
    aws_bucket = os.getenv('aws_bucket')
    
    # initialize Boto3 S3 client with credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    # list all JSON files in given directory
    files_to_upload = [f for f in os.listdir(dir_path) if f.endswith(".json")]
    
    for file in files_to_upload:
        file_path = os.path.join(dir_path, file)
        s3_key = f"{folder_prefix}{file}"  # Object key in S3 bucket
        
        try:
            # check if file already exists in S3 bucket
            s3_client.head_object(Bucket=aws_bucket, Key=s3_key)
            logging.info("File already exists in S3, skipping upload: %s", file)
        
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                # file does not exist; proceed with upload
                try:
                    s3_client.upload_file(file_path, aws_bucket, s3_key)
                    logging.info("Uploaded file: %s to S3 bucket: %s", file, aws_bucket)
                    
                    # delete local file after successful upload
                    os.remove(file_path)
                    logging.info("Deleted local file: %s", file)
                
                except Exception as upload_error:
                    logging.error("Error uploading file %s to S3: %s", file, upload_error)
            else:
                logging.error("Error checking file %s existence in S3: %s", file, e)
        except Exception as general_error:
            logging.error("Unexpected error processing file %s: %s", file, general_error)
