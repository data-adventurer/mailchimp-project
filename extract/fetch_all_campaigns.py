import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from mailchimp_marketing import Client
from load_mailchimp_client import load_mailchimp_client
from mailchimp_marketing.api_client import ApiClientError

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

    try:
        while True:
            # call Mailchimp API to list campaigns by creation date, paginating results
            response = mailchimp.campaigns.list(
                since_create_time=start_date,
                before_create_time=end_date,
                count=count,
                offset=offset
            )
            
            # extract campaigns from response or empty list if key not found
            campaigns = response.get("campaigns", [])
            all_campaigns.extend(campaigns)
            
            # log successful fetch of current page of campaigns
            days_fetched = (end_date - start_date).days
            logging.info(
                "Fetched %d campaigns (offset %d). Total campaigns collected: %d from the last %d days",
                len(campaigns), offset, len(all_campaigns), days_fetched
            )
            
            # ff fewer campaigns than count returned, no more pages remain
            if len(campaigns) < count:
                break
            
            # increment offset to fetch next page
            offset += count

    except ApiClientError as api_err:
        # log errors specific to Mailchimp API client (API errors, invalid request, etc.)
        logging.error("Mailchimp API client error while fetching campaigns: %s", api_err.text)
    except Exception as e:
        # catch all other exceptions (network issues, etc.) and log them
        logging.error("Unexpected error during fetch_all_campaigns: %s", e)

    # return accumulated list of all fetched campaigns (empty if error occurred)
    return all_campaigns