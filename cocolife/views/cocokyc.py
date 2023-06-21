import base64
import os
import logging
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers.KYCSerializer import TemplateIDSerializer, AvatarSelfieSerializer, PostIdandSelfieKycSerializer

from rest_framework.generics import RetrieveUpdateAPIView

from django.shortcuts import get_object_or_404

from kyc.models import TemplateID
from cocolife.models.DigiKYC import DigiUserID
from cocolife.serializers.DigiKYCSerializer import DigiUpdateKYC
from kyc.utils import compare_photo, check_details
from rest_framework import status
from cocolife.models.DigiInsuree import DigiInsuree

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

logger = logging.getLogger('api.views')

__all__ = ['CLKycHandler', 'TemplateIDViewSet', 'AvatarSelfie']

MAGPIE_FEE = 0.039


class CLKycHandler(RetrieveUpdateAPIView):
    queryset = DigiUserID.objects.all()
    lookup_field = 'user_id'
    serializer_class = DigiUpdateKYC

    def setToNone(self, user_id):
        user_id.selfie = None
        user_id.photo_id = None
        user_id.photo_id_back = None
        user_id.encoded = None
        user_id.verified = False
        user_id.template = None
        return user_id.save()

    def put(self, request, user_id):

        user = get_object_or_404(DigiInsuree, user_id=user_id)

        try:
            user_id, created = DigiUserID.objects.update_or_create(user=user)

            # TODO - Checks if there is existing data.
            # if user_id.selfie and user_id.photo_id and user_id.photo_id_back:
            #     return Response("Please update instead.", status=status.HTTP_400_BAD_REQUEST)

            # Get Data from Request
            template_id = request.data.get('template_id')
            selfie_img_data = request.data.get('selfie')
            id_front_img_data = request.data.get('photo_id')
            id_back_img_data = request.data.get('photo_id_back')

            # Template Validation from Request
            if template_id:
                # Check if sent template exist from db
                try:
                    template = TemplateID.objects.get(
                        id=request.data.get('template_id'))
                except TemplateID.DoesNotExist:
                    return Response("Template not Found", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Template is Required', status=status.HTTP_400_BAD_REQUEST)

            # Validate if ID for both Front and Back Exist
            # remove this if block when production
            if request.query_params.get('validate') == "off":
                # Get Base64 String
                front_format, front_imgstr = id_front_img_data.split(
                    ';base64,')
                # Get Image Extension
                front_ext = front_format.split('/')[-1]
                front_img_id = base64.b64decode(front_imgstr)
                front_photo_id = ContentFile(
                    front_img_id, name='front_id_photo_%s.%s' % (user.user_id, front_ext))

                # Back ID
                back_format, back_imgstr = id_back_img_data.split(';base64,')
                back_ext = back_format.split('/')[-1]
                back_img_id = base64.b64decode(back_imgstr)
                back_photo_id = ContentFile(
                    back_img_id, name='back_id_photo_%s.%s' % (user.user_id, back_ext))
            else:
                if id_front_img_data and id_back_img_data:
                    # Get Base64 String
                    front_format, front_imgstr = id_front_img_data.split(
                        ';base64,')
                    # Get Image Extension
                    front_ext = front_format.split('/')[-1]
                    front_img_id = base64.b64decode(front_imgstr)
                    front_photo_id = ContentFile(
                        front_img_id, name='front_id_photo_%s.%s' % (user.user_id, front_ext))

                    # Back ID
                    back_format, back_imgstr = id_back_img_data.split(
                        ';base64,')
                    back_ext = back_format.split('/')[-1]
                    back_img_id = base64.b64decode(back_imgstr)
                    back_photo_id = ContentFile(
                        back_img_id, name='back_id_photo_%s.%s' % (user.user_id, back_ext))
                else:
                    return Response("ID Photo is Required", status=status.HTTP_400_BAD_REQUEST)

            # Validate if Selfie image exist from Request
            # remove this if block when production
            if request.query_params.get('validate') == "off":
                format, imgstr = selfie_img_data.split(';base64,')
                ext = format.split('/')[-1]
                img = base64.b64decode(imgstr)
                selfie = ContentFile(img, name='selfie_%s.%s' %
                                     (user.user_id, ext))
            else:
                if selfie_img_data:
                    format, imgstr = selfie_img_data.split(';base64,')
                    ext = format.split('/')[-1]
                    img = base64.b64decode(imgstr)
                    selfie = ContentFile(img, name='selfie_%s.%s' %
                                         (user.user_id, ext))
                else:
                    return Response("Selfie is required", status=status.HTTP_400_BAD_REQUEST)

            # if not (selfie_img_data and id_front_img_data and id_back_img_data):
            #     return Response("Input is required", status=status.HTTP_400_BAD_REQUEST)

            # Save Fields to UserID Instance
            user_id.selfie = selfie
            user_id.photo_id = front_photo_id
            user_id.photo_id_back = back_photo_id
            #user_id.verified = False
            user_id.template = template
            user_id.save()
            user_id.encode_photo()
            insuree = user

            filename = os.path.join(BASE_DIR, 'tmp\%d' % user.user_id)

            with open(filename, 'wb') as f:
                f.write(img)

            # FIX INDENTION BY 1 WHEN VALIDATION RESUMES
            names = []
            for fname in insuree.first_name.lower().split(' '):
                names.append(fname)
            for lname in insuree.last_name.lower().split(' '):
                names.append(lname)

            # Validate ID Photos; ID type, and ID name matches Template and Profile
            if settings.IS_PRODUCTION:
                validity = check_details(
                    user_id.photo_id.url, template.institute_name, names)
            else:
                validity = check_details(
                    user_id.photo_id.path, template.institute_name, names)

            # remove this if block when production
            if request.query_params.get('validate') == "off":
                validity = True

            if validity is not True:
                if (validity == "WRONG_ID"):
                    # Sets Images to Null for Failed Validation
                    self.setToNone(user_id)
                    return Response({
                        'status': 'fail',
                        'code': 3,
                        'message': 'The identification card that was uploaded does not match the type selected'
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.setToNone(user_id)
                    return Response({
                        'status': 'fail',
                        'code': 4,
                        'message': 'Name detected in ID does not match the name in your profile. Please update your profile or upload a different ID.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            # Proceed to Validating Selfie once ID passed
            else:
                filename = os.path.join(BASE_DIR, 'tmp\%d' % user.user_id)

                with open(filename, 'wb') as f:
                    f.write(img)

                try:
                    # Compare ID Photo and Selfie
                    result = compare_photo(user_id.encoded, filename)

                    # remove this if block when production
                    if request.query_params.get('validate') == "off":
                        result = True

                    if not result:
                        self.setToNone(user_id)
                        logger.exception('Comparison failed')

                        return Response({
                            'status': 'fail',
                            'code': 8,
                            'message': 'Photo in ID did not match the selfie. Please upload a clearer photo ID or retake selfie.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                except IndexError as e:
                    self.setToNone(user_id)
                    logger.exception(e)

                    return Response({
                        'status': 'fail',
                        'code': 7,
                        'message': 'Error detecting face on image. Please retake your photo.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                except Exception as e:
                    self.setToNone(user_id)
                    logger.exception(e)

                    return Response({
                        'status': 'fail',
                        'code': 6,
                        'message': 'An error occurred. Please try again.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # When Validation passes, proceed to save instance
            user_id.verified = True
            user_id.save()
            os.remove(filename)

            # Original Response, but causes code below to be unreachable
            """ return Response({
                'status': 'success',
                'message': 'You can now continue with your enrollment.'
            }) """

            context = {
                'status': 'success',
                'message': 'Successfully matched name in ID with profile.'
            }

            return Response(context)

        # UNCOMMENT WHEN VALIDATION RESUMES
        # End of Try Except for ID
        except IndexError as e:
            self.setToNone(user_id)
            logger.exception(e)

            return Response({
                'status': 'fail',
                'code': 5,
                'message': 'Error detecting face in ID. Please upload a clearer photo.'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.setToNone(user_id)
            logger.exception(e)

            return Response({
                'status': 'fail',
                'code': 2,
                'message': 'Error uploading ID'
            }, status=status.HTTP_400_BAD_REQUEST)


class TemplateIDViewSet(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = TemplateID.objects.all()
    serializer_class = TemplateIDSerializer


class AvatarSelfie(generics.ListAPIView):
    serializer_class = AvatarSelfieSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return DigiUserID.objects.filter(user=user_id)
