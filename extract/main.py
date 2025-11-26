from load_mailchimp_client import load_mailchimp_client
from fetch_all_campaigns import fetch_all_campaigns
from save_campaigns import save_campaigns
from mailchimp_load_to_s3 import upload_json_files_to_s3
import logging
import os
from datetime import datetime, timedelta

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

if __name__ == '__main__':
    mailchimp = load_mailchimp_client()
    
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S+00:00')

    logging.info("Mailchimp API extraction started")
    api_check = mailchimp.ping.get()
    if api_check != {"health_status": "Everything's Chimpy!"}:
        logging.error("Mailchimp API health check failed.")
        exit(1)

    campaigns = fetch_all_campaigns(mailchimp, start_date, end_date)
    logging.info(f"Fetched {len(campaigns)} campaigns")
    
    save_campaigns(campaigns, base_path, extract_time)
    logging.info("Campaign data extraction finished successfully")

    upload_json_files_to_s3(base_path)  # Call upload function here
    logging.info("Upload to S3 completed successfully")