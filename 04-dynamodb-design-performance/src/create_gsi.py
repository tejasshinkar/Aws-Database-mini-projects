import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "messaging-app-messages"
INDEX_NAME = "sender-time-index"

dynamodb = boto3.client("dynamodb", region_name="ap-south-1")

try:
    print("Creating Global Secondary Index...")

    response = dynamodb.update_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {
                "AttributeName": "sender_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "created_at",
                "AttributeType": "S"
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": INDEX_NAME,
                    "KeySchema": [
                        {
                            "AttributeName": "sender_id",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "created_at",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            }
        ]
    )

    print(f"GSI creation started: {INDEX_NAME}")
    print("Waiting for the index to become active...")

    waiter = dynamodb.get_waiter("table_exists")
    waiter.wait(TableName=TABLE_NAME)

    print("Table update completed.")

except ClientError as error:
    print("Error:", error)