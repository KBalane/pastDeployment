from decimal import Decimal
from cocolife.models.Product import Package, Benefit, Premium
from cocolife.utils import ART_PREMIUM_RATES_V2, YRCT_10_PREMIUM_RATES_V2
from cocolife.constants import PAYMENT_TERM_MULTIPLIER, POLICY_FEE
from datetime import date, datetime


def calculate_age(birthdate):
    birth_date = datetime.strptime(birthdate, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


class PremiumCalculator:

    def __init__(self, *args, **kwargs):
        self.package = kwargs.get('package')
        self.variant = kwargs.get('variant')
        self.payment_term = kwargs.get('payment_term')
        self.coverage_term = kwargs.get('coverage_term')
        self.age = kwargs.get('age')

    def get_package(self):
        return Package.objects.filter(id=self.package).values('product__name', 'name', 'description')[0]

    def get_benefits(self):
        benefits = Benefit.objects.filter(variant=self.variant).values()
        return [x['name'] for x in benefits]

    def get_face_amounts(self):
        benefits = Benefit.objects.filter(variant=self.variant).values()
        return [x['face_amount'] for x in benefits]

    @staticmethod
    def get_band(face_amount):
        """helper method for get_premium"""
        if face_amount <= 500000:
            band = 'Band 1'
        elif (face_amount > 500000) and (face_amount <= 1000000):
            band = 'Band 2'
        else:
            band = 'Band 3'
        return band

    def get_premium(self):
        package = self.get_package()
        face_amount = self.get_face_amounts()

        if package['product_name'] == 'Term Shield':
            band = self.get_band(face_amount[0])

            for item in (ART_PREMIUM_RATES_V2 if (package['name'] == 'Annual Renewable Term Plan')
            else YRCT_10_PREMIUM_RATES_V2):
                if item['Age'] == self.age:
                    rate = Decimal(item[band])

            annual = face_amount[0] * Decimal(rate) / 1000
            premium = annual * PAYMENT_TERM_MULTIPLIER[self.payment_term]

        else:
            rate = Premium.objects.filter(variant=self.variant, coverage_term=self.coverage_term,
                                          age_max__gte=self.age, age_min__lte=self.age).values()[0]['value']
            premium = rate * PAYMENT_TERM_MULTIPLIER[self.payment_term]
        return premium

    def get_policy_fee(self):
        policy_fee = 0
        if self.get_package()['product_name'] == 'Term Shield':
            policy_fee = POLICY_FEE * PAYMENT_TERM_MULTIPLIER[self.payment_term]
        return policy_fee

    def get_document_stamp_tax(self):
        face_amount = self.get_face_amounts()[0]
        if face_amount < 100000:
            document_tax = Decimal(50.00)
        elif face_amount > 100000 and face_amount <= 300000:
            document_tax = Decimal(20.00)
        elif face_amount > 300000 and face_amount <= 500000:
            document_tax = Decimal(50.00)
        elif face_amount > 500000 and face_amount <= 750000:
            document_tax = Decimal(100.00)
        elif face_amount > 750000 and face_amount <= 100000000:
            document_tax = Decimal(150.00)
        elif face_amount > 100000000:
            document_tax = Decimal(200.00)

        return document_tax

    def get_delivery_fee(self):
        return Decimal(0.00)

    def get_total_fee(self):
        total = self.get_premium() + self.get_policy_fee() + self.get_document_stamp_tax() + self.get_delivery_fee()
        return total

    def get_result_dictionary(self):
        return {
            'package_name': self.get_package()['name'],
            'benifits': self.get_benefits(),
            'face-ammounts': self.get_face_amounts(),
            'payment_term': self.payment_term,
            'premium': self.get_premium(),
            'policy_fee': self.get_policy_fee(),
            'document_stamp_tax': self.get_document_stamp_tax(),
            'delivery_fee': self.get_delivery_fee(),
            'total': self.get_total_fee()
        }
