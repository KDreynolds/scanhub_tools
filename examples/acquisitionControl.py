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

    # Retrieve the connection string from an environment
    # variable named AZURE_STORAGE_CONNECTION_STRING
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    # queue name
    q_name_tasks = "acquisition-control-queue"
    q_name_results = "queue-"
    
    # connect to queue
    queue_client_tasks = QueueClient.from_connection_string(connect_str, q_name_tasks)
    queue_client_results = QueueClient.from_connection_string(connect_str, q_name_results)
    queue_client_results.create_queue()
    while(True):
        messages = queue_client_tasks.receive_messages()

        for message in messages:
            print("Dequeueing message: " + message.content)
            queue_client_tasks.delete_message(message.id, message.pop_receipt)
            
            message = u"Hello World"
            print("Adding message: " + message)
            queue_client_results.send_message(message)


        time.sleep(1)