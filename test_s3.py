import boto3
import sys
import logging
import argparse
import yaml

bucket_name = 'test-bucket-boto-mzol'
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
s3 = boto3.client('s3')

"""Create S3"""
def CreateS3(bucket_name,logger):
    logger.info("Creating new bucket with name: {}".format(bucket_name));
    s3.create_bucket(Bucket=bucket_name)

"""upload file"""
def UploadFiletoS3(filename, bucket_name,logger):
    logger.info("Uploading some data to {} file: {}".format(bucket_name, filename))
    s3.upload_file(filename, bucket_name, filename)

"""read file from S3"""
def ReadFileS3(filename, bucket_name,logger):
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(bucket_name)
    obj = bucket.Object(filename)
    logger.info('Object body: {}'.format(obj.get()['Body'].read()))

"""remove S3"""
def DeleteS3(bucket_name,logger):
    logger.info('Deleting all objects in bucket {}'.format(bucket_name))
    bucket.objects.all().delete()
    logger.info('Deleting the bucket')
    bucket.delete()
    logger.info('The bucket {} has benn deleted'.format(bucket_name))

"""init logging"""
def init_logging(level,type):
    obj = {
        "STD_OUT": sys.stdout
    }
    logger = logging.getLogger("MyLog-S3")
    ch = logging.StreamHandler(obj[str(type).upper()])
    logger.setLevel(logging.getLevelName(level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

"""init parser for yaml file"""
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='File to read config-log from ')
    args = parser.parse_args()
    with args.file as logconfig:
        cfg = yaml.safe_load(logconfig)
    return cfg

def main():
    cfg = init_parser()
    type = cfg["type"]
    level = str(cfg["level"]).upper()
    logger = init_logging(level,type)
    CreateS3(bucket_name,logger)
    UploadFiletoS3("text", bucket_name,logger)
    ReadFileS3("text",bucket_name,logger)
    DeleteS3(bucket_name,logger)

if __name__ == "__main__":
    main()
