#create Kinesis Firehose stream for Qualys logs (S3)
#future vars: IAM role arn, S3 bucket arn, Lambda arn

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    )
