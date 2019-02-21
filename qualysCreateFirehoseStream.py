#create Kinesis Firehose stream for Qualys logs (S3)
#future vars: IAM role arn, S3 bucket arn, Lambda arn

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    client = boto3.client('firehose', region_name='us-east-1')
    response=client.create_delivery_stream(
        DeliveryStreamName='streamName',
        DeliveryStreamType='DirectPut',
        ExtendedS3DestinationConfiguration={
            'RoleARN': 'arn',
            'BucketARN': 'arn',
            'Prefix': 'qualysLog/',
            'ProcessingConfiguration': {
            'Enabled': True,
            'Processors': [
                {
                    'Type': 'Lambda',
                    'Parameters': [
                        {
                            'ParameterName': 'LambdaArn',
                            'ParameterValue': 'arn'
                        },
                    ]
                },
            ]
        },
            },
    )
