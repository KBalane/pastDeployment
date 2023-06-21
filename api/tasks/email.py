import logging
import os
from email import encoders
from email.mime.base import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

# from digi.models.ProductInsuree import ProductInsuree
# from digi.models import CocoInsuree
from cocolife.models import ProductInsuree, DigiInsuree
from cocolife.utils import render_mail, generate_application_form_pdf
from cocolife.constants import AGENT_EMAILS
from digiinsurance.celery import app
from digiinsurance.models import User

logger = logging.getLogger("api.tasks")

__all__ = [
    'send_verification_email',
    'send_claims_confirmation',
    # 'send_welcome_email',
    # 'send_credentials_email',
    # # 'send_reload_receipt',
    # # 'send_payout_receipt',
    'send_forgot_password_email',
    # 'send_enrollment_success_email',
    # 'send_certificate_generation_email',
    # 'send_payment_receipt_email',
    # 'send_course_completion_email',
    'send_transaction_info',
    'digi_send_email_verification',
    'digi_send_forgot_password_email',
    'digi_send_product_summary',
    'digi_send_proposal_result',
    'digi_send_inquiry',
    'digi_send_admin_create_email',
    'notify_agent_of_failed_health_declaration',
    'notify_insuree_of_failed_health_declaration',
]

support_email = 'maharlika@digi.com'


@app.task(name='tasks.email.send_verification_email')
def send_verification_email(user_id, token):
    from urllib.parse import urlparse

    logger.info("Sending verification email")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(
            'Failed to send verification email. User with ID %s not found.',
            user_id)
        return

    # verify_url = (settings.WEB_APP_URL, kwargs={'token': token}).lstrip('/')
    verify_url = '%s/api/v1/account/verify-email/%s' % (settings.WEB_APP_URL, token)

    subject = "DigiInsurance: Email Verification"
    context = {
        # 'name': user.username,
        'link': verify_url,
        # 'web_app_url': settings.WEB_APP_URL
    }

    text_content = get_template('emails/verification.txt').render(context)
    html_content = get_template('emails/verification.html').render(context)

    msg = EmailMultiAlternatives(
        subject, text_content, support_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.debug('Successfully sent verification email to %r', user)


@app.task(name='tasks.email.send_claims_confirmation')
def send_claims_confirmation(user_id, context):
    logger.info("Sending claims confirmation")
    serialized_data = context

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(
            'Failed to send claims confirmation. User with ID %s not found.' % (user_id)
        )
        return

    subject = "DigiInsurance: Claims Confirmation"

    context = {
        'Policy_Id': serialized_data.get('Policy_id'),
        'Claims_refno': serialized_data.get('Claims_id')
    }

    text_content = get_template('emails/claims_confirmation.txt').render(context)
    html_content = get_template('emails/claims_confirmation.html').render(context)

    msg = EmailMultiAlternatives(
        subject, text_content, support_email, [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.debug('Successfully sent claims email to %r', user)


# @app.task(name='tasks.email.send_welcome_email')
# def send_welcome_email(user_id):
#     logger.info("Sending welcome email")

#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         logger.warning(
#             'Failed to send welcome email. User with ID %s not found.',
#             user_id)
#         return

#     subject = "Welcome to Apptitude!"
#     context = {
#         'name': user.username,
#         'role': user.role,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     text_content = get_template('emails/welcome.txt').render(context)
#     html_content = get_template('emails/welcome.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug('Successfully sent welcome email to %r', user)


# @app.task(name='tasks.email.send_credentials_email')
# def send_credentials_email(user_id, password):
#     logger.info("Sending credentials")

#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         logger.warning(
#             'Failed to send credentials email. User with ID %s not found.',
#             user_id)
#         return

#     subject = "Apptitude: Login Credentials"
#     context = {
#         'user': user,
#         'password': password,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     text_content = get_template('emails/teacher_creds.txt').render(context)
#     html_content = get_template('emails/teacher_creds.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug('Successfully sent credentials to %r', user)


# # @app.task(name='tasks.email.send_reload_receipt')
# # def send_reload_receipt(user_id, trans_id):
# #     logger.info("Sending receipt")

# #     try:
# #         user = User.objects.get(id=user_id)
# #     except User.DoesNotExist:
# #         logger.warning(
# #             'Failed to send receipt email. User with ID %s not found.',
# #             user_id)
# #         return

# #     try:
# #         dpt = DragonpayTransaction.objects.get(id=trans_id)
# #     except DragonpayTransaction.DoesNotExist:
# #         logger.warning(
# #             'Failed to send receipt email. DragonpayTransaction with ID %s not found.',
# #             trans_id)
# #         return

# #     subject = "Apptitude: Reload Receipt"
# #     context = {
# #         'name': user.full_name,
# #         'ref_no': dpt.refno,
# #         'amount': '%s %s' % (dpt.amount, dpt.currency),
# #         'transaction_fee': '0 PHP',
# #         'total': '%s %s' % (dpt.amount, dpt.currency),
# #         'web_app_url': settings.WEB_APP_URL
# #     }

# #     text_content = get_template('emails/receipt_student.txt').render(context)
# #     html_content = get_template('emails/receipt_student.html').render(context)

# #     msg = EmailMultiAlternatives(
# #         subject, text_content, support_email, [user.email])
# #     msg.attach_alternative(html_content, "text/html")
# #     msg.send()

# #     logger.debug('Successfully sent receipt to %r', user)


# # @app.task(name='tasks.email.send_payout_receipt')
# # def send_payout_receipt(user_id, trans_id):
# #     logger.info("Sending receipt")

# #     try:
# #         user = User.objects.get(id=user_id)
# #     except User.DoesNotExist:
# #         logger.warning(
# #             'Failed to send receipt email. User with ID %s not found.',
# #             user_id)
# #         return

# #     try:
# #         dpt = DragonpayPayout.objects.get(id=trans_id)
# #     except DragonpayPayout.DoesNotExist:
# #         logger.warning(
# #             'Failed to send receipt email. DragonpayPayout with ID %s not found.',
# #             trans_id)
# #         return

# #     subject = "Apptitude: Payout Receipt"
# #     context = {
# #         'ref_no': dpt.refno,
# #         'amount': '%s %s' % (dpt.amount, dpt.currency),
# #         'transaction_fee': '0 PHP',
# #         'total': '%s %s' % (dpt.amount, dpt.currency),
# #         'web_app_url': settings.WEB_APP_URL
# #     }

# #     text_content = get_template('emails/receipt_payout.txt').render(context)
# #     html_content = get_template('emails/receipt_payout.html').render(context)

# #     msg = EmailMultiAlternatives(
# #         subject, text_content, support_email, [user.email])
# #     msg.attach_alternative(html_content, "text/html")
# #     msg.send()

# #     logger.debug('Successfully sent receipt to %r', user)


@app.task(name='tasks.email.send_forgot_password_email')
def send_forgot_password_email(user_id, uid_and_token_b64):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(
            'Failed to send forgot password confirmation. User with ID %s not found.' % (user_id)
        )
        return

    # confirm_reset_url = '%s%s' % (settings.WEB_APP_URL, reverse(
    #     'website:reset_password',
    #     kwargs={'token': uid_and_token_b64}).lstrip('/'))

    confirm_reset_url = 'https://digiinsurance-yhrbl.ondigitalocean.app/login/%s' % (uid_and_token_b64)
    subject = "Digiinsurance: Password Reset"
    context = {
        'name': user.username,
        'link': confirm_reset_url,
        'web_app_url': settings.WEB_APP_URL
    }
    text_content = get_template('emails/reset_password.txt').render(context)
    html_content = get_template('emails/reset_password.html').render(context)

    msg = EmailMultiAlternatives(subject, text_content, support_email, to=[user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# @app.task(name='tasks.email.send_reminder_email')
# def send_reminder_email(enrollment_id, context=None, attachment=None):
#     from apptitude.models.enrollment import Enrollment
#     from notifications.signals import notify
#     """
#     Recipients must be valid list of name, email tuples

#     Hardcoded Email
#     Template # 1 will always need

#     text, button_text, button_link


#     TODO: Create a method to dynamically pass context to this task for future newsletters
#     """

#     enrollment = Enrollment.objects.get(id=enrollment_id)
#     student = enrollment.student
#     course = enrollment.get_course()
#     enrolled_object = enrollment.enrolled_object

#     context = {
#         'subject': 'Apptitude: Resume {}'.format(course.name),
#         'text': "I noticed you haven't finished {}. A better version of you awaits.".format(
#             course.name),
#         'text2': 'Keep on learning by clicking the button below.',
#         'button_text': 'Resume Course!',
#         'button_link': course.course_link
#     }

#     subject = context['subject']

#     context['name'] = student.first_name

#     text_content = get_template('emails/reminder.txt').render(context)
#     html_content = get_template('emails/reminder.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     admin = User.objects.get(username='admin')

#     notify.send(
#         admin,
#         recipient=[student.user],
#         verb='<a href="{}">Resume {}</a>'.format(
#             course.course_link, course.name),
#         action_object=enrollment,
#         target=enrolled_object,
#         description='<a href="{}">Resume {}</a>'.format(
#             course.course_link, course.name),
#     )

#     logger.debug(
#         'Successfully sent reminder email to %r enrollment id %r',
#         student.user.email, enrollment_id)


# @app.task(name='tasks.interval_sending')
# def interval_send_email(enrollments, context=None, attachment=None):
#     countdown = 5
#     for enrollment in enrollments:
#         if not settings.IS_PRODUCTION:
#             logger.debug(
#                 'Will NOT send reminder EMAIL to enrollment %s', enrollment)
#             continue

#         send_reminder_email.apply_async(
#             args=(enrollment,), countdown=countdown)
#         countdown += 15


# @app.task(name='tasks.email.send_enrollment_success_email')
# def send_enrollment_success_email(enrollment_id):
#     from apptitude.models.enrollment import Enrollment

#     enrollment = Enrollment.objects.get(id=enrollment_id)
#     student = enrollment.student
#     course = enrollment.get_course()

#     if enrollment.status == Enrollment.PAID:
#         text = (
#             "You have successfully enrolled in {}! "
#             "Click the button below to start learning.").format(
#             course.name)
#         button_text = 'Start Learning'
#         button_link = course.course_link
#     else:
#         text = (
#             "You have successfully enrolled in {}! "
#             "Please complete your payment in order to start your learning."
#         ).format(course.name)
#         button_text = 'Browse Courses'
#         button_link = course.school.school_link

#     context = {
#         'name': student.first_name,
#         'subject': 'Enrollment in {} successful!'.format(course.name),
#         'text': text,
#         'button_text': button_text,
#         'button_link': button_link,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     subject = context['subject']

#     text_content = get_template(
#         'emails/enrollment_success.txt').render(context)
#     html_content = get_template(
#         'emails/enrollment_success.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug(
#         'Successfully sent enrollment success email for %r enrollment id %r',
#         student.user.email, enrollment_id)


# @app.task(name='tasks.email.send_course_completion_email')
# def send_course_completion_email(enrollment_id):
#     from apptitude.models.enrollment import Enrollment

#     enrollment = Enrollment.objects.get(id=enrollment_id)
#     student = enrollment.student
#     course = enrollment.get_course()

#     context = {
#         'subject': '{} completed!'.format(course.name),
#         'name': student.first_name,
#         'text': "Congratulations on completing {}!".format(course.name),
#         'text2': "Continue building your career by enrolling in our other Courses.",
#         'button_text': 'Browse Courses',
#         'button_link': course.school.school_link,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     subject = context['subject']

#     text_content = get_template('emails/course_completion.txt').render(context)
#     html_content = get_template('emails/course_completion.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug(
#         'Successfully sent course completion email for %r enrollment id %r',
#         student.user.email, enrollment_id)


# @app.task(name='tasks.email.send_certificate_generation_email')
# def send_certificate_generation_email(enrollment_id, certificate_id):
#     from apptitude.models.enrollment import Enrollment
#     from blockchain.models import CertificateAddress

#     enrollment = Enrollment.objects.get(id=enrollment_id)
#     course = enrollment.get_course()
#     student = enrollment.student
#     certificate = CertificateAddress.objects.get(id=certificate_id)
#     context = {
#         'subject': 'Certificate Available for {}'.format(course.name),
#         'text': "You certificate for {} is now available!".format(course.name),
#         'text2': "Click the button below to view and download your certificate.",
#         'button_text': 'Get Certificate',
#         'button_link': '{}{}'.format(
#             settings.WEB_APP_URL, reverse(
#                 'dashboard:get_certificate',
#                 kwargs={'address': certificate.address})),
#         'web_app_url': settings.WEB_APP_URL
#     }

#     subject = context['subject']

#     text_content = get_template(
#         'emails/certificate_generation.txt').render(context)
#     html_content = get_template(
#         'emails/certificate_generation.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug(
#         'Successfully sent certificate generation email to %r enrollment id %r',
#         student.user.email, enrollment_id)


# @app.task(name='tasks.email.send_payment_receipt_email')
# def send_payment_receipt_email(enrollment_id, payment_id):
#     from apptitude.models.enrollment import Enrollment
#     from apptitude.models.payment import PaymentDetail

#     enrollment = Enrollment.objects.get(id=enrollment_id)
#     course = enrollment.get_course()
#     student = enrollment.student
#     payment = PaymentDetail.objects.get(id=payment_id)

#     context = {
#         'subject': 'Payment Receipt for {}'.format(course.name),
#         'name': student.first_name,
#         'ref_no': payment.txn_id,
#         'amount': payment.amount,
#         'total': payment.amount,
#         'button_text': 'Start Learning',
#         'button_link': course.course_link,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     subject = context['subject']

#     text_content = get_template('emails/payment_receipt.txt').render(context)
#     html_content = get_template('emails/payment_receipt.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.user.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug(
#         'Successfully sent payment_receipt email for %r enrollment id %r',
#         student.user.email, enrollment_id)


# @app.task(name='tasks.email.send_campaign_email')
# def send_campaign_email(campaign_id, student_id):
#     from apptitude.models.user import Student
#     from apptitude.models.marketing import CourseCampaign

#     # TODO add try except block here
#     student = Student.objects.get(id=student_id)
#     campaign = CourseCampaign.objects.get(id=campaign_id)

#     total_emails_today = CourseCampaign.get_emails_sent_today()

#     if total_emails_today >= settings.EMAIL_LIMIT:
#         # Do not send
#         logger.info('Limit reached! Scheduling for next day!')
#         # Schedule for next day na
#         if campaign.schedule == date.today():
#             campaign.schedule = campaign.schedule + timedelta(days=1)
#             campaign.save(update_fields=['schedule', 'emails_sent_today'])
#         return

#     context = {
#         'subject': 'Take {} now!'.format(campaign.course.name),
#         'body': 'Check out our course!',
#         'name': student.first_name,
#         'course_name': campaign.course.name,
#         'button_text': 'Start Learning',
#         'button_link': campaign.course.course_link,
#         'web_app_url': settings.WEB_APP_URL
#     }
#     if campaign.email_subject:
#         context['subject'] = campaign.email_subject

#     if campaign.email_body:
#         context['body'] = campaign.email_body

#     subject = context['subject']

#     text_content = get_template('emails/campaign_course.txt').render(context)
#     html_content = get_template('emails/campaign_course.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [student.email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     campaign.last_sent_to = student
#     campaign.last_sending_mode = campaign.sending_mode
#     campaign.last_sent_date = date.today()
#     campaign.emails_sent_total = F('emails_sent_total') + 1
#     campaign.emails_sent_today = F('emails_sent_today') + 1
#     campaign.save()
#     logger.debug(
#         'Successfully sent %s campaign email to %s',
#         campaign.course.name, student.email)


# @app.task(name='tasks.do_campaign')
# def do_campaign(campaign_id):
#     from apptitude.models.marketing import CourseCampaign
#     from datetime import timedelta, date
#     from django.conf import settings
#     countdown = 5

#     campaign = CourseCampaign.objects.get(id=campaign_id)

#     # Get list of recipients
#     recipients = campaign.get_recipients()

#     # check the last recipient if continuing campaign
#     if campaign.last_sent_to:

#         # Recipients are ordered by ID so lets start with the next
#         # student in line by ID
#         recipients = recipients.filter(id__gt=campaign.last_sent_to.id)
#     logger.info(recipients.count())
#     for i, recipient in enumerate(recipients):
#         if not settings.IS_PRODUCTION:
#             logger.debug(
#                 'Will NOT send reminder EMAIL to %s', recipient.email)
#             continue
#         # Check if we are still in Gmails quota
#         total_emails_today = CourseCampaign.get_emails_sent_today()

#         if total_emails_today < settings.EMAIL_LIMIT and i < settings.EMAIL_LIMIT:
#             send_campaign_email.apply_async(
#                 args=(campaign.id, recipient.id,), countdown=countdown)
#             countdown += 15
#         else:
#             # Do not send
#             logger.info('Reached {} of {}'.format(total_emails_today, settings.EMAIL_LIMIT))
#             logger.info('Limit reached! Scheduling for next day!')
#             # Schedule for next day na
#             if campaign.schedule == date.today():
#                 campaign.schedule = campaign.schedule + timedelta(days=1)
#                 campaign.save(update_fields=['schedule', 'emails_sent_today'])
#             return


# @app.task(name='tasks.email.send_cert_request_payment_receipt_email')
# def send_cert_request_payment_receipt_email(request_id, payment_id):
#     from cms.models import CertificateRequest, CertificatePaymentDetail

#     cert_request = CertificateRequest.objects.get(id=request_id)
#     course_name = cert_request.get_course()
#     email = cert_request.fields_data['email']
#     payment = CertificatePaymentDetail.objects.get(id=payment_id)

#     context = {
#         'subject': 'Payment Receipt for Certificate Request of %s'.format(course_name),
#         'name': cert_request.first_name,
#         'ref_no': payment.txn_id,
#         'amount': payment.amount,
#         'total': payment.amount
#     }

#     subject = context['subject']

#     text_content = get_template('emails/payment_receipt.txt').render(context)
#     html_content = get_template('emails/certificate_payment_receipt.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

#     logger.debug(
#         'Successfully sent payment_receipt email for %r request id %r',
#         email, cert_request.id)


# @app.task(name='tasks.email.send_certificate_request_email')
# def send_certificate_request_email(address, request_id):
#     from api.utils import generate_certificate
#     from cms.models import CertificateRequest

#     request = CertificateRequest.objects.get(id=request_id)
#     course_name = request.course.name
#     email = request.fields_data['email']

#     context = {
#         'subject': 'Certificate Request for %s' % course_name,
#         'name': request.first_name,
#         'course_name': course_name,
#         'web_app_url': settings.WEB_APP_URL
#     }

#     subject = context['subject']

#     text_content = get_template(
#         'emails/certificate_request.txt').render(context)
#     html_content = get_template(
#         'emails/certificate_request.html').render(context)

#     msg = EmailMultiAlternatives(
#         subject, text_content, support_email, [email])
#     msg.attach_alternative(html_content, "text/html")

#     path = generate_certificate(address)
#     msg.attach_file(path)
#     msg.send()

#     logger.debug(
#         'Successfully sent certificate to email for %r request id %r',
#         email, request.id)


@app.task(name='tasks.email.send_transaction_info')
def send_transaction_info(transaction_id, email):
    context = {
        'subject': 'Transaction Success',
        'transaction_id': transaction_id
    }

    subject = context['subject']

    text_content = get_template(
        'emails/transaction.txt').render(context)
    html_content = get_template(
        'emails/transaction.html').render(context)

    msg = EmailMultiAlternatives(
        subject, text_content, support_email, [email])
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    # logger.debug(
    #     'Successfully sent transaction info to email for %r request id %r',
    #     email, request.id)


@app.task(name='tasks.email.send_forgot_password_email')
def digi_send_email_verification(email, token):
    user = get_object_or_404(User, email=email)

    activate_url = '%s/api/v1/digi/auth/account/activate/email/%s' % (settings.API_URL, token)
    subject = "Maharlika"
    context = {
        'link': activate_url,
    }
    text_content = get_template('emails/reset_password.txt').render(context)
    html_content = get_template('emails/digi-email.html').render(context)

    msg = EmailMultiAlternatives(subject, text_content, support_email, to=[user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def digi_send_forgot_password_email(user_id, uid_and_token_b64):
    user = get_object_or_404(User, id=user_id)

    confirm_reset_url = 'https://digi-insurance-web-next-pxumm.ondigitalocean.app/reset-password/%s' % (
        uid_and_token_b64)
    subject = "Qymera: Password Reset"
    context = {
        'name': user.username,
        'link': confirm_reset_url,
        'web_app_url': settings.WEB_APP_URL
    }
    text_content = get_template('emails/reset_password.txt').render(context)
    html_content = get_template('emails/digi-forgot-email.html').render(context)

    msg = EmailMultiAlternatives(subject, text_content, support_email, to=[user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def digi_send_product_summary(
        pdf,
        user_id,
        product_insuree_id,
):
    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Maharlika: Product Purchased | Product Summary"
    if IS_PRODUCTION:
        subject = "Maharlika: Product Purchased | Product Summary"

    product_no = get_object_or_404(ProductInsuree, id=product_insuree_id)
    user = DigiInsuree.objects.get(user=product_no.billed_to)
    email = [user.email]
    print(email)
    agent = ['apconde@digi.com', 'jdaguilar@digi.com']
    bcc = ['rybelbes@digi.com', 'achernandez@digi.com', 'van.keith_almazan@questronix.com.ph']
    # Uncomment this for testing
    # agent = ['james.adrian_ruiz@questronix.com.ph']
    # bcc = ['vince.josef_magbanua@questronix.com.ph', 'van.keith_almazan@questronix.com.ph']

    msg = EmailMultiAlternatives(
        subject,
        "Here is an attached file of what you have purchased.",
        support_email,
        to=email,
        cc=agent,
        bcc=bcc,
    )

    msg.attach_alternative(
        """
        We have received your application with reference no.%s <br>
        Please expect the result within 3-5 business days. <br><br>
        """ % (product_no.application_number),
        "text/html"
    )
    msg.attach('Product Summary', pdf, 'application/pdf')
    msg.send()


def digi_send_and_save_health_result_summary(pdf, user):
    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Maharlika: Health Questions Result/Summary"
    if IS_PRODUCTION:
        subject = "Maharlika: Health Questions Result/Summary"

    # user = User.objects.get(id = user)
    user = DigiInsuree.objects.get(user=user)
    email_to = user.email
    msg = EmailMultiAlternatives(
        subject, "Here is an attached file of what you have purchased.", support_email, to=[email_to])
    # subject, "Here is an attached file of the interview results.", support_email, to=['van.keith_almazan@questronix.com.ph','blair.jurgen_chacon@questronix.com.ph'])
    msg.attach_alternative("""
        Thank you for choosing digi.
        Here is an attached file of the interview results.
        """, "text/html")
    # msg.attach("http://nonprod-applb-801584624.ap-southeast-1.elb.amazonaws.com/media/products/4.pdf")
    # attachment = open(pdf, 'rb')
    # newpdf = pdf.replace("\\","/")

    msg.attach('Product Summary', pdf, 'application/pdf')

    # msg.attach_file(pdf)

    msg.send()


def digi_send_proposal_result(pdf, user, application_number):
    user = get_object_or_404(DigiInsuree, user=user)

    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Maharlika: Product Proposal"
    if IS_PRODUCTION:
        subject = "Maharlika: Product Proposal"

    msg = EmailMultiAlternatives(
        subject, "Here is an attached file of your Product Proposal.", support_email, to=[user.email])
    msg.attach_alternative("""
        Thank you for choosing digi.
        Here is an attached file of your Product Proposal #%s.
        """ % (application_number), "text/html")

    msg.attach('Product Proposal #%s' % (application_number), pdf, 'application/pdf')
    msg.send()


def digi_send_inquiry(data):
    context = {
        "data": data,
        "user": data['user'],
    }

    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] NEW MESSAGE FROM THE digi MOBILE APP"
    if IS_PRODUCTION:
        subject = "NEW MESSAGE FROM THE digi MOBILE APP"

    BCC = ["customer_service@digi.com", "rybelbes@digi.com"]
    FAKE_BCC = ['john.lendl_cuyugan@questronix.com.ph', "rybelbes@digi.com"]
    msg = EmailMultiAlternatives(
        subject, None, support_email, to=data['to_email'], bcc=BCC)

    if data['attachment']:
        # get image data
        image_name = data['attachment'].split("inquiries/")[1]
        img_path = os.path.join(settings.MEDIA_ROOT, 'inquiries/%s' % image_name)
        img_data = open(img_path, 'rb')

        part = MIMEBase('multipart', 'mixed; name=%s' % image_name)
        part.set_payload(img_data.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % image_name.lower())

        msg.attach(part)

    html_content = get_template('emails/cl_inquiry_form.html').render(context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def digi_send_admin_create_email(email, uid_and_token_b64):
    test_url = 'http://localhost:3000/account-activate/%s' % (uid_and_token_b64)
    confirm_reset_url = '%s/account-activate/%s' % (settings.API_URL, uid_and_token_b64)

    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Maharlika Admin Account Activation"
    if IS_PRODUCTION:
        subject = "Maharlika Admin Account Activation"

    context = {
        'link': confirm_reset_url,
        'web_app_url': settings.WEB_APP_URL
    }
    text_content = get_template(
        'emails/reset_password.txt').render(context)
    html_content = get_template(
        'emails/activate-admin.html').render(context)

    msg = EmailMultiAlternatives(
        subject, text_content, 'vince.josef_magbanua@questronix.com.ph', to=['vince.josef_magbanua@questronix.com.ph'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# @app.task(name='tasks.email.notify_agent_of_failed_health_declaration')
def notify_agent_of_failed_health_declaration(
        reference_id,
        product_name,
        application_datetime_str,
        application_number,
        full_name,
        mobile,
        email,
):
    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Maharlika App: A user has applied on the app for a product but failed on the health declaration"
    if IS_PRODUCTION:
        subject = "Maharlika App: A user has applied on the app for a product but failed on the health declaration"

    context = {
        'reference_id': reference_id,
        'product_name': product_name,
        'application_datetime': application_datetime_str,
        'full_name': full_name,
        'mobile': mobile,
        'email': email,
    }
    pdf = generate_application_form_pdf(application_number)

    if not pdf:
        raise Exception('Error generating application form')

    email = render_mail(
        subject.strip(),
        'email/failed_health_declaration_agent',
        context,
        AGENT_EMAILS,
        attachment_name='Application Form',
        attachment_file=pdf,
        attachment_type='application/pdf',
    )
    email.send()


# @app.task(name='tasks.email.notify_insuree_of_failed_health_declaration')
def notify_insuree_of_failed_health_declaration(
        product_name,
        insuree_email,
):
    IS_PRODUCTION = settings.IS_PRODUCTION
    subject = "[TEST] Digiinsurance Qymera: Thank you for your interest"
    if IS_PRODUCTION:
        subject = "Digiinsurance Qymera: Thank you for your interest"

    context = {
        'product_name': product_name,
    }

    email = render_mail(
        subject,
        'email/failed_health_declaration_insuree',
        context,
        [insuree_email],
    )
    email.send()
