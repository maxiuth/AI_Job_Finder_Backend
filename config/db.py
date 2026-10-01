import os
import boto3

IS_LOCAL = os.environ.get("ENV", "local") != "production"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
    endpoint_url="http://localhost:8000" if IS_LOCAL else None,
    aws_access_key_id="fake" if IS_LOCAL else None,
    aws_secret_access_key="fake" if IS_LOCAL else None,
)

USERS_TABLE = os.environ.get("USERS_TABLE", "Users")
JOBS_TABLE = os.environ.get("JOBS_TABLE", "Jobs")
APPLICATIONS_TABLE = os.environ.get("APPLICATIONS_TABLE", "Applications")
VIEWED_JOBS_TABLE = os.environ.get("VIEWED_JOBS_TABLE", "ViewedJobs")