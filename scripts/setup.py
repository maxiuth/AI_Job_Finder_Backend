# setup.py
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000",
    aws_access_key_id="fake",
    aws_secret_access_key="fake",
)
client = dynamodb.meta.client


def create_tables():
    existing = client.list_tables()["TableNames"]

    table_defs = [
        {
            "TableName": "Users",
            "AttributeDefinitions": [{"AttributeName": "userId", "AttributeType": "S"}],
            "KeySchema": [{"AttributeName": "userId", "KeyType": "HASH"}],
        },
        {
            "TableName": "Jobs",
            "AttributeDefinitions": [{"AttributeName": "jobId", "AttributeType": "S"}],
            "KeySchema": [{"AttributeName": "jobId", "KeyType": "HASH"}],
        },
        {
            "TableName": "Applications",
            "AttributeDefinitions": [
                {"AttributeName": "userId", "AttributeType": "S"},
                {"AttributeName": "jobId", "AttributeType": "S"},
            ],
            "KeySchema": [
                {"AttributeName": "userId", "KeyType": "HASH"},
                {"AttributeName": "jobId", "KeyType": "RANGE"},
            ],
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "JobIndex",
                    "KeySchema": [
                        {"AttributeName": "jobId", "KeyType": "HASH"},
                        {"AttributeName": "userId", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
        },
        {
            "TableName": "ViewedJobs",
            "AttributeDefinitions": [
                {"AttributeName": "userId", "AttributeType": "S"},
                {"AttributeName": "jobId", "AttributeType": "S"},
            ],
            "KeySchema": [
                {"AttributeName": "userId", "KeyType": "HASH"},
                {"AttributeName": "jobId", "KeyType": "RANGE"},
            ],
        },
    ]

    for definition in table_defs:
        name = definition["TableName"]
        if name in existing:
            print(f"{name} already exists, skipping.")
            continue

        dynamodb.create_table(**definition, BillingMode="PAY_PER_REQUEST")
        dynamodb.Table(name).wait_until_exists()
        print(f"Created {name}")


def seed():
    users_table = dynamodb.Table("Users")
    jobs_table = dynamodb.Table("Jobs")
    applications_table = dynamodb.Table("Applications")
    viewed_table = dynamodb.Table("ViewedJobs")

    user_id = str(uuid.uuid4())
    job_ids = [str(uuid.uuid4()) for _ in range(3)]
    job_titles = ["Frontend Engineer", "Backend Engineer", "Product Designer"]

    users_table.put_item(Item={
        "userId": user_id,
        "email": "alice@example.com",
        "name": "Alice",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    })

    for job_id, title in zip(job_ids, job_titles):
        jobs_table.put_item(Item={
            "jobId": job_id,
            "title": title,
            "company": "Acme Co",
            "postedAt": datetime.now(timezone.utc).isoformat(),
        })

    # Alice viewed all three
    for job_id in job_ids:
        viewed_table.put_item(Item={
            "userId": user_id,
            "jobId": job_id,
            "viewedAt": datetime.now(timezone.utc).isoformat(),
        })

    # Alice applied to the first one
    applications_table.put_item(Item={
        "userId": user_id,
        "jobId": job_ids[0],
        "status": "applied",
        "appliedAt": datetime.now(timezone.utc).isoformat(),
    })

    print("Seeded data. Test userId:", user_id)


if __name__ == "__main__":
    create_tables()
    seed()