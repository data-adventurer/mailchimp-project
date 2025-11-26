import os
import logging
import requests
import json
from dotenv import load_dotenv
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from datetime import datetime, timedelta

# format the extract date
extract_time = datetime.now().strftime('%Y-%m-%d %H-%M')

# configure base directory and path
base_path = "extract/data/campaigns"
os.makedirs(base_path, exist_ok=True)

# configure logging
log_dir = "extract/logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, f"mailchimp_extract_{extract_time}.log"),
    filemode='a',  
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO  
)

# connect to .env file to get api key and server prefix
load_dotenv() 

api_key = os.getenv('MAILCHIMP_API_KEY')
server_prefix = os.getenv('MAILCHIMP_SERVER_PREFIX')

mailchimp = Client()
mailchimp.set_config({
  "api_key": api_key,
  "server": server_prefix
})

from datetime import datetime

# Example: set date range (ISO 8601, UTC)
start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S+00:00')

logging.info("Environment Setup: calling api")

api_check = mailchimp.ping.get()

offset = 0
count = 1000  # max campaigns per call
all_campaigns = []

while True:
    response = mailchimp.campaigns.list(
        since_create_time=start_date,
        before_create_time=end_date,  # Fixed: use before_create_time to match start param
        count=count,
        offset=offset
    )

    campaigns = response.get("campaigns", [])
    all_campaigns.extend(campaigns)

    if len(campaigns) < count:
        # fewer campaigns mean this is the last page
        break

    offset += count

# build a list of campaign ids from the response
campaigns = response.get("campaigns", [])
campaign_ids = [c["id"] for c in campaigns]

if api_check == {"health_status": "Everything's Chimpy!"}:
    logging.info("Successful API call")

    # save each campaign separately with file name: ampaign_id>_<extract_time>.json
    for campaign in campaigns:
        campaign_id = campaign["id"]
        campaign_filename = f"{campaign_id}_{extract_time}.json"
        campaign_filepath = os.path.join(base_path, campaign_filename)
        with open(campaign_filepath, "w", encoding="utf-8") as f:
            json.dump(campaign, f, indent=4)
        logging.info(f"Saved campaign {campaign_id} to: {campaign_filepath}")

    logging.info(f"All campaign IDs: {campaign_ids}")

else:
    logging.error(f"Unsuccessful API call! Error: {api_check}")

