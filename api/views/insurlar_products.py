
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

__all__ = ['InsularProducts']


class InsularProducts(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        bigDict = [
            {
                "category": "ALLIN",
                "product_name": "ER Care All-In 80 Adults",
                "product_code": "SKU:ERCAI80A",
                "desciption": "This one-time use health care voucher provides up to Php 80,000 worth of coverage for emergency cases due to accidents and viral and bacterial illnesses and specific conditions. Services include outpatient and inpatient emergency care, semi-private room use, laboratory and diagnostic procedures, and medicines as medically required. It is accepted in more than 500 IHC-accredited hospitals nationwide excluding *Top 6 hospitals.",
                "price" : "1,350.00",
                "add_ons": "Add Top 6 Hospital Access",
                "availability" : "in stock"
            },
            {
                "category": "ALLIN",
                "product_name": "Total ProtectER",
                "product_code": "SKU:ERCAIXIL",
                "desciption": "Total ProtectER is a total protection package composed of a term insurance product with a daily hospital income benefit for a six-month coverage; and a one-time use health care voucher that provides up to Php100,000 worth of coverage for emergency cases due to accidents and viral and bacterial illnesses and specific conditions.",
                "price" : "11,750.00",
                "add_ons": "Add Top 6 Hospital Access",
                "availability" : "in stock"
            },
            {
                "category": "BOOSTER",
                "product_name": "ER Care Booster 60",
                "product_code": "SKU:ERCBT60",
                "desciption": "This one-time use health care voucher provides up to Php 60,000 worth of coverage for emergency cases due to accidents. Services include outpatient and inpatient emergency care, ward room use, laboratory and diagnostic procedures, and medicines as medically required. It is accepted in more than 500 IHC-accredited hospitals nationwide excluding the *Top 6 hospitals.",
                "price" : "800.00",
                "add_ons": "Add Top 6 Hospital Access",
                "availability" : "in stock"
            },
            {
                "category": "MEDCONSULT",
                "product_name": "MedConsult Kids",
                "product_code": "SKU:MCK",
                "desciption": "This multiple-use health voucher provides a range of consultation services with IHC-accredited medical specialists and dentists and access to telemedicine. Services include face-to-face outpatient medical consultations with IHC-accredited pediatricians nationwide.",
                "price" : "3,000.00",
                "add_ons": "Add Top 6 Hospital Access",
                "availability" : "in stock"
            },
            {
                "category": "ERCARECHOICE",
                "product_name": "ER Care Choice 30",
                "product_code": "SKU:ERCC30",
                "desciption": "This one-time use health care voucher provides up to Php 30,000 worth of coverage for emergency cases due to accidents, viral & bacterial illnesses, and specific conditions. Services include outpatient and inpatient emergency care, laboratory and diagnostic procedures, and medicines as medically required. It is accepted in more than 500 IHC-accredited hospitals nationwide including the *Top 6 hospitals.",
                "price" : "100.00",
                "add_ons": {
                    1: "30 Days Validity",
                    2: "60 Days Validity",
                    3: "90 Days Validity",
                },
                "availability" : "in stock"
            },
            {   
                "category": "SHESWELL",
                "product_name": "SHE'S WELL - LILY",
                "product_code": "SKU:SWLILY",
                "desciption": "This health voucher that covers a range of diagnostic procedures and laboratory tests for girls, 18 years old and below. Includes hospital coverage for emergency cases due to accidents and a 1-year unlimited access to telemedicine/remote medical consultation with MyPocketDoctor.",
                "price" : "8,300.00",
                "add_ons": "N/A",
                "availability" : "in stock"
            },

            

        ]

        return Response(bigDict)
