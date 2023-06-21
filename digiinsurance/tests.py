from django.http import HttpResponseNotAllowed, HttpResponse
import re


def validate_data(request):
    if request.method == 'GET':
        return HttpResponse('This is a get request', content_type='text/plain')
    elif request.method == 'POST':
        error_messages = []
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()

        if not all(char.isalnum() for char in first_name):
            error_messages.append('First name should only contain characters and numbers without any spaces or special characters')
        if not all(char.isalnum() for char in last_name):
            error_messages.append('Last name should only contain characters and numbers without any spaces or special characters')
        if not phone.isdigit() or len(phone) > 10:
            error_messages.append('Phone number should only contain numbers and should have maximum length of 10 digits')
        if not email or not re.match(r'^\w+[.+-]?\w+@\w+\.\w+(\.\w+)?$', email):
            error_messages.append('Invalid email. Email should have the format: example@domain.com')
        if error_messages:
            return HttpResponse('\n'.join(error_messages), content_type='text/plain', status=400)
        else:
            return HttpResponse('Your data is valid', content_type='text/plain')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'], content_type='text/plain')
