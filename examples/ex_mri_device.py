#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# @authors   Christoph Dinh <christoph.dinh@brain-link.de>
# @version   1.0
# @date      April, 2022
# @copyright Copyright (c) 2022, BRAIN-LINK UG and authors of ScanHub Tools. All rights reserved.
# @license   BSD 3-Clause License
# @brief     Example MRI device
# ---------------------------------------------------------------------------

# https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows
# https://github.com/Azure-Samples/automated-testing-with-azurite

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
import os
import requests
import uuid

import numpy as np


def list_files() -> []:
    file_list = []
    
    for root, dirs, files in os.walk("data"):
        for name in files:
            file_list.append({"file_name": name, "local_path": os.path.join(root,name)})

    return file_list

def get_filename_from_url(url: str) -> str:
    file_name=url.split('/')[-1]
    return file_name

def get_random_images() -> []:
    # helper function uses loremflickr.com to get a random list of images 
    images = []

    for i in range(10):
        resp = requests.get(url=f"https://loremflickr.com/json/320/240?random={i}")
        resp_json = resp.json()
        images.append(resp_json["file"])

    return images

def create_blob_from_url(storage_connection_string,container_name):
    try:
        # urls to fetch into blob storage
        url_list = get_random_images()

        # Instantiate a new BlobServiceClient and a new ContainerClient
        # blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        # container_client = blob_service_client.get_container_client(container_name)
        container_client = ContainerClient.from_connection_string(storage_connection_string, container_name)

        if not container_client.exists():
            container_client.create_container()
        
        for u in url_list:
            # Download file from url then upload blob file
            r = requests.get(u, stream = True)
            if r.status_code == 200:
                r.raw.decode_content = True
                blob_client = container_client.get_blob_client(get_filename_from_url(u))
                blob_client.upload_blob(r.raw,overwrite=True)
        return True
        
    except Exception as e:
        print(e.message, e.args)
        return False

def create_blob_from_path(storage_connection_string,container_name):
    try:
        # Instantiate a new BlobServiceClient and a new ContainerClient
        # blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        # container_client = blob_service_client.get_container_client(container_name)
        container_client = ContainerClient.from_connection_string(storage_connection_string, container_name)
        
        if not container_client.exists():
            container_client.create_container()
        
        for f in list_files():
            with open(f["local_path"], "rb") as data:
                blob_client = container_client.get_blob_client(f["file_name"])
                blob_client.upload_blob(data,overwrite=True)
        return True

    except Exception as e:
        print(e.message, e.args)
        return False

if __name__ == '__main__':

    print("K-Space")
    kspacedata = np.load('data/kspace.npy')
    print(kspacedata.shape)
    print(kspacedata[0][0])

    # DEBUG
    os.environ['STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'
    os.environ['STORAGE_CONTAINER'] = 'raw-mri' #str(uuid.uuid4()) #'scanhub-container'

    # get storage account settings
    storage_connection_string = os.environ.get("STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("STORAGE_CONTAINER")

    # # if you want to copy from a public url
    # result = create_blob_from_url(storage_connection_string,container_name)
    
    # OR if you want to upload form your local drive
    result = create_blob_from_path(storage_connection_string,container_name)

    if(result):
        print("Done!")
    else:
        print("An error occured!")