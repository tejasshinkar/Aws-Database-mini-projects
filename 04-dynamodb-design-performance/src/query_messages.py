import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("messaging-app-messages")

conversation_id = "conversation-001"

response = table.query(
    KeyConditionExpression=Key("conversation_id").eq(conversation_id)
)

items = response["Items"]

print(f"Conversation: {conversation_id}")
print(f"Messages found: {len(items)}")

for item in items[:5]:
    print(item)