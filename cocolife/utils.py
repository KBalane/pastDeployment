import datetime
from io import BytesIO

from xhtml2pdf import pisa

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template

from .models import (
    ProductInsuree,
    DigiInsuree,
    Beneficiary,
    CLHealthQuestionsAnswers,
    CLHealthQuestions,
)
from .constants import SUPPORT_EMAIL
from digiinsurance.models.AuditEntry import AuditEntry
from digiinsurance.models.User import User


def email_split(data):
    data = data.split(',')
    return data


def coco_user_tag(tag, username):
    AuditEntry.objects.create(action='%s_clicked_%s' % (username, tag), ip=None, username=username)
    user = DigiInsuree.objects.get(user=username)
    if user:
        if tag not in user.tags:
            user.tags += tag + ','
            user.save()
    else:
        pass


def coco_user_log(accessed_class, username):
    # ip = request.META.get('REMOTE_ADDR')
    current_datetime = datetime.datetime.now()
    AuditEntry.objects.create(action='accessed_%s | timestamp: %s' % (accessed_class, current_datetime), ip=None,
                              username=username)
    print("logged activity for %s" % username)


def user_management(user):
    user = User.objects.get(id=user)
    user_role = user.role

    if user_role == 'AD':
        return 'user is admin'
    elif user_role == 'ED':
        return 'user is editor'


def ipa_prem_calc():
    # example values

    # age ranges (5 to 17) , (18 to 45) , (46 to 55) , (56 to 64**)
    # age = 23 
    # coverage_term = 1 # 1 , 2 , 3
    # payment_term = 'monthly' #semi_annual , quarterly , monthly

    semi_annual = 0.5300
    quarterly = 0.2750
    monthly = 0.0975

    packages = ['Protect', 'Protect Plus']

    print("**********************")
    print("IPA PREMIUM CALCULATOR")
    age = input("Enter your age: ")
    coverage_term = input("Whats your coverage term?: ")
    payment_term = input("Payment Term: ")

    # region if chosen package is Protect
    # cocolife protect package
    # variant1
    variant1_face_amount_1 = 1000000.00
    variant1_face_amount_2 = 25000.00
    # variant2
    variant2_face_amount_1 = 500000.00
    variant2_face_amount_2 = 20000.00
    # table of premiums
    premium = 0
    if (int(age) >= 5 and int(age) <= 17):
        if ('1' in coverage_term):
            premium = 5150
        elif ('2' in coverage_term):
            premium = 9600
        elif ('3' in coverage_term):
            premium = 14250

    if ('m' in payment_term):
        # paid monthly             0.0975
        total_premium = premium * monthly

        # the returned value here will be payed monthly depending on the coverage term
    elif ('q' in payment_term):
        # paid monthly             0.2750
        total_premium = premium * quarterly

    elif ('s' in payment_term):
        # paid monthly             0.5300
        total_premium = premium * semi_annual

    print("This is for IPA: Cocolife Protect")
    print("Accidental Benefit: " + str(variant1_face_amount_1))
    print("Accidental Death Burial Benefit: " + str(variant1_face_amount_2))
    print("Total Premium: " + str(total_premium))
    #
    print("To be payed in a year: " + str(total_premium))
    # endregion if chosen package is Protect

    # cocolife protect plus package


# ipa_prem_calc()

'''
Products Model/Table
    "id": 1,
    "created_at": "Sep 29 11:51 am with Lendl Lex VK",
    "name": "IPA",
    "category": "life", #not sure
    "status": "active",
    "packages": [
      {
        "name": "Protect",
        "benefits": [
          {
            "name": "Accidental Benefit",
            "face_amount": "1000000.00"
          },
          {
            "name": "Accidental Death Burial Benefit",
            "value": "25000.00"
          }
        ],
        "age_bracket": [
            {
          "max": "17",
          "min": "5",
            },
            {
          "max": "45",
          "min": "16"
            },
        ],
        "description": "Cocolife Protect"
      },
      {
        "name": "Protect Plus",
        "benefits": [
          {
            "name": "Accidental Benefit",
            "face_amount": "1000000.00"
          },
          {
            "name": "Accidental Death Burial Benefit",
            "value": "25000.00"
          }
        ],
        "age_bracket": [
            {
          "max": "17",
          "min": "5",
          "coverage_term": 5150

            tbd (to be discussed)
                "coverage_term_1": "5150", #what is the sequence???? 
                                                example: increment is 4450 or 13.6% EXAMPLE times base price
                "coverage_term_2": "9600",
                "coverage_term_3": "14250",
            end tbd
            },
            {
          "max": "45",
          "min": "18",
          "coverage_term": 5150
            },
        ],
        "description": "Cocolife Protect Plus"
      },

      #then add for protect plus

    ],
    "payment_interval": [
      {
        "package": "lite",
        "payment": [
          {
            "type": "semi annual",
            "modal_factor": "0.5300",
          },
          {
            "type": "quarterly",
            "modal_factor": "0.2750",
          },
          {
            "type": "monthly",
            "modal_factor": "0.0975",
          }
        ]
      }
    ],
    "passing_score": 0, #TBD
    "company": 2,       #TBD
    "question": 1       #TBD
  },

'''

'''
sept 29, 2021
Agent Assisted Product Purchasing Process Reprio Discussion
Notes:

    iba iba ang healthquestions for per product

    iba ang 'qualifications' per product

    when do u want to be contacted

    directho tawag para simple ang process - sir remo

    will still push through even if nag fail health question (iba lang process)

    yearly premium

    major categories: is life and non-life

'''

# Static Values for TERM Calculation
ART_PREMIUM_RATES_V2 = [
    {"Age": "5", "Band 1": "5.77", "Band 2": "3.63", "Band 3": "2.43"},
    {"Age": "6", "Band 1": "5.74", "Band 2": "3.6", "Band 3": "2.4"},
    {"Age": "7", "Band 1": "5.71", "Band 2": "3.57", "Band 3": "2.37"},
    {"Age": "8", "Band 1": "5.67", "Band 2": "3.53", "Band 3": "2.33"},
    {"Age": "9", "Band 1": "5.64", "Band 2": "3.5", "Band 3": "2.3"},
    {"Age": "10", "Band 1": "5.61", "Band 2": "3.47", "Band 3": "2.27"},
    {"Age": "11", "Band 1": "5.64", "Band 2": "3.5", "Band 3": "2.3"},
    {"Age": "12", "Band 1": "5.67", "Band 2": "3.52", "Band 3": "2.33"},
    {"Age": "13", "Band 1": "5.7", "Band 2": "3.55", "Band 3": "2.35"},
    {"Age": "14", "Band 1": "5.73", "Band 2": "3.57", "Band 3": "2.38"},
    {"Age": "15", "Band 1": "5.76", "Band 2": "3.6", "Band 3": "2.41"},
    {"Age": "16", "Band 1": "5.85", "Band 2": "3.7", "Band 3": "2.51"},
    {"Age": "17", "Band 1": "5.95", "Band 2": "3.8", "Band 3": "2.6"},
    {"Age": "18", "Band 1": "6.04", "Band 2": "3.89", "Band 3": "2.7"},
    {"Age": "19", "Band 1": "6.14", "Band 2": "3.99", "Band 3": "2.79"},
    {"Age": "20", "Band 1": "6.23", "Band 2": "4.09", "Band 3": "2.89"},
    {"Age": "21", "Band 1": "6.28", "Band 2": "4.14", "Band 3": "2.94"},
    {"Age": "22", "Band 1": "6.33", "Band 2": "4.19", "Band 3": "2.99"},
    {"Age": "23", "Band 1": "6.37", "Band 2": "4.24", "Band 3": "3.04"},
    {"Age": "24", "Band 1": "6.42", "Band 2": "4.29", "Band 3": "3.09"},
    {"Age": "25", "Band 1": "6.47", "Band 2": "4.34", "Band 3": "3.14"},
    {"Age": "26", "Band 1": "6.48", "Band 2": "4.34", "Band 3": "3.14"},
    {"Age": "27", "Band 1": "6.49", "Band 2": "4.35", "Band 3": "3.15"},
    {"Age": "28", "Band 1": "6.49", "Band 2": "4.35", "Band 3": "3.15"},
    {"Age": "29", "Band 1": "6.5", "Band 2": "4.36", "Band 3": "3.16"},
    {"Age": "30", "Band 1": "6.51", "Band 2": "4.36", "Band 3": "3.16"},
    {"Age": "31", "Band 1": "6.62", "Band 2": "4.47", "Band 3": "3.27"},
    {"Age": "32", "Band 1": "6.74", "Band 2": "4.59", "Band 3": "3.39"},
    {"Age": "33", "Band 1": "6.85", "Band 2": "4.7", "Band 3": "3.5"},
    {"Age": "34", "Band 1": "6.97", "Band 2": "4.82", "Band 3": "3.62"},
    {"Age": "35", "Band 1": "7.08", "Band 2": "4.93", "Band 3": "3.73"},
    {"Age": "36", "Band 1": "7.25", "Band 2": "5.1", "Band 3": "3.9"},
    {"Age": "37", "Band 1": "7.42", "Band 2": "5.27", "Band 3": "4.07"},
    {"Age": "38", "Band 1": "7.6", "Band 2": "5.45", "Band 3": "4.25"},
    {"Age": "39", "Band 1": "7.77", "Band 2": "5.62", "Band 3": "4.42"},
    {"Age": "40", "Band 1": "7.94", "Band 2": "5.79", "Band 3": "4.59"},
    {"Age": "41", "Band 1": "8.3", "Band 2": "6.14", "Band 3": "4.94"},
    {"Age": "42", "Band 1": "8.65", "Band 2": "6.49", "Band 3": "5.29"},
    {"Age": "43", "Band 1": "9.01", "Band 2": "6.84", "Band 3": "5.63"},
    {"Age": "44", "Band 1": "9.36", "Band 2": "7.19", "Band 3": "5.98"},
    {"Age": "45", "Band 1": "9.72", "Band 2": "7.54", "Band 3": "6.33"},
    {"Age": "46", "Band 1": "10.2", "Band 2": "8.04", "Band 3": "6.83"},
    {"Age": "47", "Band 1": "10.69", "Band 2": "8.54", "Band 3": "7.33"},
    {"Age": "48", "Band 1": "11.17", "Band 2": "9.03", "Band 3": "7.84"},
    {"Age": "49", "Band 1": "11.66", "Band 2": "9.53", "Band 3": "8.34"},
    {"Age": "50", "Band 1": "12.14", "Band 2": "10.03", "Band 3": "8.84"},
    {"Age": "51", "Band 1": "12.94", "Band 2": "10.81", "Band 3": "9.61"},
    {"Age": "52", "Band 1": "13.75", "Band 2": "11.59", "Band 3": "10.38"},
    {"Age": "53", "Band 1": "14.55", "Band 2": "12.36", "Band 3": "11.15"},
    {"Age": "54", "Band 1": "15.36", "Band 2": "13.14", "Band 3": "11.92"},
    {"Age": "55", "Band 1": "16.16", "Band 2": "13.92", "Band 3": "12.69"},
    {"Age": "56", "Band 1": "16.98", "Band 2": "14.79", "Band 3": "13.57"},
    {"Age": "57", "Band 1": "17.8", "Band 2": "15.66", "Band 3": "14.46"},
    {"Age": "58", "Band 1": "18.62", "Band 2": "16.52", "Band 3": "15.34"},
    {"Age": "59", "Band 1": "19.44", "Band 2": "17.39", "Band 3": "16.23"},
    {"Age": "60", "Band 1": "20.26", "Band 2": "18.26", "Band 3": "17.11"},
    {"Age": "61", "Band 1": "21.85", "Band 2": "19.78", "Band 3": "18.62"},
    {"Age": "62", "Band 1": "23.45", "Band 2": "21.29", "Band 3": "20.12"},
    {"Age": "63", "Band 1": "25.04", "Band 2": "22.81", "Band 3": "21.63"},
    {"Age": "64", "Band 1": "26.64", "Band 2": "24.32", "Band 3": "23.13"},
    {"Age": "65", "Band 1": "28.23", "Band 2": "25.84", "Band 3": "24.64"},
    {"Age": "66", "Band 1": "36.45", "Band 2": "33.1", "Band 3": "31.37"},
    {"Age": "67", "Band 1": "44.68", "Band 2": "40.35", "Band 3": "38.11"},
    {"Age": "68", "Band 1": "52.9", "Band 2": "47.61", "Band 3": "44.84"},
    {"Age": "69", "Band 1": "61.12", "Band 2": "54.86", "Band 3": "51.57"},
    {"Age": "70", "Band 1": "", "Band 2": "", "Band 3": ""}
]

YRCT_10_PREMIUM_RATES_V2 = [
    {"Age": "5", "Band 1": "5.85", "Band 2": "3.65", "Band 3": "2.42"},
    {"Age": "6", "Band 1": "5.86", "Band 2": "3.66", "Band 3": "2.43"},
    {"Age": "7", "Band 1": "5.86", "Band 2": "3.66", "Band 3": "2.43"},
    {"Age": "8", "Band 1": "5.87", "Band 2": "3.67", "Band 3": "2.44"},
    {"Age": "9", "Band 1": "5.87", "Band 2": "3.67", "Band 3": "2.44"},
    {"Age": "10", "Band 1": "5.88", "Band 2": "3.68", "Band 3": "2.45"},
    {"Age": "11", "Band 1": "5.94", "Band 2": "3.75", "Band 3": "2.52"},
    {"Age": "12", "Band 1": "6.01", "Band 2": "3.82", "Band 3": "2.58"},
    {"Age": "13", "Band 1": "6.07", "Band 2": "3.88", "Band 3": "2.65"},
    {"Age": "14", "Band 1": "6.14", "Band 2": "3.95", "Band 3": "2.71"},
    {"Age": "15", "Band 1": "6.20", "Band 2": "4.02", "Band 3": "2.78"},
    {"Age": "16", "Band 1": "6.27", "Band 2": "4.09", "Band 3": "2.85"},
    {"Age": "17", "Band 1": "6.34", "Band 2": "4.15", "Band 3": "2.92"},
    {"Age": "18", "Band 1": "6.40", "Band 2": "4.22", "Band 3": "2.98"},
    {"Age": "19", "Band 1": "6.47", "Band 2": "4.28", "Band 3": "3.05"},
    {"Age": "20", "Band 1": "6.54", "Band 2": "4.35", "Band 3": "3.12"},
    {"Age": "21", "Band 1": "6.57", "Band 2": "4.38", "Band 3": "3.15"},
    {"Age": "22", "Band 1": "6.60", "Band 2": "4.41", "Band 3": "3.18"},
    {"Age": "23", "Band 1": "6.62", "Band 2": "4.45", "Band 3": "3.21"},
    {"Age": "24", "Band 1": "6.65", "Band 2": "4.48", "Band 3": "3.24"},
    {"Age": "25", "Band 1": "6.68", "Band 2": "4.51", "Band 3": "3.27"},
    {"Age": "26", "Band 1": "6.75", "Band 2": "4.58", "Band 3": "3.34"},
    {"Age": "27", "Band 1": "6.82", "Band 2": "4.65", "Band 3": "3.41"},
    {"Age": "28", "Band 1": "6.89", "Band 2": "4.72", "Band 3": "3.48"},
    {"Age": "29", "Band 1": "6.96", "Band 2": "4.79", "Band 3": "3.55"},
    {"Age": "30", "Band 1": "7.03", "Band 2": "4.86", "Band 3": "3.62"},
    {"Age": "31", "Band 1": "7.19", "Band 2": "5.03", "Band 3": "3.79"},
    {"Age": "32", "Band 1": "7.35", "Band 2": "5.19", "Band 3": "3.95"},
    {"Age": "33", "Band 1": "7.52", "Band 2": "5.36", "Band 3": "4.12"},
    {"Age": "34", "Band 1": "7.68", "Band 2": "5.52", "Band 3": "4.28"},
    {"Age": "35", "Band 1": "7.84", "Band 2": "5.69", "Band 3": "4.45"},
    {"Age": "36", "Band 1": "8.12", "Band 2": "5.98", "Band 3": "4.74"},
    {"Age": "37", "Band 1": "8.40", "Band 2": "6.27", "Band 3": "5.03"},
    {"Age": "38", "Band 1": "8.69", "Band 2": "6.56", "Band 3": "5.32"},
    {"Age": "39", "Band 1": "8.97", "Band 2": "6.85", "Band 3": "5.61"},
    {"Age": "40", "Band 1": "9.25", "Band 2": "7.14", "Band 3": "5.90"},
    {"Age": "41", "Band 1": "9.71", "Band 2": "7.61", "Band 3": "6.37"},
    {"Age": "42", "Band 1": "10.17", "Band 2": "8.08", "Band 3": "6.84"},
    {"Age": "43", "Band 1": "10.64", "Band 2": "8.56", "Band 3": "7.32"},
    {"Age": "44", "Band 1": "11.10", "Band 2": "9.03", "Band 3": "7.79"},
    {"Age": "45", "Band 1": "11.56", "Band 2": "9.50", "Band 3": "8.26"},
    {"Age": "46", "Band 1": "12.24", "Band 2": "10.20", "Band 3": "8.95"},
    {"Age": "47", "Band 1": "12.91", "Band 2": "10.89", "Band 3": "9.65"},
    {"Age": "48", "Band 1": "13.59", "Band 2": "11.59", "Band 3": "10.34"},
    {"Age": "49", "Band 1": "14.26", "Band 2": "12.28", "Band 3": "11.04"},
    {"Age": "50", "Band 1": "14.94", "Band 2": "12.98", "Band 3": "11.73"},
    {"Age": "51", "Band 1": "15.87", "Band 2": "13.94", "Band 3": "12.68"},
    {"Age": "52", "Band 1": "16.80", "Band 2": "14.89", "Band 3": "13.64"},
    {"Age": "53", "Band 1": "17.74", "Band 2": "15.85", "Band 3": "14.59"},
    {"Age": "54", "Band 1": "18.67", "Band 2": "16.80", "Band 3": "15.55"},
    {"Age": "55", "Band 1": "19.60", "Band 2": "17.76", "Band 3": "16.50"},
    {"Age": "56", "Band 1": "20.94", "Band 2": "19.14", "Band 3": "17.88"},
    {"Age": "57", "Band 1": "22.29", "Band 2": "20.52", "Band 3": "19.25"},
    {"Age": "58", "Band 1": "23.63", "Band 2": "21.90", "Band 3": "20.63"},
    {"Age": "59", "Band 1": "24.98", "Band 2": "23.28", "Band 3": "22.00"},
    {"Age": "60", "Band 1": "26.32", "Band 2": "24.66", "Band 3": "23.38"},
    {"Age": "61", "Band 1": "28.40", "Band 2": "26.78", "Band 3": "25.49"},
    {"Age": "62", "Band 1": "30.48", "Band 2": "28.91", "Band 3": "27.60"},
    {"Age": "63", "Band 1": "32.57", "Band 2": "31.03", "Band 3": "29.72"},
    {"Age": "64", "Band 1": "34.65", "Band 2": "33.16", "Band 3": "31.83"},
    {"Age": "65", "Band 1": "36.73", "Band 2": "35.28", "Band 3": "33.94"},
    {"Age": "66", "Band 1": "40.43", "Band 2": "39.08", "Band 3": "37.73"},
    {"Age": "67", "Band 1": "44.13", "Band 2": "42.88", "Band 3": "41.52"},
    {"Age": "68", "Band 1": "47.84", "Band 2": "46.68", "Band 3": "45.31"},
    {"Age": "69", "Band 1": "51.54", "Band 2": "50.48", "Band 3": "49.10"},
    {"Age": "70", "Band 1": "53.75", "Band 2": "52.84", "Band 3": "51.51"}
]


def render_mail(
        subject,
        template_prefix,
        context,
        recipient_list,
        bcc=[],
        attachment_name='',
        attachment_file=None,
        attachment_type='',
):
    bodies = {}
    for ext in ['html', 'txt']:
        template_name = '{}.{}'.format(template_prefix, ext)
        bodies[ext] = render_to_string(template_name, context).strip()

    email = EmailMultiAlternatives(
        subject=subject,
        body=bodies['txt'],
        from_email=SUPPORT_EMAIL,
        to=recipient_list,
        bcc=bcc,
    )
    email.attach_alternative(bodies['html'], 'text/html')

    if attachment_file:
        email.attach(attachment_name, attachment_file, attachment_type)

    return email


def generate_application_form_pdf(application_number):
    # ported from cocolife/views/application_form.py
    try:
        beneficiaries = [0, 1, 2, 3, 4, 5]

        productInsuree = ProductInsuree.objects.all()
        clQuestions = CLHealthQuestions.objects.all()
        clAnswers = CLHealthQuestionsAnswers.objects.all().values(
            'answer'
        )
        cocoInsuree = DigiInsuree.objects.all()
        beneficiary = Beneficiary.objects.all().values(
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
            'benefit_type', )
        # beneficiary = Beneficiary.objects.all().values(
        #     'full_name',
        #     'address',
        # )

        clQuestionsQ = clQuestions.values('question')
        product_Insuree = productInsuree.values(
            'id',
            'billed_to_id',
            'product_id__name',
            'product__coverage_amount_max',
            'package_id__name',
            'payment_term',
            'coverage_term',
            # 'indicia',
            # 'no_indicia',
            # 'not_us_person',
            # 'us_person',
        ).filter(application_number=application_number)[0]

        product_insuree_index = product_Insuree['id']
        product_insuree_ID = product_Insuree['billed_to_id']
        product_insuree_package = product_Insuree['package_id__name']
        product_insuree_face_amount = product_Insuree['product__coverage_amount_max']
        product_insuree_premium_mode = product_Insuree['payment_term']
        product_insuree_coverage_term = product_Insuree['coverage_term']
        product_insuree_ID = product_Insuree['billed_to_id']

        # FATCA (Not yet implemented)

        # fatca_indicia = product_Insuree['indicia']
        # fatca_no_indicia = product_Insuree['no_indicia']
        # fatca_not_us_person = product_Insuree['not_us_person']
        # fatca_us_person = product_Insuree['us_person']

        # print(pID)
        insuree = cocoInsuree.values(  # Fetch person insured's packaged insurance
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
        ).filter(user_id=product_insuree_ID)[0]

        coco_user_id = cocoInsuree.get(user_id=product_insuree_ID)
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

        birthdayQ = cocoInsuree.all().values('birthday').filter(
            user_id=product_insuree_ID)[0]  # Insuree's Birthday

        birthday = birthdayQ['birthday']

        birthdate = datetime.date(
            birthday.year,
            birthday.month,
            birthday.day
        )
        age = coco_user_id.get_age()

        questionIfAdult = clQuestionsQ.filter(is_adult=1).order_by('id')[0:7]
        questionIfNotAdult = clQuestionsQ.filter(is_adult=0).order_by('id')

        beneficiary = beneficiary.filter(
            product_insuree_id=product_insuree_index).order_by('id')[0:5]
        answerIfAdult = clAnswers.filter(
            ProdInsuree_id=product_insuree_index, question_id__lte=7).order_by('id')
        answerIfNotAdult = clAnswers.filter(
            ProdInsuree_id=product_insuree_index, question_id__lte=7).order_by('id')

        questionIfAdult_Arr = []
        questionIfNotAdult_Arr = []

        answerIfAdult_Arr = []
        answerIfNotAdult_Arr = []

        for questions in questionIfAdult:
            questionIfAdult_Arr.append(questions['question'])

        for questions in questionIfNotAdult:
            questionIfNotAdult_Arr.append(questions['question'])

        for answers in answerIfAdult:
            answerIfAdult_Arr.append(answers['answer'])

        for answers in answerIfNotAdult:
            answerIfNotAdult_Arr.append(answers['answer'])

        data = {  # Data passed to form
            'loop': beneficiaries,
            'id': application_number,
            # Questions
            'questionIfAdult': questionIfAdult_Arr,
            'questionIfNotAdult': questionIfNotAdult_Arr,
            # Cocoinsuree/Policy Owner Data
            'firstName': policyO_Fname,
            'middleName': policyO_Mname,
            'lastName': policyO_Lname,
            'email': policyO_Email,
            'gender': policyO_Gender,
            # 'birthday': birthday,
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
            # Application Data
            'package': product_insuree_package,
            'face_amount': product_insuree_face_amount,
            'coverage_term': product_insuree_coverage_term,
            'premium_mode': product_insuree_premium_mode,
            # Beneficiaries
            'beneficiary': beneficiary,
            # Health Declaration
            'answerIfAdult': answerIfAdult_Arr,
            'answerIfNotAdult': answerIfNotAdult_Arr,
        }

        # Template from cocolife/templates
        template = get_template('applicationForm2022.html')
        data_p = template.render(data)
        response = BytesIO()
        pdf_page = pisa.pisaDocument(
            BytesIO(data_p.encode('UTF-8')), response
        )

        if pdf_page.err:
            return

        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        filename = 'application_form_%s.pdf' % (application_number)
        content = 'inline; filename=%s' % (filename)
        # content = 'attachment; filename=%s' % (filename)
        response['Content-Disposition'] = content
        return response.content
    except Exception as e:
        print(e)
        return
