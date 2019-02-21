Qualys log export to AWS Kinesis Firehose

maintainer: Frank Dooling (fdooling@csico.com)

Lambda function that creates a Kinesis Firehose log stream and integrates
with the Qualys API using the requests module.  Log files are retrieved via
HTTP GET and delivered to log stream using direct PUT.  Log files are sent
to S3

roleTrustRelationship.json needs to be attached to the IAM role in order
for lambda and firehose to assume the role
