import json
import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client('dynamodb')
deserializer = TypeDeserializer()


def handler(event, context):
    routeName = ""
    responseCode = 200

    print("request: " + json.dumps(event))

    #todo - mapping from S3 buckets for images and audio

    if (event["queryStringParameters"] and event["queryStringParameters"]["routeName"]):
        print("Received query: " + event["queryStringParameters"]["routeName"])
        routeName = event["queryStringParameters"]["routeName"]

        # todo - update TableName
        db_response = dynamodb.get_item(
            TableName = "HistoryTourServerAppStack-RouteTableTest64965DD4-1FJF389OM46QH", 
            Key={
                'routeName': {'S': routeName}
            }
        )

        document = db_response['Item']
        print(document)
        deserialized_document = {k: deserializer.deserialize(v) for k, v in document.items()}
        response_body = deserialized_document
    else:
        message = "Please give valid parameter"
        response_body = {"message": message, "input": event}

    response = {
            "statusCode": responseCode,
            "headers": {
                "Content-Type" : "application/json"
            },
            "body": json.dumps(response_body)
        }
    return response

