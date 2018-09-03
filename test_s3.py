import boto3

# Create S3
s3 = boto3.client('s3')

bucket_name = 'test-bucket-boto-mzol'
print('Creating new bucket with name: Test-Bucket-boto-mzol')
s3.create_bucket(Bucket=bucket_name)

# upload file
filename = 'text'
print('Uploading some data to {} file: {}'.format(bucket_name, filename))
s3.upload_file(filename, bucket_name, filename)

# read file from S3
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
obj = bucket.Object(filename)
print('Object body: {}'.format(obj.get()['Body'].read()))

# Delete all objects in S3
print('\nDeleting all objects in bucket {}.'.format(bucket_name))
bucket.objects.all().delete()

# remove S3
print('\nDeleting the bucket.')
bucket.delete()

print('\nThe bucket {} has benn deleted'.format (bucket_name))
