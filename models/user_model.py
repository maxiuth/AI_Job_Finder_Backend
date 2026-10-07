from config.db import dynamodc, USERS_TABLE

table = dynamodb.Table(USERS_TABLE)

def create_user(item: dict):
    """
    Create a new user
    """
    table.put_item(Item=item)
    return item

def get_user(user_id: str):
    response = table.get_item(Key={"userId": user_id})
    return response.get("Item")

def list_users():
    response = table.scan()
    return response.get("Items", [])

def update_user(user_id: str, name: str):
    response = table.update_item(
        Key={"userId": user_id},
        UpdateExpression="SET #n = :name",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={":name": name},
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes")

def delete_user(user_id: str):
    table.delete_item(Key={"userId": user_id})
    return "User deleted successfully"