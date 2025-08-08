from pymongo import MongoClient
from bson import json_util
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URL"))
db = client["ai_dashboard"]

# Get collections
detections_collection = db["detections"]
cameras_collection = db["cameras"]
users_collection = db["users"]

# Fetch one document from each collection
detection_sample = detections_collection.find_one()
camera_sample = cameras_collection.find_one()
user_sample = users_collection.find_one()

# Combine into a single dictionary
export_data = {
    "detection_sample": detection_sample,
    "camera_sample": camera_sample,
    "user_sample": user_sample
}

# Export to a JSON file
output_path = "mongo_schema_samples.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=4, default=json_util.default)

print(f"Schema samples exported to: {output_path}")
