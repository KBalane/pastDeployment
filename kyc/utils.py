import boto3
import face_recognition
import json
import io
import urllib.request

from django.conf import settings


def get_s3_session():
    return boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def get_s3_client():
    """A client object is used to access boto3 low-level
       interface (close to 1:1 map with AWS API)"""
    session = get_s3_session()
    return session.client('s3')


def get_s3_resource():
    """A resource object is used to access boto3 high-level objects
      (easier to work with than client but less powerful)"""
    session = get_s3_session()
    return session.resource('s3')


def get_s3_bucket():
    s3 = get_s3_resource()
    return s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


def encode_photo(path):
    if settings.IS_PRODUCTION:
        photo_id = face_recognition.load_image_file(
            urllib.request.urlopen(path))
    else:
        photo_id = face_recognition.load_image_file(path)
    photo_encoding = face_recognition.face_encodings(photo_id)[0]

    return json.dumps(photo_encoding.tolist())


def compare_photo(encoded_id, path_captured):
    id_encoded = json.loads(encoded_id)

    captured_id = face_recognition.load_image_file(path_captured)
    # Throws uncaught Error when no face is detected, still works tho.
    captured_encoding = face_recognition.face_encodings(captured_id)[0]

    results = face_recognition.compare_faces(
        [id_encoded], captured_encoding, tolerance=0.4)  # Documentation recommends 0.6

    return results[0]


def detect_texts(image_path):
    import re
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    if settings.IS_PRODUCTION:
        content = urllib.request.urlopen(image_path)
        image = vision.types.Image(content=content.read())
    else:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return [word.lower() for word in re.findall(r'\w+', texts[0].description)]


def check_details(image_path, institute, names):
    words = detect_texts(image_path)
    if not set(institute.lower().split()).issubset(words):
        return "WRONG_ID"

    for name in names:
        if name in words:
            pass
        else:
            return "WRONG_NAME"
    return True


def detect_name(image_path, template):
    texts = detect_texts(image_path.path)
    details = {}
    institute = ''
    first_name = ''
    last_name = ''

    for index in json.loads(template.institute):
        institute += texts[index]
    for index in json.loads(template.first_name):
        first_name += texts[index]
    for index in json.loads(template.last_name):
        last_name += texts[index]

    details['institute'] = institute
    details['first_name'] = first_name
    details['last_name'] = last_name

    return details
