import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"
TABLE_NAME = "messaging-app-messages"


def check_dynamodb_table():
    dynamodb = boto3.client("dynamodb", region_name=REGION)

    try:
        response = dynamodb.describe_table(
            TableName=TABLE_NAME
        )

        table = response["Table"]

        print("DynamoDB connection successful!")
        print(f"Table name: {table['TableName']}")
        print(f"Table status: {table['TableStatus']}")
        print(f"Item count: {table.get('ItemCount', 0)}")
        print(f"Table ARN: {table['TableArn']}")

    except ClientError as error:
        print("Unable to access DynamoDB table.")
        print(f"Error: {error}")


if __name__ == "__main__":
    check_dynamodb_table()