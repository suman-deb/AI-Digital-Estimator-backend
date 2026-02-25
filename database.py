import os
import uuid
import json
from datetime import datetime

def get_container(container_name):
    """Get Cosmos DB container or return None if not configured"""
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
        print(f"Cosmos DB connection error: {e}")
        return None

def save_estimate(data):
    """Save estimate to Cosmos DB or mock if not configured"""
    try:
        container = get_container("estimates")
        
        if container is None:
            # Mock save for testing without Cosmos DB
            print(f"Mock save (Cosmos DB not configured)")
            print(f"Data: {json.dumps(data, indent=2)}")
            return data

        # Create a copy to avoid modifying original
        save_data = data.copy()
        save_data["id"] = str(uuid.uuid4())
        save_data["type"] = "estimate"
        save_data["timestamp"] = datetime.utcnow().isoformat()

        container.upsert_item(save_data)
        print(f"Successfully saved to Cosmos DB with id: {save_data['id']}")
        return save_data
        
    except Exception as e:
        print(f"Error saving to Cosmos DB: {str(e)}")
        print("Continuing without saving...")
        # Return original data - don't fail the request
        return data