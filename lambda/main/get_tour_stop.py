import boto3
from boto3.dynamodb.types import TypeDeserializer

import json
from os import path
import sys
from math import radians, cos, sin, asin, sqrt

from get_route import generate_presigned_url

BUCKET = "history-tour-server-tourassetssbucketb8884501-1tv88uba51ic2"
TABLE = "HistoryTourServerAppStack-RouteTable64965DD4-1FJF389OM46QH"

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
deserializer = TypeDeserializer()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371.0088 * 0.621371192 
    return c * r

def generate_presigned_url_tour_stop(tour_stop):
     parameters = { "Bucket": BUCKET }

     for image in range(0,len(tour_stop["images"])):
            parameters["Key"] = path.join("images", tour_stop["images"][image])
            presigned_url = generate_presigned_url(s3, 'get_object', parameters, 1000)
            tour_stop["images"][image] = presigned_url
    
     parameters["Key"] = path.join("audio", tour_stop["audioFile"])
     presigned_url_audio = generate_presigned_url(s3, 'get_object', parameters, 1000)
     tour_stop["audioFile"] = presigned_url_audio

def handler(event, context):
    route_name = ""
    response_code = 200

    print("request: " + json.dumps(event))

    if (event["queryStringParameters"] and event["queryStringParameters"]["routeName"]):
        print("Received query: " + event["queryStringParameters"]["routeName"])
        route_name = event["queryStringParameters"]["routeName"]

    if (event["queryStringParameters"] and event["queryStringParameters"]["latitude"] and 
        event["queryStringParameters"]["longitude"]):
        lat = event["queryStringParameters"]["latitude"]
        lon = event["queryStringParameters"]["longitude"] 
        print("Received query: " + "lat : " + lat + "," + "lon: " + lon )

        db_response = dynamodb.get_item(
            TableName = TABLE,
            Key={
                'routeName': {'S': route_name}
            }
        )

        route = db_response['item']
        deserialized_route = {k: deserializer.deserialize(v) for k, v in route.items()}

        for tour in range(0, len(deserialized_route["tourStops"])):
            tour_coordinates = deserialized_route["tourStops"][tour]["gpsCoordinates"]
            min_distance = sys.maxsize
            min_distance_index = 0

            center_lat = float(tour_coordinates["latitude"])
            center_lon = float(tour_coordinates["longitude"])
            distance = haversine(center_lat,center_lon,lat,lon)

            if (min_distance > distance):
                min_distance = distance
                min_distance_index = tour
        
        closest_tour = deserialized_route["tourStops"][min_distance_index]
        generate_presigned_url_tour_stop(closest_tour)

        response_body = closest_tour
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