# read_mongodb_base64_to_image.py

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary
import urllib.parse
import base64
import os

# ===== 1. MongoDB connection details (same style as your other script) =====

# Replace these with your actual AWS credentials
aws_access_key_id = ""
aws_secret_access_key = ""

# URL-encode credentials in case they contain special characters
username = urllib.parse.quote_plus(aws_access_key_id)
password = urllib.parse.quote_plus(aws_secret_access_key)

host = ""
database_name = ""
collection_name = ""   # <--- change if needed

# Compose the SRV URI with AWS authentication (same pattern as your script)
mongo_uri = (
    f"mongodb+srv://{username}:{password}@{host}/{database_name}"
    "?authMechanism=MONGODB-AWS"
    "&authSource=%24external"
    "&appName=vs629"
)

# ===== 2. Input: ObjectId and output file path =====
# Put the _id you want to read here
target_id_str = ""        # <- change this

# Where to save the output image
output_image_path = "gateway_attachment_output.jpg"  # extension can be .png, .jpg, etc.


def get_image_bytes_from_doc(doc):
    """
    Extract raw image bytes from the 'data' field.
    Handles:
      - BSON Binary
      - bytes/bytearray
      - base64-encoded string
    """
    data_field = doc.get("data")

    if data_field is None:
        raise ValueError("Document has no 'data' field")

    # PyMongo Binary type
    if isinstance(data_field, Binary):
        return bytes(data_field)

    # Raw bytes
    if isinstance(data_field, (bytes, bytearray)):
        return bytes(data_field)

    # Base64-encoded string
    if isinstance(data_field, str):
        # If it’s prefixed like "data:image/png;base64,....", strip metadata
        if "," in data_field and "base64" in data_field[:50]:
            data_field = data_field.split(",", 1)[1]

        return base64.b64decode(data_field)

    raise TypeError(f"Unsupported type for 'data' field: {type(data_field)}")


def main():
    # 1. Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # 2. Find the document by _id
    target_id = ObjectId(target_id_str)
    doc = collection.find_one({"_id": target_id})

    if not doc:
        print(f"No document found with _id = {target_id_str}")
        return

    try:
        # 3. Extract image bytes from 'data' field
        image_bytes = get_image_bytes_from_doc(doc)

        # 4. Write to file
        with open(output_image_path, "wb") as f:
            f.write(image_bytes)

        print(f"Image written to: {os.path.abspath(output_image_path)}")

    except Exception as e:
        print(f"Error while creating image: {e}")


if __name__ == "__main__":
    main()
