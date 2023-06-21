import datetime

from email.mime import application
from io import BytesIO
from xhtml2pdf import pisa

from api.tasks.email import digi_send_and_save_health_result_summary
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from cocolife.models import CLHealthQuestions, CLHealthQuestionsAnswers
from cocolife.models import ProductInsuree, DigiInsuree, PolicyOwner, Beneficiary
from cocolife.models.Product import Benefit

from cocolife.signals.pdf_generator import pdf_generator
from cocolife.signals.premium_calculator import calculate_age
from cocolife.signals import decryption

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import EmailMessage

__all__ = ['GenerateApplicationForm', 'ApplicationFormPDF']


class GenerateApplicationForm(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            beneficiaries = [0, 1, 2, 3, 4, 5]
            productinsuree_qs = ProductInsuree.objects.all()
            digiquestion_qs = CLHealthQuestions.objects.all()
            digianswer_qs = CLHealthQuestionsAnswers.objects.all().values('answer')
            digiinsuree_qs = DigiInsuree.objects.all()
            beneficiary_qs = Beneficiary.objects.all().values(
                'full_name',
                'address',
                'contact_no',
                'birth_place',
                'birth_date',
                'citizenship',
                'sex',
                'relationship',
                'percentage_share',
                'priority_type',
                'benefit_type')
            digiquestions_qs = digiquestion_qs.values('question')
            prod_insuree = productinsuree_qs.values(
                'id',
                'billed_to_id',
                'product_id__name',
                'product__coverage_amount_max',
                'package_id__name',
                'payment_term',
                'coverage_term',
            ).filter(application_number=id)[0]

            product_insuree_index = prod_insuree['id']
            product_insuree_id = prod_insuree['billed_to_id']
            product_insuree_product = prod_insuree['product_id__name']
            product_insuree_package = prod_insuree['package_id__name']
            product_insuree_face_amount = prod_insuree['product__coverage_amount_max']
            product_insuree_premium_mode = prod_insuree['payment_term']
            product_insuree_coverage_term = prod_insuree['coverage_term']
            product_insuree_ID = prod_insuree['billed_to_id']

            insuree = DigiInsuree.values(
                'email',
                'first_name',
                'middle_name',
                'last_name',
                'gender',
                'occupation',
                'civil_status',
                'nationality',
                'place_of_birth',
                'sss',
                'tin',
                'business',
                'tel_number',
                'home_address',
                'home_village',
                'home_city',
                'home_province',
                'home_zip_code',
            ).filter(user_id=product_insuree_id)[0]

            digi_user_id = DigiInsuree.get(user_id=product_insuree_id)
            policyO_Fname = insuree['first_name']
            policyO_Mname = insuree['middle_name']
            policyO_Lname = insuree['last_name']
            policyO_Email = insuree['email']
            policyO_Gender = insuree['gender']
            policyO_Occupation = insuree['occupation']
            policyO_Civil_status = insuree['civil_status']
            policyO_Nationality = insuree['nationality']
            policyO_PoB = insuree['place_of_birth']
            policyO_SSS = insuree['sss']
            policyO_TIN = insuree['tin']
            policyO_Business = insuree['business']
            policyO_Telno = insuree['tel_number']
            policyO_Address = insuree['home_address']
            policyO_Village = insuree['home_village']
            policyO_HomeCity = insuree['home_city']
            policyO_Province = insuree['home_province']
            policyO_ZipCode = insuree['home_zip_code']

            birthdayQ = DigiInsuree.all().values('birthday').filter(
                user_id=product_insuree_id)[0]

            birthday = birthdayQ['birthday']
            birthdate = datetime.date(
                birthday.year, birthday.month, birthday.day
            )
            age = digi_user_id.get_age()

            questionIfAdult = digiquestions_qs.filter(is_adult=1).order_by('id')[0:7]
            questionIfNotAdult = digiquestions_qs.filter(is_adult=0).order_by('id')

            digi_beneficiary = beneficiary_qs.filter(product_insuree_id=product_insuree_index).order('id')[0:5]
            answerIfAdult = digianswer_qs.filter(ProdInsuree_id=product_insuree_index, question_id__lte=7).order_by(
                'id')
            answerIfNotAdult = digianswer_qs.filter(ProdInsuree_id=product_insuree_index, question_id__lte=7).order_by(
                'id')

            print(answerIfAdult)

            questionIfAdult_Arr = []
            questionIfNotAdult_Arr = []

            answerIfAdult_Arr = []
            answerIfNotAdult_Arr = []

            beneficiaryList_Arr = []

            for questions in questionIfAdult:
                questionIfAdult_Arr.append(questions['question'])

            for questions in questionIfNotAdult:
                questionIfNotAdult_Arr.append(questions['question'])

            for answers in answerIfAdult:
                answerIfAdult_Arr.append(answers['answer'])

            for answers in answerIfNotAdult:
                answerIfNotAdult_Arr.append(answers['answer'])

            data = {
                'loop': beneficiaries,
                'id': id,
                'questionIfAdult': questionIfAdult_Arr,
                'questionIfNotAdult': questionIfNotAdult_Arr,

                'firstName': policyO_Fname,
                'middleName': policyO_Mname,
                'lastName': policyO_Lname,
                'email': policyO_Email,
                'gender': policyO_Gender,
                'birthday': birthday,
                'occupation': policyO_Occupation,
                'civil_status': policyO_Civil_status,
                'nationality': policyO_Nationality,
                'age': age,
                'birthday': birthdate,
                'place_of_birth': policyO_PoB,
                'sss': policyO_SSS,
                'tin': policyO_TIN,
                'business': policyO_Business,
                'telno': policyO_Telno,
                'address': policyO_Address,
                'village': policyO_Village,
                'municipality': policyO_HomeCity,
                'province': policyO_Province,
                'zip': policyO_ZipCode,

                'package': product_insuree_package,
                'face_amount': product_insuree_face_amount,
                'coverage_term': product_insuree_coverage_term,
                'premium_mode': product_insuree_premium_mode,

                'beneficiary': beneficiaries,

                'answerIfAdult': answerIfAdult_Arr,
                'answerIfNotAdult': answerIfNotAdult_Arr,
            }

            template = get_template('applicationForm2022.html')
            data_p = template.render(data)
            response = BytesIO()
            pdf_page = pisa.pisaDocument(
                BytesIO(data_p.encode('UTF-8')), response
            )
            if not pdf_page.err:
                response = HttpResponse(
                    response.getvalue(), content_type='application/pdf')
                filename = "Application Form.pdf"
                content = "inline; filename=%s" % (filename)
                download = request.GET.get("download")

                if download:
                    content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content
                return response

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ApplicationFormPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = decryption.decrypt(request.data.get("id"))
        try:
            application = ProductInsuree.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': 'application does not exists'}, status=status.HTTP_404_NOT_FOUND)

        application_data = application.application_form

        application_data['product_selection']['package'] = application.package.name
        application_data['product_selection']['face_amount'] = Benefit.objects.filter(
            variant=application.variant).value('face_amount')
        application_data['product_selection']['premium'] = application.premium_amount_due
        application_data['product_selection']['age'] = calculate_age(application_data['product_selection']['birthdate'])
        application_data['healthquestion'] = self.get_question_context(application_data['healthquestion'])
        application_data['application1']['height'] = application.height
        application_data['application2']['weight'] = application.weight

        context = application_data

        if application.product.name == 'Term Shield':
            template = get_template('Application for Insurance SIO under E-commerce.html')
        else:
            template = get_template('IPA Application Form - 0721-2.html')

        try:
            path_to_save_pdf = f'{settings.MEDIA_ROOT}\{id}.pdf'
            pdf_password = application.application_number
            generator = pdf_generator(template, context)
            pdf = generator.generate(path_to_save_pdf, pdf_password)

        except:
            return Response({"error": 'an error has occured while generating your pdf'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            customer_email = application_data[{'filename': f'{application.application_number}.pdf',
                                               'content': pdf.read()}]
            underwriting_email = 'vanjo_mampusti@questronix.com.ph'

            attachments = [{'filename': f'{application.application_number}.pdf', 'content': pdf.read()}]

            self.send_email(
                'Generated PDF',
                'digiinsurance@qymera.com',
                f'Good Day Customer! Here are your generated PDF. The password for your PDF is "{pdf_password}"',
                attachments, [underwriting_email, customer_email])
            return Response({"success": "An email was sent to you containing your application form"},
                            status=status.HTTP_200_OK)

        except:
            return Response({"error": 'An error has occured while sending email'}, status=status.HTTP_400_BAD_REQUEST)

    def get_questions_context(self, question_dict):
        question_list = []
        for q in question_dict:
            question = CLHealthQuestions.objects.get(id=q['question'])

            if question.question_type == 'Yes/No':
                entry = {'number': question.question_number, 'question': question.question, 'answer': q['answer'],
                         "is_adult": question.is_adult}
                question_list.append(entry)
        return question_list

    def send_email(self, subject, from_email, text_content, attachemnts, to_email):
        msg = EmailMessage(subject, text_content, from_email, to_email)
        for attachment in attachemnts:
            msg.attach(attachment['file'], attachment['content'], 'text/pdf')
        msg.send(fail_silently=False)
