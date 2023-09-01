import boto3
from boto3.dynamodb.types import TypeDeserializer

import json
from os import environ
from get_route import generate_presigned_urls_for_route

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
deserializer = TypeDeserializer()

table_name = environ["TABLE"]


def handler(event, context):
    response_code = 200

    print("request: " + json.dumps(event))

    if event["queryStringParameters"] and event["queryStringParameters"]["query"]:
        print("Received query: " + event["queryStringParameters"]["query"])
        query = event["queryStringParameters"]["query"]

        # check if query is substring of key
        db_response = dynamodb.scan(
            TableName=table_name,
            FilterExpression="contains(#routeName, :routeName)",
            ExpressionAttributeNames={"#routeName": "routeName"},
            ExpressionAttributeValues={":routeName": {"S": query}},
        )

        routes = db_response["Items"]
        for route in range(0, len(routes)):
            routes[route] = {
                k: deserializer.deserialize(v) for k, v in routes[route].items()
            }
            routes[route] = generate_presigned_urls_for_route(routes[route])
        response_body = {"routes": routes}
    else:
        message = "Please input valid parameters"
        response_body = {"message": message, "input": event}

    response = {
        "statusCode": response_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response_body),
    }
    return response
