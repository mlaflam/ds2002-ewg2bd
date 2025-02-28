#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

import boto3
import requests
import os
import sys
import mimetypes
from urllib.parse import urlparse

# Get input arguments
url = sys.argv[1]
bucket_name = sys.argv[2]
expiration_time = int(sys.argv[3])  # Convert expiration time to integer

s3 = boto3.client('s3', region_name='us-east-1')

def download_file(url, file_path):
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

  except requests.exceptions.RequestException as e:
    print(f"Error downloading: {e}")

def upload_and_presign(expires_in, file_name, bucket_name, object_name=None):
  if object_name is None:
    object_name = os.path.basename(file_name)

  # Determine MIME type - this keeps it from just downloading to browser
  content_type, _ = mimetypes.guess_type(file_name)
  if content_type is None:
    content_type = "application/octet-stream"  # Default if MIME type is unknown

  # Upload file with correct Content-Type
  s3.upload_file(
    file_name,
    bucket_name,
    object_name,
    ExtraArgs={'ContentType': content_type}  # Set Content-Type
  )

  print(f"File {file_name} uploaded as {object_name} in {bucket_name} with Content-Type {content_type}")

  # Generate a presigned URL
  presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_name},
    ExpiresIn=expires_in
  )

  print(f"Presigned URL: {presigned_url}")
  return presigned_url

# Parse the URL to get the filename
parsed_url = urlparse(url)
filename = os.path.basename(parsed_url.path)
path = os.path.join(os.getcwd(), filename)  # Saves to current directory

# Download file
download_file(url, path)

# Upload and presign
upload_and_presign(expiration_time, path, bucket_name, filename)

# Example Usage
# ./upload.py https://pngimg.com/uploads/dinosaur/dinosaur_PNG16609.png ds2002-lab4 300