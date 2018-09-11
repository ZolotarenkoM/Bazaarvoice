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
    """
    Create S3 bucket
    """

    logger.info("Creating new bucket with name: {}".format(bucket_name))
    s3.create_bucket(Bucket=bucket_name)


def upload_file_to_s3(filename, bucket_name, logger):
    """
    Upload file to S3 buccket
    """

    logger.info("Uploading data to {} file: {}".format(bucket_name, filename))
    s3.upload_file(filename, bucket_name, filename)


def read_file_s3(filename, bucket_name, logger):
    """
    Read file from S3 bucket
    """

    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(bucket_name)
    obj = bucket.Object(filename)
    logger.info('Object body: {}'.format(obj.get()['Body'].read()))


def delete_s3(bucket_name, logger):
    """
    Remove all objects in S3 bucket and the bucket itself
    """

    logger.info('Deleting all objects in bucket {}'.format(bucket_name))
    bucket.objects.all().delete()
    logger.info('Deleting the bucket')
    bucket.delete()
    logger.info('The bucket {} has been deleted'.format(bucket_name))


def init_logging(level_log, type_log):
    """
    Init logging for output messages.

    Args:
        level_log: this is value of logging level
        type_log: this is type of logging

    Returns:
        logger: loggers object
    """

    logger = logging.getLogger("MyLog-S3")
    handler = init_handler(type_log)
    logger.setLevel(logging.getLevelName(level_log))
    format_log = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handler.setFormatter(logging.Formatter(format_log))
    logger.addHandler(handler)
    return logger


def init_handler(type_log):
    """
    Init stream handler for logging

    Args:
        type_log: this is type of logging

    Returns:
        handler: this is stream (console) handler
    """

    list_output = {
        "STD_OUT": sys.stdout
    }
    handler = logging.StreamHandler(list_output[str(type_log).upper()])
    return handler


def init_parser():
    """
    Init and return parser for yaml file

    Returns:
        parser: this is parser for type file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r'))
    return parser


def init_args():
    """
    The function returns already parsed arguments

    Returns:
        args: this is a list of arguments
    """

    parser = init_parser()
    args = parser.parse_args()
    with args.file as logconfig:
        try:
            args = yaml.safe_load(logconfig)
        except yaml.YAMLError as exc:
            print(exc)
    return args


def main(args):
    type_log = args["type"]
    level_log = str(args["level"]).upper()
    logger = init_logging(level_log, type_log)
    create_s3(bucket_name, logger)
    upload_file_to_s3("text", bucket_name, logger)
    read_file_s3("text", bucket_name, logger)
    delete_s3(bucket_name, logger)


if __name__ == "__main__":
    main(init_args())
