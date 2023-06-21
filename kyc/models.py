import json
import os

from django.conf import settings
from django.db import models

from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.User import User
from kyc.utils import encode_photo, detect_name, detect_texts


def upload_photo_id(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users/id/', name)


def upload_photo_id_back(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users/id/', name)


def upload_selfie(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users/selfie/', name)


def upload_template_id(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('companies/id/', name)


class UserID(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ids')
    template = models.ForeignKey('kyc.TemplateID', null=True, blank=True, on_delete=models.CASCADE)
    photo_id = models.ImageField(upload_to=upload_photo_id, null=True, blank=True)
    photo_id_back = models.ImageField(upload_to=upload_photo_id_back, default="")
    selfie = models.ImageField(upload_to=upload_selfie, null=True, blank=True)
    verified = models.BooleanField(default=False)
    encoded = models.JSONField(null=True)

    def encode_photo(self):
        if settings.IS_PRODUCTION:
            self.encoded = encode_photo(self.photo_id.url)
        else:
            self.encoded = encode_photo(self.photo_id.path)
        self.save()

    def detect_name_id(self, template):
        image_path = ''
        if settings.IS_PRODUCTION:
            image_path = self.photo_id.url
        else:
            image_path = self.photo_id  # REMOVED .path
        return detect_name(image_path, template)

    def __str__(self):
        return self.user.get_full_name()


class TemplateID(models.Model):
    template_name = models.CharField(max_length=64)
    template_id = models.ImageField(upload_to=upload_template_id)
    institute_name = models.CharField(max_length=128)
    institute = models.CharField(max_length=32)
    # first_name = models.CharField(max_length=32)
    # last_name = models.CharField(max_length=32)

    def locate_texts(self, fields):
        if settings.IS_PRODUCTION:
            texts = detect_texts(self.template_id.url)
        else:
            texts = detect_texts(self.template_id.path)

        for key, value in fields.items():
            index = []
            if key == 'institute':
                for w in value.split(' '):
                    index.append(texts.index(w.lower()))
                self.institute = json.dumps(index)
                self.institute_name = value
            # elif key == 'first_name':
            #     for w in value.split(' '):
            #         index.append(texts.index(w.lower()))
            #     self.first_name = json.dumps(index)
            # elif key == 'last_name':
            #     for w in value.split(' '):
            #         index.append(texts.index(w.lower()))
            #     self.last_name = json.dumps(index)

        self.save()

    def __str__(self):
        return self.template_name
