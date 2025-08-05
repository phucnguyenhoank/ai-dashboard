from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URL"))
db = client["ai_dashboard"]  # Database name
detections_collection = db["detections"]  # Collection name