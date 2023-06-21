import base64
import jwt
import json

from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.contrib.auth.models import update_last_login

from cocolife.models import Profile
from cocolife.signals import encryption, decryption
from digiinsurance.models import User
from api.utils import create_token

from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from datetime import datetime, timedelta

__all__ = [
            'SSOUserCreate', 'SSOObtainUserInfo',
           'SSOUpdateUserImage', 'SSOGenerateJWT',
           'SSOUserCreateV2', 'SSOUpdateUserFix']


class SSOUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middel_name = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField()
    birthdate = serializers.DateField()

    class Meta:
        model = User
        fields = ['email', 'middle_name', 'first_name',
                  'last_name', 'mobile_number', 'birthday']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'].split('@')[0],
            email=validated_data.get('email'),
            role='IN',
            is_verified=True,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            mobile_number=validated_data.get('mobile_number')
        )
        user.save()

        profile = Profile.objects.create(
            user=user,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            mobile_number=user.mobile_number,
            middle_name=validated_data.get('middle_name'),
            birthday=validated_data.get('birthday'),
            default_contact_info='email'
        )
        return profile


class SSOUserUpdateFIX(serializers.ModelSerializer):
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField()
    birthday = serializers.DateField()

    class Meta:
        model = User
        fields = 'middle_name', 'first_name', 'last_name', 'mobile_number', 'birthday'


class ObtainUserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)


class SSOUserSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username'

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('username') + 'digiinsurance@qymera.com',
            role='IN',
            is_verified=True
        )
        user.save()
        return user


class SSOUpdateUserImageSerializer(serializers.ModelSerializer):
    photo = serializers.CharField()

    class Meta:
        model = User
        fields = 'photo'

    def update(self, instance, validated_data):
        b64_photo = validated_data.pop('photo', None)
        if b64_photo:
            try:
                b64_format, b64_string = b64_photo.split(';base64,')
                ext = b64_format.split('/')[-1]
                b64_decoded_img = base64.b64decode(b64_string)
                photo = ContentFile(
                    b64_decoded_img,
                    name='profile_img_%s.%s' % (instance.id, ext)
                )
                instance.photo = photo
                instance.save()
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"photo": 'unable to upload image'})
            return instance


class SSOGenerateJWT(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.id != 4:
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = self.generate_jwt(user.id)
        return Response({'token': token}, status=status.HTTP_201_CREATED)

    @staticmethod
    def generate_jwt(id):
        payload = {
            'id': id,
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(hours=1)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class SSOUserCreate(GenericAPIView):
    permission_classes = AllowAny

    def post(self, request):
        token = request.data.get('token', None)
        is_valid = self.validate_jwt(token)

        if not is_valid:
            return Response('invalid token', status=status.HTTP_401_UNAUTHORIZED)

        serializer = SSOUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_jwt(token):
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return False

        if decode['id'] == 4:
            return True
        else:
            return False


class SSOUserCreateV2(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token', None)
        is_valid = self.validate_jwt(token)

        if not is_valid:
            return Response('invalid token', status=status.HTTP_401_UNAUTHORIZED)

        serializer = SSOUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_jwt(token):
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            print(e)
            return False
        if decode['id'] == 4:
            return True
        else:
            return False


class SSOUpdateUserImage(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = SSOUpdateUserImageSerializer

    def get_object(self):
        user = self.request.user
        return user


class SSOObtainUserInfo(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainUserInfoSerializer

    def post(self, request):
        if request.data.get('user') is None:
            decryptedData = {
                "token": request.data.get('token'),
                "user": {
                    "mobile_number": request.data.get("mobile_number"),
                    "first_name": request.data.get("first_name"),
                    "last_name": request.data.get("last_name"),
                    "middle_name": request.data.get("middle_name"),
                    "birthday": request.data.get("birthday"),
                }
            }
        else:
            now = datetime.now()
            user = request.data.get('user', None)
            if user.get('middle_name') is None:
                decryptedData = {
                    "token": request.data.get("token"),
                    "email": decryption.decrypt(request.data.get('email')),
                    "user": {
                        "email": decryption.decrypt(request.data.get("email")),
                        "mobile_number": decryption.decrypt(user.get("mobile_number")),
                        "first_name": decryption.decrypt(user.get("first_name")),
                        "last_name": decryption.decrypt(user.get("last_name")),
                        "middle_name": user.get("middle_name"),
                        "birthday": decryption.decrypt(user.get("birthday"))
                    }
                }
            else:
                decryptedData = {
                    "token": request.data.get("token"),
                    "email": decryption.decrypt(request.data.get('email')),
                    "user": {
                        "email": decryption.decrypt(request.data.get("email")),
                        "mobile_number": decryption.decrypt(user.get("mobile_number")),
                        "first_name": decryption.decrypt(user.get("first_name")),
                        "last_name": decryption.decrypt(user.get("last_name")),
                        "middle_name": decryption.decrypt(user.get("middle_name")),
                        "birthday": decryption.decrypt(user.get("birthday"))
                    }
                }
        serializer = self.get_serializer(data=decryptedData)
        serializer.is_valid(raise_exception=True)

        token = serializer.data.get('token')
        is_valid = self.validate_jwt(token)
        if not is_valid:
            return Response("invalid token", status=status.HTTP_401_UNAUTHORIZED)

        email = serializer.data.get('email')
        cl_core_user = decryptedData['user']

        if cl_core_user.get('first_name') is None:
            cl_core_user = request.data.get('user')

        print(cl_core_user)

        if not User.objects.filter(email=email).exists() and not cl_core_user:
            return Response({'pepperoni': 'user not found, please provide CL Core User'})

        if cl_core_user:
            dob = cl_core_user.pop('birthday')
            middle_name = cl_core_user.pop('middle_name', None)

            dob_valid = self.validated_dob(dob)
            mobile_number_valid = self.validate_mobile(cl_core_user.get('mobile_number'))

            if not cl_core_user.get('first_name') or not cl_core_user.get('last_name'):
                return Response({'name': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not dob_valid:
                return Response({"error": 'invalid date format. must be YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now()
        micro_second = "%s" % (str(now.microsecond)[:2])
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'email': email,
                'username': email.split('@')[0] + micro_second,
                'role': 'IN',
                **cl_core_user
            }
        )

        if created:
            Profile.objects.create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                middle_name=middle_name,
                last_name=user.last_name,
                mobile_number=user.mobile_number,
                birthday=dob,
                # birthday=user.birthday,
                default_contact_info='email'
            )

        token = create_token(user=user)
        data = self.format_response(user, token)
        update_last_login(None, user)

        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def format_response(user, token):
        data = {
            "id": user.id,
            "key": str(token),
            "email": encryption.encrypt(user.email),
            "photo": encryption.encrypt(str(user.photo)),
            "email_otp_active": user.is_otp_active,
            "info": {
                "email": encryption.encrypt(user.email),
                "mobile_number": encryption.encrypt(user.mobile_number),
                "first_name": encryption.encrypt(user.first_name),
                "last_name": encryption.encrypt(user.last_name),
            }
        }
        if hasattr(user, 'profile'):
            if user.profile.middle_name is None:
                data['info']['middle_name'] = user.profile.middle_name
            else:
                data['info']['middle_name'] = encryption.encrypt(user.profile.middle_name)
            data['info']['birthday'] = encryption.encrypt(str(user.profile.birthday))  # birthday converted to string
            data['info']['full_name'] = encryption.encrypt(user.profile.get_full_name())
        return data

    @staticmethod
    def validate_mobile(mobile):
        if User.objects.filter(mobile_number=mobile).exists():
            return False
        return True

    @staticmethod
    def validate_dob(date):
        try:
            datetime.fromisoformat(date)
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def validate_jwt(token):
        try:
            decode = jwt.decode(
                token, settings.SECRET_JEY, algorithms=["HS256"]
            )
        except Exception as e:
            print(e)
            return False

        if decode['id'] == 4:
            return True
        else:
            return False


class SSOUpdateUserFix(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SSOUserUpdateFIX

    def put(self, request):
        user = request.user
        can_edit = False

        required_data = [user.first_name, user.last_name, user.mobile_number]
        if None in required_data or "" in required_data:
            can_edit = True

        if hasattr(user, 'profile'):
            return Response({'profile': 'edit not allowed for populated user data'}, status=status.HTTP_403_FORBIDDEN)
        print('user can edit: ', can_edit)

        if can_edit:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.first_name = serializer.data.get('first_name')
            user.last_name = serializer.data.get('last_name')
            user.mobile_number = serializer.data.get('mobile_number')
            user.save()

            Profile.objects.create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                mobile_number=user.mobile_number,
                middle_name=serializer.data.get('middle_name'),
                birthday=serializer.data.get('birthday'),
                default_contact_info='email'
            )
        return Response({'reciept': 'verified'}, status=status.HTTP_200_OK)
