from config.db import dynamodb, USERS_TABLE

table = dynamodb.Table(USERS_TABLE)


def create_user(item: dict):
    # Fails (ConditionalCheckFailedException) if this userId already exists, so we never overwrite a profile
    table.put_item(Item=item, ConditionExpression="attribute_not_exists(userId)")
    return item


def get_user(user_id: str):
    response = table.get_item(Key={"userId": user_id})
    return response.get("Item")


def update_user(user_id: str, name: str):
    response = table.update_item(
        Key={"userId": user_id},
        UpdateExpression="SET #n = :name",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={":name": name},
        ReturnValues="ALL_NEW",
    )
    return response["Attributes"]


def delete_user(user_id: str):
    table.delete_item(Key={"userId": user_id})
