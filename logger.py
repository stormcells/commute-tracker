import json
import boto3
import os
import datetime

def lambda_handler(event, context):
    print('From SNS: ', event)
    message = event['Records'][0]['Sns']['Message']
    message = message.replace("'", "\"")
    
    print('Message: ', message)
    # print(type(message))
    message = json.loads(message)
    # print('message dictionary: ', message)
    
    date = message.get("Date")
    hour = message.get("Hour")
    duration = message.get("Duration")
    origin = message.get("origin")
    target = message.get("target")
    
    dynamodb = boto3.resource('dynamodb')
    
    table = ''
    if os.environ['HOME'] in origin:
        print('MorningCommute')
        table = dynamodb.Table('MorningCommute2')
    else:
        print('EveningCommute')
        table = dynamodb.Table('EveningCommute2')
        
    todayInt = datetime.datetime.today() - datetime.timedelta(hours=4)
    print('todayInt: ', todayInt)
    
    today = todayInt.strftime('%A')
    print('today: ', today)
    
    if os.environ['DB_ENABLED'] == 'TRUE':
        table.put_item(Item={
            'Date': date,
            'Hour': hour,
            'Day': today,
            'Duration': duration
        })
    else:
        print('Would have logged')
        
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed')
    }
