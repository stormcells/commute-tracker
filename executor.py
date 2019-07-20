import json
from botocore.vendored import requests
import os
import datetime
import boto3

def lambda_handler(event, context):
    print('From SNS: ', event)
    message = event['Records'][0]['Sns']['Message']
    message = message.replace("'", "\"")
    print('Message: ', message)
    print('Message type: ', type(message))

    message = json.loads(message)
    print('message dictionary: ', message)

    starting = message.get("origin")
    print('origin: ', starting)
    
    target = message.get("target")
    print('target: ', target)
    
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = dict(
        origin=starting,
        destination=target,
        departure_time='now',
        trafficModel='bestguess',
        key=os.environ['GMAPS_API_KEY']
    )
    
    print('params: ', params)

    response = requests.get(url=url, params=params)
    data = response.json()
    
    print(data)
    
    driving_time = data['routes'][0]['legs'][0]['duration_in_traffic']['text']
    print('Driving time = ', driving_time)

    distance = data['routes'][0]['legs'][0]['distance']['text']
    print('Distance = ' + distance)
    
    time_dist = {}
    time_dist['driving_time'] = driving_time
    time_dist['distance'] = distance

    respond = json.dumps(time_dist)
    
    now = datetime.datetime.now() - datetime.timedelta(hours=4)
    d = now.strftime("%Y-%m-%d")
    h = now.strftime("%H:%M:%S")

    print('hour: ', h)
    print('Current date: ', d)
    
    if os.environ['SNS_ENABLED'] == 'TRUE':
        entry = {
            'Date': d,
            'Hour': h,
            'Duration': driving_time,
            'origin': starting,
            'target': target
        }
        print('entry: ', entry)
        
        sns = boto3.client('sns')
        
        response = sns.publish(
            TopicArn=os.environ['TOPIC_ARN'],    
            Message=json.dumps(entry),    
        )

        # Print out the response
        print(response)
    else:
        response = 200
        print('Would have published to SNS')

    return {
        'statusCode': 200,
        'body': response
    }
