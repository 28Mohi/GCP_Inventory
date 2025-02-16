from asyncio.log import logger
import pandas as pd 
from google.cloud import storage,bigquery 
from google.oauth2 import service_account as sa 
import logging 

#Logging Config
logging.basicConfig(level=logging.DEBUG)
log=logging.getLogger(__name__)

def Upload_CSV_to_GCS(bucket_name,source_file_path,Dest_file_path):
    try:
        #Credientials Validation 
        credentials=sa.Credentials.from_service_account_file(r"C:\Users\mohid\Downloads\polar-casing-*******-e9-1d64e08c2acf.json")

        # Initializing Google Cloud Storage client
        print("Initializing Google Cloud Storage client...")
        Storage_client=storage.Client(credentials=credentials, project='polar-casing-449010-e9')
        print(f"Connected to project: {Storage_client.project}")

        #Accessing bucket
        print(f"Accessing bucket: {bucket_name}")
        Bucket_name=Storage_client.bucket(bucket_name)

        #
        print(f"Uploading file: {source_file_path} to {Dest_file_path}")
        blob= Bucket_name.blob(Dest_file_path)
        blob.upload_from_filename(source_file_path)

        print("The File Uploaded Sucessfully")
        log.info("File Upload Sucess")
    except Exception as e:
        
        log.error(e)

#Passing the value    
bucket_name="inventory_file_processing"
source_file_path=r"C:\Users\mohid\Downloads\inventory_data_1000.csv"
Dest_file_path="inventory file processing_folder/upload_1000.csv"

#Calling the Function
Upload_CSV_to_GCS(bucket_name,source_file_path,Dest_file_path)

