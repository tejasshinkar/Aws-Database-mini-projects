import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "messaging-app-messages"
REGION = "ap-south-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

conversation_id = "conversation-001"
message_id = "message-0001"

try:
    response = table.update_item(
        Key={
            "conversation_id": conversation_id,
            "message_id": message_id
        },
        UpdateExpression="SET message_text = :new_text",
        ConditionExpression="attribute_exists(message_id)",
        ExpressionAttributeValues={
            ":new_text": "Updated using a conditional write."
        },
        ReturnValues="UPDATED_NEW"
    )

    print("Conditional update successful!")
    print("Updated values:", response["Attributes"])

except ClientError as error:
    if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
        print("Condition failed: Item does not exist.")
    else:
        print("Error:", error)