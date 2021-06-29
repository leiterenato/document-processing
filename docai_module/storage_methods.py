from . import config

# Generates a signed URL for downloading a blob using HTTP GET.
def create_signed_url_download(
    blob_name: str,
    bucket_name: str
) -> str:
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="GET",
    )
    return url

# Generates a signed URL for uploading a blob using HTTP POST.
def create_signed_url_upload(
    blob_name: str,
    bucket_name: str,
    content_type: str
):
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="PUT",
        content_type=content_type,
    )
    return signed_url

# Download object from cloud storage
def download_blob_bytes(
    bucket_name: str, 
    source_blob_name: str
):
    """Downloads a blob from the bucket."""    
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_bytes()

# Upload bytes to cloud storage
def upload_blob_bytes(
    bucket_name: str, 
    image_bytes: bytes, 
    destination_blob_name: str,
    content_type: str
):
    """Uploads a file to the bucket."""
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(image_bytes, content_type=content_type)
    
# The bucket will have the same name as your project
def create_bucket(bucket_name):
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="us-east1")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

# Function to upload the PDF to a bucket
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = config.STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )