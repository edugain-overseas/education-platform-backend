# from io import BytesIO
#
# import boto3
# from fastapi import UploadFile
#
# from app.setting import (AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY,
#                          AWS_BUCKET_NAME)
#
# STUDENT_IMAGE_FOLDER = 'images/student_profile_photo/'
# SUBJECT_AVATAR_FOLDER = 'images/subject_main_photo/'
# SUBJECT_LOGO_FOLDER = 'images/subject_logo/'
#
#
# def get_s3_client():
#     s3_client = boto3.client(
#         "s3",
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_ACCESS_SECRET_KEY
#     )
#
#     return s3_client
#
#
# def get_bytes_image(file: UploadFile):
#     file_content = file.file.read()
#     return BytesIO(file_content)
#
#
# def save_images(file: UploadFile):
#     s3_client = get_s3_client()
#     bytes_file = get_bytes_image(file)
#     s3_client.put_object(
#         Body=bytes_file,
#         Bucket=AWS_BUCKET_NAME,
#         Key=SUBJECT_LOGO_FOLDER + file.filename
#     )
#
#     return SUBJECT_LOGO_FOLDER + file.filename
