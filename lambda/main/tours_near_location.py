import boto3
from boto3.dynamodb.types import TypeDeserializer

import json
import sys

from get_route import generate_presigned_urls_for_route
from get_tour_stop import haversine

BUCKET = "history-tour-server-tourassetssbucketb8884501-1tv88uba51ic2"
TABLE = "HistoryTourServerAppStack-RouteTable64965DD4-1FJF389OM46QH"

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
deserializer = TypeDeserializer()

def handler(event, context):
    response_code = 200

    print("request: " + json.dumps(event))

    if (event["queryStringParameters"] and event["queryStringParameters"]["latitude"] and 
        event["queryStringParameters"]["longitude"]):
        current_lat = event["queryStringParameters"]["latitude"]
        current_lon = event["queryStringParameters"]["longitude"] 
        print("Received query: " + "lat : " + current_lat + "," + "lon: " + current_lon)

        response = dynamodb.scan(TableName=TABLE) 
        routes = response["Items"]


        closest_routes = {}
        for route in range(0,len (routes)):
            route_deserialized = {k: deserializer.deserialize(v) for k, v in routes[route].items()}
            distance_closest_tour_stop_on_route = sys.maxsize
            for tour_stop in range(0, len(route_deserialized["tourStops"])):
                stop_lat = float(route_deserialized["tourStops"][tour_stop]["gpsCoordinates"]["latitude"])
                stop_lon = float(route_deserialized["tourStops"][tour_stop]["gpsCoordinates"]["longitude"])
                distance = haversine(stop_lat,stop_lon,current_lat,current_lon)
                
                if distance_closest_tour_stop_on_route > distance:
                    distance_closest_tour_stop_on_route = distance
                
                route_name = route_deserialized["routeName"]
                closest_routes[route_name] = distance_closest_tour_stop_on_route

        top_three_routes = sorted(closest_routes.items(), key=lambda x: x[1])[:3]
        result = []
        for k,v in top_three_routes:
            db_response = dynamodb.get_item(
                    TableName = TABLE,
                    Key={
                        'routeName': {'S': k}
                    }
                )
            db_response_d = {k: deserializer.deserialize(v) for k, v in db_response['Item'].items()}
            generate_presigned_urls_for_route(db_response_d)
            result.append(db_response_d)        
        response_body = {"routes_nearby": result}
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