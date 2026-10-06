from config.db import dynamodb, VIEWED_JOBS_TABLE

table = dynamodb.Table(VIEWED_JOBS_TABLE)

def record_view(user_id: str, job_id: str, item: dict):
    item.update({"userId": user_id, "jobId": job_id})
    table.put_item(Item=item)
    return item

def list_viewed_jobs(user_id: str):
    response = table.query(
        KeyConditionExpression="userId = :uid",
        ExpressionAttributeValues={":uid": user_id},
    )
    return response.get("Items", [])