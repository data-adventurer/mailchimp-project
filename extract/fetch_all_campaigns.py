import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
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

def fetch_all_campaigns(mailchimp, start_date, end_date):
    offset = 0
    count = 1000
    all_campaigns = []

    while True:
        response = mailchimp.campaigns.list(
            since_create_time=start_date,
            before_create_time=end_date,
            count=count,
            offset=offset
        )
        campaigns = response.get("campaigns", [])
        all_campaigns.extend(campaigns)
        if len(campaigns) < count:
            break
        offset += count

    return all_campaigns