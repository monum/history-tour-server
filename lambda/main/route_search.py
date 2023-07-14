import boto3
from boto3.dynamodb.types import TypeDeserializer

import json
from get_route import generate_presigned_urls_for_route

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
deserializer = TypeDeserializer()

TABLE = "History-Tour-Server-RouteTable64965DD4-1FJF389OM46QH"

def handler(event, context):
    response_code = 200

    print("request: " + json.dumps(event))

    if (event["queryStringParameters"] and event["queryStringParameters"]["query"]):
        print("Received query: " + event["queryStringParameters"]["query"])
        query = event["queryStringParameters"]["query"]
        
        # check if query is substring of key
        db_response = dynamodb.scan(
            TableName = TABLE,
            FilterExpression = "contains(#routeName, :routeName)",
            ExpressionAttributeNames = {"#routeName": "routeName"},
            ExpressionAttributeValues = {
                ':routeName':{'S': query}
            }
        )

        routes = db_response["Items"]
        
        for route in range(0,len(routes)):
            db_response["Items"][route] = {k: deserializer.deserialize(v) for k, v in routes[route].items()}
    
        for route in range(0,len(routes)):
            routes[route] = generate_presigned_urls_for_route(routes[route])
        response_body = {"routes":routes}
    else:
        message = "Please input valid parameters"
        response_body = {"message": message, "input": event}

    response = {
        "statusCode": response_code,
        "headers": {
           "Content-Type" : "application/json"
        },
        "body": json.dumps(response_body)
    }
    return response
