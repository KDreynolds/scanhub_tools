#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# @authors   Christoph Dinh <christoph.dinh@brain-link.de>
# @authors   Johannes Behrens <johannes.behrens@brain-link.de>
# @version   1.0
# @date      May, 2022
# @copyright Copyright (c) 2022, BRAIN-LINK UG and authors of ScanHub Tools. All rights reserved.
# @license   BSD 3-Clause License
# @brief     Acquisitioncontrol
# ---------------------------------------------------------------------------


from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

import time, os


if __name__ == '__main__':
    print("AcquisitionControl started")

    # DEBUG
    os.environ['STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'

    # Retrieve the connection string from an environment
    # variable named AZURE_STORAGE_CONNECTION_STRING
    connect_str = os.getenv("STORAGE_CONNECTION_STRING")

    # queue name
    q_name_tasks = "acquisition-control-queue"
    q_name_results = "acquistion-control-results-queue"
    
    # connect to queue
    queue_client_tasks = QueueClient.from_connection_string(connect_str, q_name_tasks,
                            message_encode_policy = BinaryBase64EncodePolicy(),
                            message_decode_policy = BinaryBase64DecodePolicy())
    queue_client_results = QueueClient.from_connection_string(connect_str, q_name_results,
                            message_encode_policy = BinaryBase64EncodePolicy(),
                            message_decode_policy = BinaryBase64DecodePolicy())
    # queue_client_results.create_queue()
    while(True):
        messages = queue_client_tasks.receive_messages()

        for message in messages:
            print(message)
            print("Dequeueing message: " + message.content.decode('UTF-8'))
            queue_client_tasks.delete_message(message.id, message.pop_receipt)
            
            print("Adding message: " + message.content.decode('UTF-8'))
            queue_client_results.send_message(message.content)

        time.sleep(1)