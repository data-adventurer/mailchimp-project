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

def save_campaigns(campaigns, base_path, extract_time):
    for campaign in campaigns:
        campaign_id = campaign["id"]
        filename = f"{campaign_id}_{extract_time}.json"
        filepath = os.path.join(base_path, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(campaign, f, indent=4)

        logging.info(f"Saved campaign {campaign_id} to: {filepath}")