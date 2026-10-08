from config.db import dynamodb, APPLICATIONS_TABLE

table = dynamodb.Table(APPLICATIONS_TABLE)

def create_application(user_id: str, job_id: str, item: dict):
    item.update({"userId": user_id, "jobId": job_id})
    table.put_item(Item=item)
    return item

def get_application(user_id: str, job_id: str):
    response = table.get_item(Key={"userId": user_id, "jobId": job_id})
    return response.get("Item")

def list_applications_for_user(user_id: str):
    response = table.query(
        KeyConditionExpression="userId = :uid",
        ExpressionAttributeValues={":uid": user_id}
    )
    return response.get("Item", [])

def update_application_status(user_id: str, job_id: str, status: str):
    response = table.update_item(
        Key={"userId": user_id, "jobId": job_id},
        UpdateExpression="SET #s = :status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": status},
        ReturnValues="ALL_NEW",
    )
    return response["Attributes"]

def delete_application(user_id: str, job_id: str):
    table.delete_item(Key={"userId": user_id, "jobId": job_id})
    
def list_applicants_for_job(job_id: str):
    # Uses the JobIndex GSi (jobId as a partition key)
    response = table.query(
        IndexName="JobIndex",
        KeyConditionExpression="jobId = :jid",
        ExpressionAttributeValues={":jid": job_id},
    )
    return response.get("Item", [])