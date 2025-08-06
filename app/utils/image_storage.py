# api/utils/image_storage.py
import os
import base64
import uuid

# Define the directory where images will be saved
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def save_base64_image(base64_string: str) -> str:
    """
    Saves a base64-encoded image to the local file system.
    Returns the file path or None if an error occurs.
    """
    try:
        # Remove "data:image/..." prefix if present
        if base64_string.startswith("data:image"):
            base64_string = base64_string.split(",")[1]
        
        # Remove whitespace/newlines
        base64_string = base64_string.strip().replace("\n", "").replace("\r", "")

        # Add padding if missing
        missing_padding = len(base64_string) % 4
        if missing_padding:
            base64_string += "=" * (4 - missing_padding)

        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)
        image_bytes = base64.b64decode(base64_string)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        return filepath
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

def get_base64_from_path(image_path: str, include_prefix: bool = False) -> str:
    """
    Reads an image from the given path and returns its base64-encoded string.
    If include_prefix=True, returns a string like "data:image/jpeg;base64,<base64>".
    Returns None if an error occurs.
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")

        # Remove newlines just in case
        encoded = encoded.strip().replace("\n", "").replace("\r", "")

        if include_prefix:
            # Detect extension for correct MIME type
            ext = os.path.splitext(image_path)[1].lower()
            mime_type = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }.get(ext, "application/octet-stream")
            return f"data:{mime_type};base64,{encoded}"

        return encoded

    except Exception as e:
        print(f"Error reading image: {e}")
        return None
