import os
import uuid
from datetime import datetime

def get_container(container_name):
    try:
        from azure.cosmos import CosmosClient
        
        connection_string = os.environ.get("COSMOS_CONNECTION")
        if not connection_string:
            print("Warning: COSMOS_CONNECTION not set, using mock storage")
            return None
            
        client = CosmosClient.from_connection_string(connection_string)
        database = client.get_database_client("DigitalEstimatorDB")
        return database.get_container_client(container_name)
    except Exception as e:
        print(f"Cosmos DB error: {e}")
        return None

def save_estimate(data):
    try:
        container = get_container("estimates")
        
        if container is None:
            # Mock save for local testing
            print(f"Mock save (no Cosmos DB): {data}")
            return data

        data["id"] = str(uuid.uuid4())
        data["type"] = "estimate"
        data["timestamp"] = datetime.utcnow().isoformat()

        container.upsert_item(data)
        return data
    except Exception as e:
        print(f"Error saving estimate: {e}")
        # Don't fail the whole request, just log
        return data