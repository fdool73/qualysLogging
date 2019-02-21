#export Qualys logs to AWS Kinesis Firehose stream
#create and put to Kinesis Firehose stream (S3)


#future vars: IAM role arn, S3 bucket arn, Lambda arn


import boto3
from botocore.vendored import requests
import logging
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

username = "cscsy3fd"
password = "Gotohellqualys1!"

headers = {
    'X-Requested-With':'Qualys API Test',
    }

login = {
  'action':'login',
  'username':username,
  'password':password
}

session = requests.Session()
r = session.post('https://qualysapi.qg3.apps.qualys.com/api/2.0/fo/session/', headers=headers, data=login)

logExport = session.get('https://qualysapi.qg3.apps.qualys.com/api/2.0/fo/activity_log?action=list', headers=headers)

#create and send to Kinesis Firehose stream
def lambda_handler(event, context):
    client = boto3.client('firehose', region_name='us-east-1')
    response=client.create_delivery_stream(
        DeliveryStreamName='qualysLogs',
        DeliveryStreamType='DirectPut',
        ExtendedS3DestinationConfiguration={
            'RoleARN': 'arn:aws:iam::137453691370:role/qualysFirehose',
            'BucketARN': 'arn:aws:s3:::qualys-logs-export',
            'Prefix': 'qualysLog/',
            'ProcessingConfiguration': {
            'Enabled': True,
            'Processors': [
                {
                    'Type': 'Lambda',
                    'Parameters': [
                        {
                            'ParameterName': 'LambdaArn',
                            'ParameterValue': 'arn:aws:lambda:us-east-1:137453691370:function:qualysLogTransformSyslogToCsv'
                        },
                    ]
                },
            ]
        },
            },
    ),
    time.sleep(90)
    response2=client.put_record(
        DeliveryStreamName='qualysLogs',
        Record={
            'Data': logExport.text
        }
    )
