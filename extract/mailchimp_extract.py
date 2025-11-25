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
base_path = "extract/data"
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

# print(f"Saved to: {filepath}")
logging.info("Environment Setup: calling api")

api_check = mailchimp.ping.get()
response = mailchimp.campaigns.list()

# create filename with extract time
filename = f"mailchimp_campaigns_{extract_time}.json"
filepath = os.path.join(base_path, filename)


if api_check == {"health_status": "Everything's Chimpy!"}:
    # log successful api call
    logging.info('Successful API call')

    with open(filepath, "w", encoding="utf-8") as f:
      json.dump(response, f, indent=4)

    logging.info(f"Saved to: {filepath}")

else:
    logging.error(f"Unsuccessful API call! Error {response.status_code}: {response.text}")
