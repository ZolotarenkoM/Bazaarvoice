import boto3
import sys
import logging

# Create logger
logger = logging.getLogger("MyLog-S3")
logger.setLevel(logging.DEBUG)
# create the logging handlers (file and stream)
fh = logging.FileHandler("test_s3.log", mode='w')
ch = logging.StreamHandler(stream=sys.stdout)
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

# Create S3
s3 = boto3.client('s3')
bucket_name = 'test-bucket-boto-mzol'
logger.info("Creating new bucket with name: {}".format(bucket_name));
s3.create_bucket(Bucket=bucket_name)

# upload file
filename = 'text'
logger.info("Uploading some data to {} file: {}".format(bucket_name, filename))
s3.upload_file(filename, bucket_name, filename)

# read file from S3
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
obj = bucket.Object(filename)
logger.info('Object body: {}'.format(obj.get()['Body'].read()))

# Delete all objects in S3
logger.info('Deleting all objects in bucket {}'.format(bucket_name))
bucket.objects.all().delete()

# remove S3
logger.info('Deleting the bucket')
bucket.delete()
logger.info('The bucket {} has benn deleted'.format (bucket_name))
