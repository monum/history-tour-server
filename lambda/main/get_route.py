import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

import json
import logging
from os import path

logger = logging.getLogger(__name__)

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
deserializer = TypeDeserializer()

BUCKET = "history-tour-server-tourassetssbucketb8884501-1tv88uba51ic2"
TABLE = "HistoryTourServerAppStack-RouteTable64965DD4-1FJF389OM46QH"

def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    Parameters
    ----------
    s3_client: 
        A Boto3 Amazon S3 client.
    client_method: 
        The name of the client method that the URL performs.
    method_parameters: 
        The parameters of the specified client method.
    expires_in: 
        The number of seconds the presigned URL is valid for.
    
    Returns
    -------
    url: 
        The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method)
        raise
    return url

def generate_presigned_urls_for_route(deserialized_route):
    for tour_stop in range(0,len(deserialized_route["tourStops"])):
        current_stop = deserialized_route["tourStops"][tour_stop]
        parameters = { "Bucket": BUCKET }

        for image in range(0,len(current_stop["images"])):
            parameters["Key"] = path.join("images", current_stop["images"][image])
            presigned_url = generate_presigned_url(s3, 'get_object', parameters, 1000)
            deserialized_route["tourStops"][tour_stop]["images"][image] = presigned_url
    
        parameters["Key"] = path.join("audio", current_stop["audioFile"])
        presigned_url_audio = generate_presigned_url(s3, 'get_object', parameters, 1000)
        deserialized_route["tourStops"][tour_stop]["audioFile"] = presigned_url_audio
    return deserialized_route
    
def handler(event, context):
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

        route = db_response['Item']
        #print(document)
        deserialized_route = {k: deserializer.deserialize(v) for k, v in route.items()}
        response_body = generate_presigned_urls_for_route(deserialized_route)
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

