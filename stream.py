import os
import time
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS S3 Configuration
S3_BUCKET = "parkease"
MANAGER_CLERK_ID = os.getenv("MANAGER_CLERK_ID")
S3_FOLDER = f"videos/{MANAGER_CLERK_ID}"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION")
RTSP_URL = os.getenv("RTSP_URL")

# Validate environment variables
if not AWS_ACCESS_KEY or not AWS_SECRET_KEY or not AWS_REGION_NAME or not RTSP_URL:
    raise EnvironmentError("Missing required environment variables.")

# Output folder for video clips
OUTPUT_FOLDER = "./clips"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION_NAME,
)

def upload_to_s3(file_path, bucket, s3_key):
    """Uploads a file to S3."""
    try:
        s3_client.upload_file(file_path, bucket, s3_key)
        print(f"Uploaded: {file_path} -> s3://{bucket}/{s3_key}")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def record_and_upload():
    """Continuously records 5-minute clips and uploads them to S3."""
    clip_index = 0

    while True:
        clip_filename = f"clip_{clip_index:04d}.mp4"
        clip_path = os.path.join(OUTPUT_FOLDER, clip_filename)

        # GStreamer pipeline to capture a 5-minute clip (300 seconds)
        gst_pipeline = (
            f"timeout 120 gst-launch-1.0 rtspsrc location={RTSP_URL} ! "
            f"decodebin ! videoconvert ! x264enc ! mp4mux ! "
            f"filesink location={clip_path} -e"
        )

        try:
            # Record video using GStreamer
            print(f"Recording 5-minute clip: {clip_path}")
            os.system(gst_pipeline)

            # Check if the file was created
            if not os.path.exists(clip_path):
                print(f"Clip not recorded: {clip_path}")
                time.sleep(5)  # Retry delay
                continue

            # Upload to S3
            s3_key = os.path.join(S3_FOLDER, clip_filename)
            upload_to_s3(clip_path, S3_BUCKET, s3_key)

            # Optionally delete local file after uploading
            os.remove(clip_path)
            print(f"Deleted local file: {clip_path}")

            clip_index += 1
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Retry delay

if _name_ == "_main_":
    try:
        record_and_upload()
    except KeyboardInterrupt:
        print("Stopped by user.")