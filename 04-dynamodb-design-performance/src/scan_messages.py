import boto3

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("messaging-app-messages")

print("Starting table scan...")

response = table.scan(
    ReturnConsumedCapacity="TOTAL"
)

print(f"Items scanned: {response['ScannedCount']}")
print(f"Items returned: {response['Count']}")
print(f"Consumed capacity units: {response['ConsumedCapacity']['CapacityUnits']}")

print("Scan completed.")