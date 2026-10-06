from config.db import dynamodb, APLLICATIONS_TABLE

table = dynamodb.Table(APPLICATIONS_TABLE)

def create_application(user_id: str, job_id: str, item: dict):
    