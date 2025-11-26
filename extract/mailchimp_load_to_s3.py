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
    load_dotenv()

    dir_path = "extract/data/campaigns"
    folder_prefix = 'mailchimp-import/'

    aws_access_key = os.getenv('aws_access_key')
    aws_secret_key = os.getenv('aws_secret_access_key')
    aws_bucket = os.getenv('aws_bucket')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    # try:
    #     s3_client.head_bucket(Bucket=aws_bucket)
    #     logging.info(f"Access to S3 bucket '{aws_bucket}' confirmed")
    # except ClientError as e:
    #     logging.error(f"Failed to access S3 bucket '{aws_bucket}': {e}")
    #     raise e


    files_to_upload = [f for f in os.listdir(dir_path) if f.endswith(".json")]

    for file in files_to_upload:
        file_path = os.path.join(dir_path, file)
        s3_key = f"{folder_prefix}{file}"  # S3 key (path inside the bucket)

        # Check if file exists in S3
        try:
            s3_client.head_object(Bucket=aws_bucket, Key=s3_key)
            print(f"File already exists in S3, skipping upload: {file}")
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                # File does not exist, proceed with upload
                try:
                    s3_client.upload_file(file_path, aws_bucket, s3_key)
                    print(f"✓ Uploaded: {file}")

                    os.remove(file_path)
                    print(f"Deleted: {file}")
                except Exception as upload_error:
                    print(f"Error uploading {file}: {upload_error}")
            else:
                print(f"Error checking {file} in S3: {e}")
