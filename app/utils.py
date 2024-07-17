import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_file_to_blob(file, filename):
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
        
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        
        # Upload the file to Azure Blob Storage
        blob_client.upload_blob(file)
        
        print(f"File {filename} uploaded to Blob Storage.")
    except Exception as ex:
        print(f"Exception: {ex}")
        raise
