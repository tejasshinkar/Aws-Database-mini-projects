
import boto3
from datetime import datetime, timedelta, timezone
import random
import uuid

TABLE_NAME = "messaging-app-messages"
REGION = "ap-south-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

sample_messages = [
    "Hey, how are you?",
    "Are we meeting today?",
    "The project is almost complete.",
    "Let's discuss this tomorrow.",
    "Can you send me the details?",
    "That sounds good!",
    "I will check and let you know.",
    "Thanks for your help."
]

print("Starting data insertion...")

with table.batch_writer() as batch:
    for i in range(1000):
        conversation_id = f"conversation-{(i % 50) + 1:03d}"
        message_id = f"message-{i + 1:04d}"

        item = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "sender_id": f"user-{random.randint(1, 20):03d}",
            "message_text": random.choice(sample_messages),
            "created_at": (
                datetime.now(timezone.utc) - timedelta(minutes=i)
            ).isoformat(),
            "message_type": "text"
        }

        batch.put_item(Item=item)

        if (i + 1) % 100 == 0:
            print(f"Inserted {i + 1} messages...")

print("Successfully inserted 1,000 messages.")