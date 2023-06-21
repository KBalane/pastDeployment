import base64
import errno
import io
import json
import logging
import os
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from digiinsurance.models.Policy import Policy
from kyc.models import UserID, TemplateID
from kyc.forms import ImageUploadForm
from kyc.utils import compare_photo, check_details, get_s3_bucket, detect_texts

logger = logging.getLogger('kyc.views')


@login_required
def compare_faces(request):
    if request.method == 'POST':
        user = request.user
        img_data = request.POST['image']
        format, imgstr = img_data.split(';base64,')
        img = base64.b64decode(imgstr)
        filename = '/tmp/%d' % user.id
        with open(filename, 'wb') as f:
            f.write(img)

        uid = UserID.objects.get(user=user)
        result = compare_photo(uid.encoded, filename)

        return HttpResponse(result)


@login_required
def upload_user_id(request):
    if request.method == 'GET':
        return render(request, 'upload.html')

    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m, created = UserID.objects.update_or_create(user=request.user)
            m.photo_id = form.cleaned_data['id_image']
            m.save()
            m.encode_photo()

            template = TemplateID.objects.get(
                template_name=request.POST.get('template_name'))

            user = request.user
            names = []
            for fname in user.first_name.lower().split(' '):
                names.append(fname)
            for lname in user.last_name.lower().split(' '):
                names.append(lname)

            validity = check_details(m.photo_id.path, template.template_name, names)
            # separate err page or redirect to initial screen
            if validity is not True:
                if (validity == "WRONG_ID"):
                    return render(request, 'error.html', context={"success": False})

            else:
                context = {
                    # 'name': m.detect_name_id(template),
                    'name': ' '.join(names),
                    'detected': check_details(m.photo_id.path, template.template_name, names)
                }
                return render(request, 'show_camera.html', context=context)
        else:
            print(form.errors)


def show_camera(request):
    return render(request, 'show_camera.html')


@login_required
def upload_template_id(request):
    if request.method == 'GET':
        # Take picture of the template ID
        return render(request, 'upload_template.html')

    elif request.method == 'POST':
        data = request.POST
        form = ImageUploadForm(request.POST, request.FILES)
        fields = {
            'institute': data.get('institute'),
            'first_name': 'anon',
            'last_name': 'anon'
        }

        if form.is_valid():
            m, created = TemplateID.objects.update_or_create(
                template_name=data.get('template_name'),
                first_name='anon',
                last_name='anon'
            )
            m.template_id = form.cleaned_data['id_image']
            m.save()
            m.locate_texts(fields)

        return redirect(reverse('kyc:upload_pic'))


@method_decorator(login_required, name='dispatch')
class UploadUserIdHandler(generic.View):
    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        user = request.user

        if form.is_valid():
            try:
                template = TemplateID.objects.get(
                    id=request.POST.get('template_id'))
                user_id, created = UserID.objects.update_or_create(
                    user=request.user)
                if 'policy' in request.POST:
                    policy = Policy.objects.get(id=request.POST.get('policy'))
                    user_id.policy = policy

                img_data = request.POST.get('selfie_image')
                if img_data:
                    format, imgstr = img_data.split(';base64,')
                    ext = format.split('/')[-1]
                    img = base64.b64decode(imgstr)
                    selfie = ContentFile(
                        img, name='selfie_%s.%s' % (user.id, ext))
                    user_id.selfie = selfie

                user_id.photo_id = form.cleaned_data['id_image']
                user_id.verified = False
                user_id.template = template
                user_id.save()
                user_id.encode_photo()

                # details = m.detect_name_id(template)

                names = []
                for fname in user.first_name.lower().split(' '):
                    names.append(fname)
                for lname in user.last_name.lower().split(' '):
                    names.append(lname)

                if settings.IS_PRODUCTION:
                    validity = check_details(
                        user_id.photo_id.url, template.institute_name, names)
                else:
                    validity = check_details(
                        user_id.photo_id.path, template.institute_name, names)
                if validity is not True:
                    if validity == "WRONG_ID":
                        return HttpResponse(json.dumps({
                            'status': 'fail',
                            'code': 3,
                            'message': 'The identification card that was uploaded does not match the type selected'
                        }), status=400, content_type="application/json")
                    else:
                        return HttpResponse(json.dumps({
                            'status': 'fail',
                            'code': 4,
                            'message': 'Name detected in ID does not match the name in your profile. Please update your'
                                       'profile or upload a different ID.'
                        }), status=400, content_type="application/json")

            except IndexError as e:
                logger.exception(e)

                return HttpResponse(json.dumps({
                    'status': 'fail',
                    'code': 5,
                    'message': 'Error detecting face in ID. Please upload a clearer photo.'
                }), status=400, content_type="application/json")

            except Exception as e:
                logger.exception(e)

                return HttpResponse(json.dumps({
                    'status': 'fail',
                    'code': 2,
                    'message': 'Error uploading ID'
                }), status=400, content_type="application/json")

            if img_data:
                filename = '/tmp/%d' % user.id
                with open(filename, 'wb') as f:
                    f.write(img)

                try:
                    result = compare_photo(user_id.encoded, filename)
                except IndexError as e:
                    logger.exception(e)

                    return HttpResponse(json.dumps({
                        'status': 'fail',
                        'code': 7,
                        'message': 'Error detecting face in snapshot. Please retake your photo.'
                    }), status=400, content_type="application/json")

                except Exception as e:
                    logger.exception(e)

                    return HttpResponse(json.dumps({
                        'status': 'fail',
                        'code': 6,
                        'message': 'An error occurred. Please try again.'
                    }), status=400, content_type="application/json")

                if not result:
                    logger.exception('Comparison failed')
                    return HttpResponse(json.dumps({
                        'status': 'fail',
                        'code': 8,
                        'message': 'Photo in ID did not match the selfie. Please upload a clearer ID or retake your photo.'
                    }), status=400, content_type="application/json")

                user_id.verified = True
                user_id.save(update_fields=['verified'])

                return HttpResponse(json.dumps({
                    'status': 'success',
                    'message': 'You can now continue with your enrollment.'
                }), content_type="application/json")

            context = {
                'status': 'success',
                'message': 'Successfully matched name in ID with profile.'
            }

            return HttpResponse(
                json.dumps(context), content_type="application/json")
        else:
            logger.debug('KYC has form errors', form.errors)
            return HttpResponse(json.dumps({
                'status': 'fail', 'errors': form.errors}), status=400,
                content_type="application/json")


@method_decorator(login_required, name='dispatch')
class UploadTemplateIdHandler(generic.View):
    def post(self, request):
        data = request.POST
        form = ImageUploadForm(request.POST, request.FILES)
        fields = {
            'institute': data.get('institute'),

        }

        # 'first_name': data.get('first_name'),
        # 'last_name': data.get('last_name')

        if form.is_valid():
            try:
                m, created = TemplateID.objects.update_or_create(
                    template_name=data.get('template_name'))
                m.template_id = form.cleaned_data['image']
                m.save()
                m.locate_texts(fields)
            except Exception as e:
                logger.exception(e)
                return HttpResponse(json.dumps({
                    'status': 'fail', 'message': 'Error creating template'
                }), status=400, content_type="application/json")
            return HttpResponse(
                json.dumps({'status': 'success'}),
                content_type="application/json")
        else:
            logger.debug('Upload template id has form errors', form.errors)
            return HttpResponse(json.dumps({
                'status': 'fail', 'errors': form.errors}), status=400,
                content_type='application/json')


@method_decorator(login_required, name='dispatch')
class CompareFacesHandler(generic.View):
    def post(self, request):
        user = request.user
        img_data = request.POST.get('selfie_image')
        format, imgstr = img_data.split(';base64,')
        img = base64.b64decode(imgstr)
        filename = '/tmp/%d' % user.id
        with open(filename, 'wb') as f:
            f.write(img)

        uid = UserID.objects.get(user=user)
        try:
            result = compare_photo(uid.encoded, filename)
        except IndexError as e:
            logger.exception(e)

            return HttpResponse(json.dumps({
                'status': 'fail', 'message': 'Error detecting face in snapshot. Please retake your photo.'
            }), status=400, content_type="application/json")

        except Exception as e:
            logger.exception(e)

            return HttpResponse(json.dumps({
                'status': 'fail', 'message': 'An error occurred. Please try again.'
            }), status=400, content_type="application/json")

        return HttpResponse(result)


@method_decorator(login_required, name='dispatch')
class UploadSnapshot(generic.View):
    def post(self, request):
        user = request.user

        try:
            img_data = request.POST.get('image')
            course_id = request.POST.get('course_id')
            format, imgstr = img_data.split(';base64,')
            data = base64.b64decode(imgstr)
            file_like = io.BytesIO(data)
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            if settings.IS_PRODUCTION:
                filename = 'media/kyc/snapshots/course_%s/student_%s/%s.jpg' % (
                    course_id, user.student.id, timestamp)
                bucket = get_s3_bucket()
                bucket.upload_fileobj(file_like, filename)

                file_like.close()
            else:
                filename = '%s/kyc/snapshots/course_%s/student_%s/%s.jpg' % (
                    settings.MEDIA_ROOT, course_id, user.student.id, timestamp)
                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise

                with open(filename, 'wb') as f:
                    f.write(data)

            return HttpResponse(
                json.dumps({'status': 'success'}),
                content_type="application/json")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(json.dumps({
                'status': 'fail', 'message': 'Error uploading snapshot'
            }), status=400, content_type="application/json") \
 \
 \
@login_required
def upload_ocr(request):
    if request.method == 'GET':
        return render(request, 'upload_image.html')

    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            instance, created = UserID.objects.update_or_create(user=request.user)
            instance.photo_id = form.cleaned_data['id_image']
            instance.save()
            # disable face detection
            # instance.encode_photo()

            res = detect_texts(instance.photo_id.path)

            return render(request, 'show_results.html', context={"words": res})
        else:
            print(form.errors)
