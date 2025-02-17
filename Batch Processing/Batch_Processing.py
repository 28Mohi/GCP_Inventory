from asyncio.log import logger
import pandas as pd 
from google.cloud import storage,bigquery 
from google.oauth2 import service_account as sa 
import logging 
import io

#Logging Config
logging.basicConfig(level=logging.DEBUG)
log=logging.getLogger(__name__)

def Upload_CSV_to_GCS(bucket_name,source_file_path,Dest_file_path):
    try:
        #Credientials Validation 
        credentials=sa.Credentials.from_service_account_file(r"Replace With your Credentials")

        # Initializing Google Cloud Storage client
        print("Initializing Google Cloud Storage client...")
        Storage_client=storage.Client(credentials=credentials, project='Project_ID')
        print(f"Connected to project: {Storage_client.project}")

        #Accessing bucket
        print(f"Accessing bucket: {bucket_name}")
        Bucket_name=Storage_client.bucket(bucket_name)

        #
        print(f"Uploading file: {source_file_path} to {Dest_file_path}")
        blob= Bucket_name.blob(Dest_file_path)
        blob.upload_from_filename(source_file_path)

        csv_data = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(csv_data))
        return df
        print("The File Uploaded Sucessfully")
        log.info("File Upload Sucess")
    except Exception as e:
        
        log.error(e)

def upload_GCS_to_BQ(df,Dataset_id,table_name):
    try:
        credentials=sa.Credentials.from_service_account_file(r"Replace With your Credentials")
        bq_client=bigquery.Client(credentials=credentials,project='Project_ID')
        
        # Using strings for dataset and table references
        table_id = f"polar-casing-449010-e9.{Dataset_id}.{table_name}"
       
        # Set up job configuration

        schema=[
            bigquery.SchemaField("Item_ID","INTEGER"),
            bigquery.SchemaField("Item_Name","STRING"),
            bigquery.SchemaField("Supplier","STRING"),
            bigquery.SchemaField("Warehouse_Location","STRING"),
            bigquery.SchemaField("Stock_Quantity","STRING"),
            bigquery.SchemaField("Reorder_Level","STRING"),
            bigquery.SchemaField("Last_Updated","Date")
        ]
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,            
            schema=schema,     
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            skip_leading_rows=1,
            create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
        )
        
        # Upload data to BigQuery
        print(f"Uploading data from GCS to BigQuery table: {table_id}")
        load_job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        load_job.result()  # Wait for the job to complete

        print(f"Data uploaded to BigQuery table {table_id} successfully!")
        log.info(f"Data uploaded to BigQuery table {table_id} successfully!")

    except Exception as e:
        log.error(f"Error: {e}")
        print(e)
    except Exception  as e:
        print(e)


#Passing the value    
bucket_name="inventory_file_processing"
source_file_path=r"C:\Users\mohid\Downloads\inventory_data_1000.csv"
Dest_file_path="inventory file processing_folder/upload_1000.csv"
Dataset_id="Test"
table_name="Sample"

#Calling the Function
df=Upload_CSV_to_GCS(bucket_name,source_file_path,Dest_file_path)

upload_GCS_to_BQ(df,"Test","Sample")