import os
import json
from google.cloud import bigquery as bq
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'itr-aimasteryhub-lab-1a116262496d.json'
client = bq.Client(project="itr-aimasteryhub-lab")
 
print("Connected to BigQuery...")
datasets = list(client.list_datasets())
print(f"Found {len(datasets)} datasets:")
 
for dataset in datasets:
    print(f"- {dataset.dataset_id}")

# List tables in the conference_data dataset
dataset_id = "conference_data"
print(f"\nListing tables in {dataset_id}:")
tables = list(client.list_tables(dataset_id))
for table in tables:
    print(f"- {table.table_id}")
    
# Get schema of the sessions table
table_ref = client.dataset(dataset_id).table("sessions")
try:
    table = client.get_table(table_ref)
    print("\nSchema of sessions table:")
    for field in table.schema:
        print(f"- {field.name} ({field.field_type}, mode={field.mode})")
except Exception as e:
    print(f"Error getting table schema: {e}")

print("\nRunning the scraper...")
from scrapers.parsers.aicon_infoq import AiconInfoqScraper
from scrapers.parsers.qcon_infoq import QconInfoqScraper
from bigquery.client import BigQueryClient
from bigquery.upload import ConferenceUploader
import uuid
from datetime import datetime

# Now run the full scraper
print("\nRunning the full scraper...")
scraper = QconInfoqScraper(
    use_bigquery=True,
    bq_credentials='itr-aimasteryhub-lab-1a116262496d.json',
    bq_project_id="itr-aimasteryhub-lab"
)

scraper.run()