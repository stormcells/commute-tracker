import json
import datetime
import boto3
import os

def lambda_handler(event, context):
    now = datetime.datetime.now() - datetime.timedelta(hours=4)
    hour = int(now.strftime('%H'))
    print('hour: ', hour)
    
    home = os.environ['HOME']
    work = os.environ['WORK']
    data = {}
    
    if hour <= 12:
        # Morning Commute
        print('AM')
        data['origin'] = home
        data['target'] = work
    else:
        # Evening Commute
        print('PM')
        data['origin'] = work
        data['target'] = home

    message = json.dumps(data)
    print('message', message)
    
    # Create an SNS client
    sns = boto3.client('sns')

    if os.environ['SNS_ENABLED'] == 'TRUE':
        # Publish a message to the SNS topic
        response = sns.publish(
            TopicArn=os.environ['TOPIC_ARN'],    
            Message=message,    
        )

        # Print out the response
        print('response: ', response)
    
        code = response['ResponseMetadata']['HTTPStatusCode']
        code = int(code)
    
        return {
            'statusCode': code,
            'body': json.dumps(response)
        }
    else:
        print('SNS disabled')
        return {
            'statusCode': 200,
            'body': 'SNS disabled'
        }
