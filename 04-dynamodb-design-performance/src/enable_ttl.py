import boto3
import time

dynamodb = boto3.client("dynamodb", region_name="ap-south-1")

TABLE_NAME = "messaging-app-messages"

print("Enabling TTL...")

dynamodb.update_time_to_live(
    TableName=TABLE_NAME,
    TimeToLiveSpecification={
        "Enabled": True,
        "AttributeName": "expires_at"
    }
)

print("TTL configuration submitted.")
print("Checking TTL status...")

time.sleep(2)

response = dynamodb.describe_time_to_live(
    TableName=TABLE_NAME
)

print("TTL status:", response["TimeToLiveDescription"]["TimeToLiveStatus"])
print("TTL attribute:", response["TimeToLiveDescription"].get("AttributeName"))