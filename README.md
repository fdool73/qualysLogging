Qualys log export to AWS Kinesis Firehose

Maintainer: Frank Dooling (fdooling@cisco.com)

Two Lambda functions,  qualysCreateFirehoseStream.py creates a Kinesis Firehose
log stream and qualysLogExport.py which integrates with the Qualys API using the
requests module.  Log files are retrieved via HTTP GET, transformed into
CSV using Lambda blueprint and delivered to log stream using direct PUT.
Log files are sent to S3

roleTrustRelationship.json needs to be attached to the IAM role in order 
for lambda and firehose to assume the role
