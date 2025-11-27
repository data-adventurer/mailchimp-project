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

def load_mailchimp_client():
    try:
        # load environment variables from .env file
        load_dotenv()
        
        # retrieve Mailchimp API key and server prefix from environment variables
        api_key = os.getenv('MAILCHIMP_API_KEY')
        server_prefix = os.getenv('MAILCHIMP_SERVER_PREFIX')
        
        # check if the required environment variables are present
        if not api_key or not server_prefix:
            raise ValueError("MAILCHIMP_API_KEY or MAILCHIMP_SERVER_PREFIX is missing from environment variables")
        
        # initialize the Mailchimp client and set configuration
        mailchimp = Client()
        mailchimp.set_config({
            "api_key": api_key,
            "server": server_prefix
        })
        
        # log successful client configuration
        logging.info("Mailchimp client configured successfully with server prefix: %s", server_prefix)
        
        return mailchimp
    
    except ValueError as ve:
        logging.error("Failed to load Mailchimp credentials: %s", ve)
    except Exception as e:
        logging.error("An unexpected error occurred while loading Mailchimp client: %s", e)
