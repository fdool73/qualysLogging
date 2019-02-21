#export Qualys logs to AWS Kinesis Firehose stream
#set username and password as lambda environment variables (encrypted at rest)

import boto3
from botocore.vendored import requests
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

headers = {
    'X-Requested-With':'Qualys API',
    }

login = {
  'action':'login',
  'username':os.environ['username'],
  'password':os.environ['password']
}

session = requests.Session()
r = session.post('https://qualysapi.qg3.apps.qualys.com/api/2.0/fo/session/', headers=headers, data=login)

logExport = session.get('https://qualysapi.qg3.apps.qualys.com/api/2.0/fo/activity_log?action=list', headers=headers)

#send to existing Kinesis Firehose stream
def lambda_handler(event, context):
    client = boto3.client('firehose', region_name='us-east-1')
    response=client.put_record(
        DeliveryStreamName='qualysLogs',
        Record={
            'Data': logExport.text
        }
    )
