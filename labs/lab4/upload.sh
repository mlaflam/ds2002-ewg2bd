#!/bin/bash

filename="$1"
bucket_name="$2"
expiration_time="$3"

default_expiration_time=604800 #default 7 days

# Check if expiration_time is specified, otherwise use default
if [ -z "$expiration_time" ]; then
  expiration_time=$default_expiration_time
fi

# Upload
aws s3 cp $filename s3://$bucket_name

# Presign
aws s3 presign --expires-in $expiration_time s3://$bucket_name/$filename