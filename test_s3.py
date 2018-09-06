import boto3
import sys
import logging
import argparse
import yaml

bucket_name = 'test-bucket-boto-mzol'
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
s3 = boto3.client('s3')


def create_s3(bucket_name, logger):
    """Create S3"""
    logger.info("Creating new bucket with name: {}".format(bucket_name))
    s3.create_bucket(Bucket=bucket_name)


def upload_file_to_S3(filename, bucket_name, logger):
    """upload file"""
    logger.info("Uploading data to {} file: {}".format(bucket_name, filename))
    s3.upload_file(filename, bucket_name, filename)


def read_file_s3(filename, bucket_name, logger):
    """read file from S3"""
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(bucket_name)
    obj = bucket.Object(filename)
    logger.info('Object body: {}'.format(obj.get()['Body'].read()))


def delete_s3(bucket_name, logger):
    """remove S3"""
    logger.info('Deleting all objects in bucket {}'.format(bucket_name))
    bucket.objects.all().delete()
    logger.info('Deleting the bucket')
    bucket.delete()
    logger.info('The bucket {} has benn deleted'.format(bucket_name))


def init_logging(level, type):
    """init logging"""
    obj = {
        "STD_OUT": sys.stdout
    }
    logger = logging.getLogger("MyLog-S3")
    ch = logging.StreamHandler(obj[str(type).upper()])
    logger.setLevel(logging.getLevelName(level))
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ch.setFormatter(logging.Formatter(format))
    logger.addHandler(ch)
    return logger


def init_parser():
    """init parser for yaml file"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r'))
    args = parser.parse_args()
    with args.file as logconfig:
        try:
            parser = yaml.safe_load(logconfig)
        except yaml.YAMLError as exc:
            print(exc)
    return parser


def main(args):
    parser = init_parser()
    type = parser["type"]
    level = str(parser["level"]).upper()
    logger = init_logging(level, type)
    create_s3(bucket_name, logger)
    upload_file_to_S3("text", bucket_name, logger)
    read_file_s3("text", bucket_name, logger)
    delete_s3(bucket_name, logger)


if __name__ == "__main__":
    main(sys.argv)
