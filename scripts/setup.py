"""
Creates the local DynamoDB tables and seeds sample JOBS.

Users are NOT seeded: a user's id is their Firebase uid, which only exists after you
sign up through Firebase. Create a test account from your React app (or the Firebase
console), then call POST /auth/sync to create the matching DynamoDB profile.

Usage (from the backend folder), with DynamoDB Local running:
    python scripts/setup.py
    python scripts/setup.py --reset    # delete all tables first
"""

import os
import sys
import uuid
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from config.db import dynamodb, USERS_TABLE, JOBS_TABLE, APPLICATIONS_TABLE, VIEWED_JOBS_TABLE

client = dynamodb.meta.client
ALL_TABLES = [USERS_TABLE, JOBS_TABLE, APPLICATIONS_TABLE, VIEWED_JOBS_TABLE]


def reset_tables():
    existing = client.list_tables()["TableNames"]
    for name in ALL_TABLES:
        if name in existing:
            dynamodb.Table(name).delete()
            dynamodb.Table(name).wait_until_not_exists()
            print(f"Deleted {name}")


def create_tables():
    existing = client.list_tables()["TableNames"]

    table_defs = [
        {
            "TableName": USERS_TABLE,  # key = Firebase uid (no email index needed: Firebase handles login)
            "AttributeDefinitions": [{"AttributeName": "userId", "AttributeType": "S"}],
            "KeySchema": [{"AttributeName": "userId", "KeyType": "HASH"}],
        },
        {
            "TableName": JOBS_TABLE,
            "AttributeDefinitions": [{"AttributeName": "jobId", "AttributeType": "S"}],
            "KeySchema": [{"AttributeName": "jobId", "KeyType": "HASH"}],
        },
        {
            "TableName": APPLICATIONS_TABLE,
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
            "TableName": VIEWED_JOBS_TABLE,
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


def seed_jobs():
    now = datetime.now(timezone.utc).isoformat()
    for title in ["Frontend Engineer", "Backend Engineer", "Product Designer"]:
        job_id = str(uuid.uuid4())
        dynamodb.Table(JOBS_TABLE).put_item(Item={
            "jobId": job_id, "title": title, "company": "Acme Co", "postedAt": now,
        })
        print(f"Seeded job: {title} ({job_id})")


if __name__ == "__main__":
    if "--reset" in sys.argv:
        reset_tables()
    create_tables()
    seed_jobs()
