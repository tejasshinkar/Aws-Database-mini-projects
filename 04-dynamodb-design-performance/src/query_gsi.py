import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("messaging-app-messages")

sender_id = "user-019"

response = table.query(
    IndexName="sender-time-index",
    KeyConditionExpression=Key("sender_id").eq(sender_id)
)

print(f"Messages sent by: {sender_id}")
print(f"Messages found: {response['Count']}")

for item in response["Items"]:
    print(item)