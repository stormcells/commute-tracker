import json
import boto3
import datetime

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb',)
    table = dynamodb.Table('EveningCommute2')
    response = table.scan()
    
    # print('response type: ', type(response))
    print('response size: ', len(response))
    # print(response.values())
    
    data = response['Items']
    # print('data type: ', type(data))
    # print(data)
    
    while response.get('LastEvaluatedKey'):
        print('Getting data')
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    # print('retrieved entries: ', len(data))
    # print('data type: ', type(data))
    # one = data[0]
    # print('Element 1: ', one)
    # print('Element 1 type: ', type(one))
    # vals = list(one.values())
    # print('val one: ', vals[0])

    string = "Date (S),Day (S),Hour (S),Duration (S)\n"
    
    for entry in data:
        values = list(entry.values())
        
        date    = values[0]
        day     = values[1]
        hour    = values[2]
        mins    = values[3]
        
        row     = str(date) + ','
        row     += str(day) + ','
        row     += str(hour) + ','
        row     += str(mins) + '\n'
        
        string += row 
    
    print(string[0:500])
    
    now = datetime.datetime.today() - datetime.timedelta(hours=4)
    date = now.strftime("%Y-%m-%d-%I:%M:%S")
    file = "evening-commute/{}.csv".format(date)
    print(file)

    s3 = boto3.resource('s3')
    object = s3.Object('commuting-data', file)
    object.put(Body=string)
    # object.put(Body=json.dumps(data))

    return {
        'statusCode': 200,
        'body': string
    }
