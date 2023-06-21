from cocolife.serializers.ProductSerializer import ProductProposalSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from cocolife.models.Product import *
from decimal import Decimal
from rest_framework.permissions import AllowAny
from cocolife.utils import ART_PREMIUM_RATES_V2, YRCT_10_PREMIUM_RATES_V2

__all__ = ['GetProductProposal', 'YRCT10']


class GetProductProposal(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ProductProposalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            package = Package.objects.filter(id=serializer.data['package']).values()[0]
            benefits = Benefit.objects.filter(
                variant=serializer.data['variant']).values()

            benef_arr = []
            amounts_arr = []
            for item in benefits:
                amounts_arr.append('{:.2f}'.format(item['face_amount']))
                benef_arr.append(item['name'])

            for item in ART_PREMIUM_RATES_V2:  # Reference for the ART Static Values
                if item['Age'] == '5':
                    print(item['Band 2'])
                """ for x in item:
                    print(x) """

            # query prems by term and by age,
            premiums = Premium.objects.filter(
                variant=serializer.data['variant'], coverage_term=serializer.data['coverage_term'],
                age_max__gte=serializer.data['age'], age_min__lte=serializer.data['age']).values()[0]

            if serializer.data['payment_term'] == 'monthly':
                amount = premiums['value'] * Decimal(0.0975)
            elif serializer.data['payment_term'] == 'quarterly':
                amount = premiums['value'] * Decimal(0.2750)
            elif serializer.data['payment_term'] == 'semi annual':
                amount = premiums['value'] * Decimal(0.5300)
            else:
                amount = premiums['value']

            data = {
                "package_name": package['name'],
                "benefits": benef_arr,
                "face_amounts": amounts_arr,
                "payment_term": serializer.data['payment_term'],
                "premium": '{:.2f}'.format(amount)
            }
            # if user chooces to proceed with application, resend info, as product insuree.
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YRCT10(APIView):
    def get(self, request, age, face_amount):

        # print(YRCT_PREMIUM_RATES[0])
        # face_amount = 500000  # C6 500k, 1M
        # api/v1/cocolife/yrct10/31/500000/

        age = age
        face_amount = face_amount
        band_chosen = ''
        if (face_amount <= 500000):
            band_chosen = 'Band 1'
        elif ((face_amount > 500000) and (face_amount <= 1000000)):
            band_chosen = 'Band 2'
        str_age = str(age)
        # loop 20 times for age if term shield 1 (optional)
        rate = 0
        # if 500k, band 1. if 1m, band 2. no 2m/band 3 available right now.
        for item in YRCT_10_PREMIUM_RATES_V2:
            if item['Age'] == str_age:  # + '.00':  # and whatever band chosen
                rate = item[band_chosen]  # G7
        annual = face_amount * float(rate) / 1000  # H7
        semi_annual = round(annual * 0.53, 2)
        quarterly = round(annual * 0.275, 2)
        monthly = round(annual * 0.0975, 2)

        # pf = Policy Fee
        pf_annual = 400  # H8
        pf_semi = round(pf_annual * 0.53, 2)
        pf_qtr = round(pf_annual * 0.275, 2)
        pf_mon = round(pf_annual * 0.0975, 2)

        total_annual = annual + pf_annual
        total_semi = semi_annual + pf_semi
        total_qtr = quarterly + pf_qtr
        total_mon = monthly + pf_mon

        res = {
            "plan": "Term Shield 10 (10 YRCT)",
            "issue_age": age,
            "face_amount": face_amount,

            "rate": rate,
            "annual": annual,
            "semi_annual": semi_annual,
            "quarterly": quarterly,
            "monthly": monthly,

            "pf_annual": pf_annual,
            "pf_semi": pf_semi,
            "pf_qtr": pf_qtr,
            "pf_mon": pf_mon,

            "total_annual": total_annual,
            "total_semi": total_semi,
            "total_qtr": total_qtr,
            "total_mon": total_mon,

        }
        return Response(res)
