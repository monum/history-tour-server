import boto3
from boto3.dynamodb.types import TypeDeserializer

import json
from get_route import generate_presigned_urls_for_route

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
deserializer = TypeDeserializer()

BUCKET = "history-tour-server-tourassetssbucketb8884501-1tv88uba51ic2"
TABLE = "HistoryTourServerAppStack-RouteTable64965DD4-1FJF389OM46QH"

def handler(event, context):
    route_name = ""
    response_code = 200

    print("request: " + json.dumps(event))

    if (event["queryStringParameters"] and event["queryStringParameters"]["routeName"]):
        print("Received query: " + event["queryStringParameters"]["routeName"])
        route_name = event["queryStringParameters"]["routeName"]

        db_response = dynamodb.get_item(
            TableName = TABLE,
            Key={
                'routeName': {'S': route_name}
            }
        )
        route = db_response['item']
        deserialized_route = {k: deserializer.deserialize(v) for k, v in route.items()}
        generate_presigned_urls_for_route(deserialized_route)
        tour = deserialized_route["tourStops"]

        response_body = {"tourStops": tour}
    else:
        message = "Please give valid parameter"
        response_body = {"message": message, "input": event}

    response = {
            "statusCode": response_code,
            "headers": {
                "Content-Type" : "application/json"
            },
            "body": json.dumps(response_body)
        }
    return response