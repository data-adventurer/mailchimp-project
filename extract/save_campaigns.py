import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from mailchimp_marketing import Client

# Set up extract time and logging (outside functions)
extract_time = datetime.now().strftime('%Y-%m-%d %H-%M')
extract_stamp = datetime.now().strftime('%Y-%m-%d')

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

def save_campaigns(campaigns, base_path, extract_stamp):
    for campaign in campaigns:
        try:
            # extract campaign ID to form filename
            campaign_id = campaign["id"]
            filename = f"{campaign_id}_{extract_stamp}.json"
            filepath = os.path.join(base_path, filename)
            
            # write campaign data to JSON file with UTF-8 encoding
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(campaign, f, indent=4)
            
            # log successful save with file path info
            logging.info("Saved campaign %s to: %s", campaign_id, filepath)
        
        except KeyError:
            # log missing 'id' in campaign dictionary
            logging.error("Campaign missing 'id' key. Campaign data skipped: %s", campaign)
        except IOError as io_err:
            # log file writing issues like permission or disk space errors
            logging.error("IO error saving campaign %s to file: %s", campaign.get("id", "unknown"), io_err)
        except Exception as e:
            # log any other unexpected error during save process
            logging.error("Unexpected error saving campaign %s: %s", campaign.get("id", "unknown"), e)