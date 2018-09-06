# Test-Python-boto
#################################################################################
### Library dependencies for the python code.  You need to install these with ###
### `pip install -r requirements.txt` before you can run this code            ###
#################################################################################

This script is:
	* create S3 bucket in aws
	* upload file to bucket
	* read this file from S3
	* delete bucket

Logging is implemented using module "logging". 
The script accepts an argument file in the yaml format with the level and type of logging

Example for Ubuntu:
	python3 test_s3.py -f log.yaml
