import os
import base64
import uuid

# Define the directory where images will be saved
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def save_base64_image(base64_string: str) -> str:
    """
    Saves a base64 encoded image to the local file system.
    Returns the file path.
    """
    try:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        # Decode the base64 string
        image_bytes = base64.b64decode(base64_string)

        # Write the bytes to a file
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        return filepath
    except Exception as e:
        print(f"Error saving image: {e}")
        return None