from pymongo import MongoClient
from datetime import datetime, timezone
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
camera_sample_base64 = get_base64_from_path("images\\camera1.png", include_prefix=True)
frog_sample_base64 = get_base64_from_path("images\\frog.png", include_prefix=True)


# Sample data for users
users = [
    {"user_id": "user1", "name": "Alice", "phone": "+1111111111", "is_active": True},
    {"user_id": "user2", "name": "Bob", "phone": "+2222222222", "is_active": True},
    {"user_id": "user3", "name": "Charlie", "phone": "+3333333333", "is_active": False},
    {"user_id": "user4", "name": "David", "phone": "+4444444444", "is_active": False},
    {"user_id": "user5", "name": "Eve", "phone": "+5555555555", "is_active": True}
]

# Sample data for cameras

cameras = [
    {
        "camera_id": "cam1",
        "name": "Entrance Cam",
        "image_path": "images/cam1.jpg",
        "short_description": "Model: AI-Cam X512 | Resolution: 2560×1440 (2K Quad HD)",
        "details_description": (
            "Model: AI-Cam X512\n"
            "Resolution: 2560 × 1440 (2K Quad HD)\n"
            "Frame Rate: 30 FPS\n"
            "Lens: 3.6mm Fixed Lens\n"
            "Field of View: 110° (Horizontal)\n"
            "Night Vision: IR-Cut Filter, 30m (98ft) Range\n"
            "AI Features:\n"
            "  - Person Detection\n"
            "  - Vehicle Detection\n"
            "  - Face Recognition\n"
            "  - Intrusion Zone Detection\n"
            "  - License Plate Recognition (LPR)\n"
            "Video Compression: H.265 / H.264 / MJPEG\n"
            "Audio: Built-in Mic & Speaker (Two-way audio)\n"
            "Storage:\n"
            "  - microSD Card up to 256GB\n"
            "  - Cloud (optional)\n"
            "  - RTSP/NVR supported\n"
            "Connectivity:\n"
            "  - Ethernet (RJ45, PoE)\n"
            "  - Wi-Fi 2.4GHz (optional model)\n"
            "Power: PoE (802.3af) or 12V DC\n"
            "Operating Temperature: -20°C to 60°C\n"
            "Waterproof Rating: IP67\n"
            "Smart Alerts: Real-time push notification with snapshot\n"
            "Dimensions: 145mm × 70mm × 70mm\n"
            "Weight: 350g"
        )
    },
    {
        "camera_id": "cam2",
        "name": "Parking Lot Cam",
        "image_path": "images/cam2.jpg",
        "short_description": "Model: AI-Cam P410 | Resolution: 1920×1080 (Full HD)",
        "details_description": (
            "Model: AI-Cam P410\n"
            "Resolution: 1920 × 1080 (Full HD)\n"
            "Frame Rate: 60 FPS\n"
            "Lens: 2.8mm Wide-Angle Lens\n"
            "Field of View: 120° (Horizontal)\n"
            "Night Vision: IR-Cut Filter, 25m (82ft) Range\n"
            "AI Features:\n"
            "  - Vehicle Detection\n"
            "  - Intrusion Zone Detection\n"
            "Video Compression: H.265 / H.264\n"
            "Audio: Built-in Mic\n"
            "Storage:\n"
            "  - microSD Card up to 128GB\n"
            "  - RTSP/NVR supported\n"
            "Connectivity: Ethernet (RJ45)\n"
            "Power: PoE or 12V DC\n"
            "Operating Temperature: -10°C to 55°C\n"
            "Waterproof Rating: IP66\n"
            "Smart Alerts: Motion detection alerts\n"
            "Dimensions: 150mm × 75mm × 75mm\n"
            "Weight: 320g"
        )
    },
    {
        "camera_id": "cam3",
        "name": "Warehouse Cam",
        "image_path": "images/cam3.jpg",
        "short_description": "Model: AI-Cam W730 | Resolution: 3840×2160 (4K Ultra HD)",
        "details_description": (
            "Model: AI-Cam W730\n"
            "Resolution: 3840 × 2160 (4K Ultra HD)\n"
            "Frame Rate: 25 FPS\n"
            "Lens: 4.0–120mm Motorized Zoom Lens (PTZ)\n"
            "Field of View: 90°–10° (Adjustable)\n"
            "Night Vision: IR LED Array, 100m (328ft) Range\n"
            "AI Features:\n"
            "  - Person Tracking\n"
            "  - Object Counting\n"
            "  - Intrusion Detection\n"
            "Video Compression: H.265+ / H.265 / H.264\n"
            "Audio: External Mic & Speaker Support\n"
            "Storage:\n"
            "  - microSD Card up to 512GB\n"
            "  - NVR\n"
            "Connectivity: Ethernet (RJ45, PoE+)\n"
            "Power: PoE+ or 24V AC\n"
            "Operating Temperature: -30°C to 65°C\n"
            "Waterproof Rating: IP67\n"
            "Smart Alerts: Auto-tracking with real-time alerts\n"
            "Dimensions: 300mm × 150mm × 150mm\n"
            "Weight: 1.5kg"
        )
    },
    {
        "camera_id": "cam4",
        "name": "Office Cam",
        "image_path": "images/cam4.jpg",
        "short_description": "Model: AI-Cam D220 | Resolution: 1920×1080 (Full HD)",
        "details_description": (
            "Model: AI-Cam D220\n"
            "Resolution: 1920 × 1080 (Full HD)\n"
            "Frame Rate: 30 FPS\n"
            "Lens: 2.8mm Fixed Lens\n"
            "Field of View: 105° (Horizontal)\n"
            "Night Vision: IR LEDs, 15m (49ft) Range\n"
            "AI Features:\n"
            "  - Face Recognition\n"
            "  - Loitering Detection\n"
            "Video Compression: H.265 / H.264\n"
            "Audio: Built-in Mic\n"
            "Storage:\n"
            "  - microSD Card up to 128GB\n"
            "  - Cloud Storage\n"
            "Connectivity: Wi-Fi 2.4GHz / Ethernet (optional)\n"
            "Power: USB-C 5V or PoE\n"
            "Operating Temperature: 0°C to 45°C\n"
            "Smart Alerts: Employee access monitoring\n"
            "Dimensions: 120mm × 60mm × 60mm\n"
            "Weight: 250g"
        )
    },
    {
        "camera_id": "cam5",
        "name": "Backyard Cam",
        "image_path": "images/cam5.jpg",
        "short_description": "Model: AI-Cam O540 | Resolution: 2560×1440 (2K Quad HD)",
        "details_description": (
            "Model: AI-Cam O540\n"
            "Resolution: 2560 × 1440 (2K Quad HD)\n"
            "Frame Rate: 30 FPS\n"
            "Lens: 2.8mm Fixed Lens\n"
            "Field of View: 115° (Horizontal)\n"
            "Night Vision: Color Night Vision, 20m (66ft) Range\n"
            "AI Features:\n"
            "  - Person Detection\n"
            "  - Animal Detection\n"
            "  - Package Detection\n"
            "Video Compression: H.265 / H.264\n"
            "Audio: Built-in Mic & Speaker (Two-way audio)\n"
            "Storage:\n"
            "  - microSD Card up to 256GB\n"
            "  - Cloud Storage\n"
            "Connectivity: Wi-Fi 2.4/5GHz\n"
            "Power: Solar Panel or 12V DC\n"
            "Operating Temperature: -20°C to 55°C\n"
            "Waterproof Rating: IP66\n"
            "Smart Alerts: Motion and sound detection\n"
            "Dimensions: 140mm × 70mm × 70mm\n"
            "Weight: 300g"
        )
    }
]



# Sample data for detections
detections = [
    {
        "type": "knife",
        "lat": 40.7128,
        "long": -74.0060,
        "timestamp": datetime(2023, 10, 1, 12, 0, 0, tzinfo=timezone.utc),
        "seen": False,
        "camera_id": "cam1",
        "user_id": "user1",
        "camera_name": "Entrance Cam",
        "user_name": "Alice",
        "image_path": "images/det1.jpg"
    },
    {
        "type": "knife",
        "lat": 34.0522,
        "long": -118.2437,
        "timestamp": datetime(2023, 10, 2, 14, 30, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 3, 9, 15, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 4, 16, 45, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 5, 11, 20, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 6, 13, 0, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 7, 15, 30, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 8, 10, 0, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 9, 17, 0, 0, tzinfo=timezone.utc),
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
        "timestamp": datetime(2023, 10, 10, 12, 30, 0, tzinfo=timezone.utc),
        "seen": False,
        "camera_id": "cam1",
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
            f.write(base64.b64decode(camera_sample_base64.split(",")[1]))
        cameras_collection.insert_one(camera)

    # Insert users
    users_collection.insert_many(users)

    # Save sample images for detections and insert
    for detection in detections:
        with open(detection["image_path"], "wb") as f:
            if detection["type"] == "dog":
                f.write(base64.b64decode(frog_sample_base64.split(",")[1]))
            else:
                f.write(base64.b64decode(sample_base64.split(",")[1]))
        detections_collection.insert_one(detection)

    print("Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()