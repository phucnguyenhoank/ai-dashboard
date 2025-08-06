from pymongo import MongoClient
from datetime import datetime
import base64
from app.utils.image_storage import get_base64_from_path
import os

# Ensure the images directory exists
if not os.path.exists("images"):
    os.makedirs("images")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ai_dashboard"]
cameras_collection = db["cameras"]
users_collection = db["users"]
detections_collection = db["detections"]

# Sample base64 string from the dump image
sample_base64 = get_base64_from_path("images\\loading_cat.png", include_prefix=True)

# Sample data for users
users = [
    {"user_id": "user1", "name": "Alice", "phone": "+1111111111"},
    {"user_id": "user2", "name": "Bob", "phone": "+2222222222"},
    {"user_id": "user3", "name": "Charlie", "phone": "+3333333333"},
    {"user_id": "user4", "name": "David", "phone": "+4444444444"},
    {"user_id": "user5", "name": "Eve", "phone": "+5555555555"}
]

# Sample data for cameras
cameras = [
    {
        "camera_id": "cam1",
        "name": "Entrance Cam",
        "image_path": "images/cam1.jpg",
        "short_description": "Monitors entrance",
        "details_description": "High-res camera with night vision"
    },
    {
        "camera_id": "cam2",
        "name": "Parking Lot Cam",
        "image_path": "images/cam2.jpg",
        "short_description": "Monitors parking lot",
        "details_description": "Wide-angle camera"
    },
    {
        "camera_id": "cam3",
        "name": "Warehouse Cam",
        "image_path": "images/cam3.jpg",
        "short_description": "Monitors warehouse",
        "details_description": "PTZ camera"
    },
    {
        "camera_id": "cam4",
        "name": "Office Cam",
        "image_path": "images/cam4.jpg",
        "short_description": "Monitors office",
        "details_description": "Dome camera"
    },
    {
        "camera_id": "cam5",
        "name": "Backyard Cam",
        "image_path": "images/cam5.jpg",
        "short_description": "Monitors backyard",
        "details_description": "Weatherproof camera"
    }
]

# Sample data for detections
detections = [
    {
        "type": "knife",
        "lat": 40.7128,
        "long": -74.0060,
        "timestamp": datetime(2023, 10, 1, 12, 0, 0),
        "seen": False,
        "camera_id": "cam1",
        "user_id": "user1",
        "camera_name": "Entrance Cam",
        "user_name": "Alice",
        "image_path": "images/det1.jpg"
    },
    {
        "type": "gun",
        "lat": 34.0522,
        "long": -118.2437,
        "timestamp": datetime(2023, 10, 2, 14, 30, 0),
        "seen": True,
        "camera_id": "cam2",
        "user_id": "user2",
        "camera_name": "Parking Lot Cam",
        "user_name": "Bob",
        "image_path": "images/det2.jpg"
    },
    {
        "type": "person",
        "lat": 51.5074,
        "long": -0.1278,
        "timestamp": datetime(2023, 10, 3, 9, 15, 0),
        "seen": False,
        "camera_id": "cam3",
        "user_id": "user3",
        "camera_name": "Warehouse Cam",
        "user_name": "Charlie",
        "image_path": "images/det3.jpg"
    },
    {
        "type": "car",
        "lat": 48.8566,
        "long": 2.3522,
        "timestamp": datetime(2023, 10, 4, 16, 45, 0),
        "seen": True,
        "camera_id": "cam4",
        "user_id": "user4",
        "camera_name": "Office Cam",
        "user_name": "David",
        "image_path": "images/det4.jpg"
    },
    {
        "type": "dog",
        "lat": 35.6895,
        "long": 139.6917,
        "timestamp": datetime(2023, 10, 5, 11, 20, 0),
        "seen": False,
        "camera_id": "cam5",
        "user_id": "user5",
        "camera_name": "Backyard Cam",
        "user_name": "Eve",
        "image_path": "images/det5.jpg"
    },
    {
        "type": "knife",
        "lat": 40.7128,
        "long": -74.0060,
        "timestamp": datetime(2023, 10, 6, 13, 0, 0),
        "seen": True,
        "camera_id": "cam1",
        "user_id": "user2",
        "camera_name": "Entrance Cam",
        "user_name": "Bob",
        "image_path": "images/det6.jpg"
    },
    {
        "type": "gun",
        "lat": 34.0522,
        "long": -118.2437,
        "timestamp": datetime(2023, 10, 7, 15, 30, 0),
        "seen": False,
        "camera_id": "cam2",
        "user_id": "user3",
        "camera_name": "Parking Lot Cam",
        "user_name": "Charlie",
        "image_path": "images/det7.jpg"
    },
    {
        "type": "person",
        "lat": 51.5074,
        "long": -0.1278,
        "timestamp": datetime(2023, 10, 8, 10, 0, 0),
        "seen": True,
        "camera_id": "cam3",
        "user_id": "user4",
        "camera_name": "Warehouse Cam",
        "user_name": "David",
        "image_path": "images/det8.jpg"
    },
    {
        "type": "car",
        "lat": 48.8566,
        "long": 2.3522,
        "timestamp": datetime(2023, 10, 9, 17, 0, 0),
        "seen": False,
        "camera_id": "cam4",
        "user_id": "user5",
        "camera_name": "Office Cam",
        "user_name": "Eve",
        "image_path": "images/det9.jpg"
    },
    {
        "type": "dog",
        "lat": 35.6895,
        "long": 139.6917,
        "timestamp": datetime(2023, 10, 10, 12, 30, 0),
        "seen": True,
        "camera_id": "cam5",
        "user_id": "user1",
        "camera_name": "Backyard Cam",
        "user_name": "Alice",
        "image_path": "images/det10.jpg"
    }
]

# Insert sample data
def insert_sample_data():
    # Clear existing data (optional)
    cameras_collection.delete_many({})
    users_collection.delete_many({})
    detections_collection.delete_many({})

    # Save sample images for cameras and insert
    for camera in cameras:
        with open(camera["image_path"], "wb") as f:
            f.write(base64.b64decode(sample_base64.split(",")[1]))
        cameras_collection.insert_one(camera)

    # Insert users
    users_collection.insert_many(users)

    # Save sample images for detections and insert
    for detection in detections:
        with open(detection["image_path"], "wb") as f:
            f.write(base64.b64decode(sample_base64.split(",")[1]))
        detections_collection.insert_one(detection)

    print("Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()