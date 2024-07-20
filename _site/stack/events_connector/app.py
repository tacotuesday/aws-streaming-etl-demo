# Make sure boto3 is installed locally, i.e. pip install boto3
import json
import random
import boto3
import datetime

kinesis_client = boto3.client("kinesis", region_name="us-east-1")
# Constants:
STREAM_NAME = "tacotuesday-stream-staging"


def get_data():
    return {
        "event_time": datetime.datetime.now().isoformat(),
        "event_name": random.choice(
            ["JOIN", "LEAVE", "OPEN_CHAT", "SUBSCRIBE", "SEND_MESSAGE"]
        ),
        "user": round(random.random() * 100),
    }

def lambda_handler(event, context):
    processed = 0
    print(STREAM_NAME)
    try:
        print("Trying to send events to Kinesis...")
        for i in range(0, 45):
            data = get_data()
            print(i, " : ", data)
            kinesis_client.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(data),
                PartitionKey="partitionkey",
            )
            processed += 1
    except Exception as e:
        print(e)
    message = "Successfully processed {} events.".format(processed)
    return {"statusCode": 200, "body": {"lambdaResult": message}}