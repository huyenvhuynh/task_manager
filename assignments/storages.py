# this file allows uploaded files to not get sent to the default storage (which is currently local storage) and instead get sent to the S3 bucket
from storages.backends.s3boto3 import S3Boto3Storage

class AssignmentStorage(S3Boto3Storage):
    location = 'assignments' 
    file_overwrite = False 