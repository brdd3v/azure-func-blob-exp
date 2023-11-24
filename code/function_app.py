import azure.functions as func
import pandas as pd
import logging
import os
from azure.storage.blob import BlobServiceClient
from io import BytesIO, StringIO


app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob",
                  path="container-exp/{name}.csv",
                  connection="AzureWebJobsStorage") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}. Blob Size: {myblob.length} bytes.")
    
    logging.info("Read csv file")
    df = pd.read_csv(BytesIO(myblob.read()))

    logging.info("Create txt file")
    sio = StringIO()
    df.info(buf=sio)
    output_info = sio.getvalue()
    sio.close()

    conn_str = os.environ["APPSETTING_AzureWebJobsStorage"]
    output_blob = f"{myblob.name.split('/')[-1]}.txt"

    logging.info("Upload txt file to Azure Blob Storage")
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container="container-exp", blob=output_blob)
    blob_client.upload_blob(output_info, overwrite=True)
