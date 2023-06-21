import base64
import logging
import os
import tempfile
from pathlib import Path


from django.conf import settings
from django.core.files.base import ContentFile

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import TemplateIDSerializer

from digiinsurance.models import Insuree, User

from kyc.models import TemplateID, UserID
from kyc.utils import compare_photo, check_details
from django.http.response import JsonResponse

from  api.serializers import UpdateSelfieSerializer, UpdatePhoto_idSerializer
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

logger = logging.getLogger('api.views')

__all__ = ['UpdateID','UpdateSelfie']

MAGPIE_FEE = 0.039

class UpdateID(CreateAPIView):
    queryset = UserID.objects.all()
    serializer_class = UpdatePhoto_idSerializer
    def post(self, request, user_id):
        user = User.objects.get(id = user_id)
        # user = request.user
        try:
            template = TemplateID.objects.get(
                id=request.data.get('template_id')
            )
            user_id, created = UserID.objects.update_or_create(user=user)

            id_img_data_front = request.data.get('id_image_front')
            id_img_data_back = request.data.get('id_image_back')
            if id_img_data_front and id_img_data_back:
                format_front, imgstr_front = id_img_data_front.split(';base64,')
                ext_front = format_front.split('/')[-1]
                format_back, imgstr_back = id_img_data_back.split(';base64,')
                ext_back = format_back.split('/')[-1]

                img_id_front = base64.b64decode(imgstr_front)
                img_id_back = base64.b64decode(imgstr_back)

                photo_id_front = ContentFile(img_id_front, name='photo_ID_%s.%s' % (user.id, ext_front))
                photo_id_back = ContentFile(img_id_back, name='photo_ID_%s.%s' % (user.id, ext_back))

            else:
                msg = _('ID photo is required.')
                return JsonResponse(msg)

            user_id.photo_id = photo_id_front
            user_id.photo_id_back = photo_id_back
            user_id.template = template
            user_id.save()
            user_id.encode_photo()
            insuree = user.insuree

            names = []
            for fname in insuree.first_name.lower().split(' '):
                names.append(fname)
            for lname in insuree.last_name.lower().split(' '):
                names.append(lname)

            if settings.IS_PRODUCTION:
                validity = check_details(
                    user_id.photo_id.url, template.institute_name, names
                )
            else:
                validity = check_details(
                    user_id.photo_id.path, template.institute_name, names
                )

            if validity is not True:
                if (validity == "WRONG_ID"):
                    return Response({
                        'status':'fail',
                        'code':3,
                        'message':'The identification card uploaded does not match the type selected.'
                    })
                else:
                    return Response({
                        'status':'fail',
                        'code':4,
                        'message':'Name detected in ID does not match name in your profile. Please update your profile or upload a different ID.'
                    })
            else:
                context = {
                    'status':'success',
                    'message':'You can now proceed to shopping.'
                }
                return Response(context)

        except IndexError as e:
            logger.exception(e)

            return Response({
                'status': 'fail',
                'code': 5,
                'message': 'Error detecting face in ID. Please upload a clearer photo.'
            })

        except Exception as e:
            logger.exception(e)

            return Response({
                'status': 'fail',
                'code': 2,
                'message': 'Error uploading ID'
            })

class UpdateSelfie(CreateAPIView):
    queryset = UserID.objects.all()
    serializer_class = UpdateSelfieSerializer
    def post(self, request, user_id):
        user = User.objects.get(id = user_id)
        # user =request.user

        try:
            user_id, created = UserID.objects.update_or_create(user=user)

            selfie_img_data = request.data.get('selfie_image')
            if selfie_img_data:
                format, imgstr = selfie_img_data.split(';base64,')
                ext = format.split('/')[-1]
                img = base64.b64decode(imgstr)
                selfie = ContentFile(img, name='selfie_%s.%s' % (user.id, ext))
                user_id.selfie = selfie

            else:
                msg = _('Selfie photo is required.')
                return JsonResponse(msg)

            user_id.save()


        except IndexError as e:
            logger.exception(e)

            return Response({
                'status': 'fail',
                'code': 5,
                'message': 'Error detecting face in ID. Please upload a clearer photo.'
            })

        except Exception as e:
            logger.exception(e)

            return Response({
                'status':'fail',
                'code':2,
                'message':'Error in uploading selfie!'
            })

        filename = os.path.join(BASE_DIR, 'tmp\%d' % user.id)
        if selfie_img_data:
            with open(filename, 'wb') as f:
                f.write(img)

            try:
                result = compare_photo(user_id.encoded, filename)
            except IndexError as e:
                logger.exception(e)

                return Response({
                    'status':'fail',
                    'code':6,
                    'message':'An error occurred. Please try again!'
                })

            if not result:
                logger.exception('Comparison failed')

                return Response({
                    'status':'fail',
                    'code':8,
                    'message':'Photo ID did not match the selfie. Please upload a clearer photo ID or retake selfie.'
                })

            os.remove(filename)

            return Response({
                'status':'success',
                'message':'You can now continue with your shopping.'
            })

            context = {
                'status':'success',
                'message':'Successfully matched name in ID and profile.'
            }

            return Response(context)
