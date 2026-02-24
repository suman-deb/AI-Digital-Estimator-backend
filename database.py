
import os
from azure.cosmos import CosmosClient

def get_container(container_name):
    client = CosmosClient.from_connection_string(
        os.environ["COSMOS_CONNECTION"]
    )
    database = client.get_database_client("DigitalEstimatorDB")
    return database.get_container_client(container_name)

import uuid
from datetime import datetime

def save_estimate(data):
    container = get_container("estimates")

    data["id"] = str(uuid.uuid4())
    data["type"] = "estimate"
    data["timestamp"] = datetime.utcnow().isoformat()

    container.upsert_item(data)

    return data
