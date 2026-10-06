from config.db import dynamodb, JOBS_TABLE

table = dynamodb.Table(JOBS_TABLE)

def create_job(item: dict):
    table.put_item(Item=item)
    return item

def get_job(job_id: str):
    response = table.get_item(Key={"jobId": job_id})
    return response.get("Item")

def list_jobs():
    response = table.scan()
    return response.get("Items", [])