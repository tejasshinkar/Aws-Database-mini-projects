import boto3
from boto3.dynamodb.types import TypeDeserializer

from config import AWS_REGION, DYNAMODB_TABLE


dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
deserializer = TypeDeserializer()


def put_user(user_id, name, email):
    response = dynamodb.put_item(
        TableName=DYNAMODB_TABLE,
        Item={
            "user_id": {"S": user_id},
            "name": {"S": name},
            "email": {"S": email},
        },
    )

    return response


def get_user(user_id):
    response = dynamodb.get_item(
        TableName=DYNAMODB_TABLE,
        Key={"user_id": {"S": user_id}},
    )

    item = response.get("Item")

    if not item:
        return None

    return {
        key: deserializer.deserialize(value)
        for key, value in item.items()
    }


def update_user(user_id, name, email):
    response = dynamodb.update_item(
        TableName=DYNAMODB_TABLE,
        Key={"user_id": {"S": user_id}},
        UpdateExpression="SET #n = :name, email = :email",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":name": {"S": name},
            ":email": {"S": email},
        },
        ReturnValues="ALL_NEW",
    )

    item = response.get("Attributes", {})

    return {
        key: deserializer.deserialize(value)
        for key, value in item.items()
    }


def delete_user(user_id):
    response = dynamodb.delete_item(
        TableName=DYNAMODB_TABLE,
        Key={"user_id": {"S": user_id}},
        ReturnValues="ALL_OLD",
    )

    item = response.get("Attributes")

    if not item:
        return None

    return {
        key: deserializer.deserialize(value)
        for key, value in item.items()
    }


if __name__ == "__main__":
    user = get_user("user-1")
    print(user)
