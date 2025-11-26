The Mailchimp API is a set of programming tools that allows developers to interact with Mailchimp’s platform directly. 
It utilises RESTful principles, enabling applications to access and manage data, such as audience lists, email campaigns, and automations, programmatically. 
With the API, it’s possible to add or update subscribers, create and send email campaigns, automate workflows, and retrieve performance data, all without using Mailchimp’s web interface.
For this project, the Mailchimp API was called specifically to extract data about email campaigns.

### Introduction
The first step was to choose the core tools and prepare the environments. A Python script was selected to call the Mailchimp API, extract the data, and load it into an Amazon S3 bucket as the raw landing zone. 
This setup required creating a GitHub repository for version control and an S3 bucket configured with the appropriate keys and policies to ensure data security. 
Because the GitHub repository folder structure would be created using the dbt project, this was set up next. The dbt project was created and connected to both the GitHub repository and the Snowflake database, allowing changes to be tracked and deployed in a structured way.

The S3 bucket was then configured to connect to a Snowflake database, enabling the data to be moved into cloud storage and queried efficiently. 
This stage of the setup involved creating storage integration, a pipeline, and a stage in Snowflake to handle the incoming files. 
The database was linked to the dbt project to handle transformation and modelling.

### The Data 

This JSON represents detailed information about a Mailchimp email campaign. It includes metadata, campaign settings, delivery and performance statistics, and API endpoint links.

Main data types and meaning:
_links: A list of API endpoints related to this campaign (GET, POST, DELETE actions). Helps discover how to interact programmatically with the campaign.

Basic info: Fields like id, archive_url, content_type, create_time, status, and type describe the campaign identity, status, creation timestamp, and type (e.g., regular).

Delivery status: The delivery_status object holds booleans and counts showing the sending status such as emails sent, canceled, and whether cancellation is allowed.

Recipient info: recipients details the audience list this campaign was sent to including ID, name, and recipient count.

Performance summary: report_summary provides numeric metrics like open rate, click rate, number of opens, and clicks, which are typical marketing KPIs.

Send & scheduling: send_time marks when the campaign was scheduled or sent.

Settings: The settings object holds customized campaign options such as subject line, from name, reply-to address, footer usage, and preview text.

Tracking: The tracking object flags which types of tracking (opens, clicks, ecommerce) are enabled.

Other flags: Various booleans like resendable, needs_block_refresh indicate capabilities or refresh needs.

In essence, this JSON encapsulates a full snapshot of campaign configuration, delivery, audience, and performance data, intended for both API communication and reporting.

### Extract & Load

#### Python environment

1. Virtual environment
A virtual environment isolates your Python project’s dependencies from other projects and system-wide packages.

Creating a Virtual Environment
Open your terminal or command prompt.
Navigate to your project directory or create a new one:
```text
mkdir myproject
cd myproject
```
Create a virtual environment named env (you can name it anything):
```text
python -m venv env
```

Activating the Virtual Environment
On macOS/Linux:

``text
source env/bin/activate
```

On Windows:
```text
env\Scripts\activate
```

Once activated, your command prompt will prefix with the environment name, e.g., (env).

Deactivating the Virtual Environment
When done, deactivate it by running:

```text
deactivate
```

This setup allows you to safely install project-specific packages without affecting your global Python installation.

2. Requirements
This project requires the following Python version and packages to be installed

```Python
python==3.12
boto3==1.41.3
mailchimp-marketing==3.0.80
python-dotenv==1.2.1
```
Make sure you have Python 3.12 installed before installing the packages above. You can install the dependencies using a package manager like pip by running:

```Python
pip install -r requirements.txt
```

#### Main Script
This script extracts Mailchimp campaign data from the last 90 days, saves it locally, and uploads it to AWS S3.

load_mailchimp_client: Initializes the Mailchimp API client.

fetch_all_campaigns: Retrieves all campaigns between specified start and end dates.

save_campaigns: Saves the fetched campaign data as JSON files locally.

upload_json_files_to_s3: Uploads the saved JSON files to an S3 bucket.

The script also sets up logging to track progress and errors. 
It performs a health check on the Mailchimp API before fetching data to ensure connectivity. 
Use this script to automate Mailchimp campaign data extraction and storage efficiently.

```Python
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
```

### Storage integration


### Transform


### Orchestration





