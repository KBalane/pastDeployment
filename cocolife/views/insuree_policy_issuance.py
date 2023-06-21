from cocolife.serializers.InsureePolicyIssuanceSerializer import InsureePolicyIssuanceSerializer
from django.http.response import Http404
from digiinsurance.models import InsureePolicy
from cocolife.models import InsureePolicyIssuanceSettings
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView


from django.http import HttpResponse

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  

from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from rest_framework.permissions import AllowAny


__all__ = ['InsureePolicyPDFSettings', 'InsureePolicyPDFIssuance','UpdateInsureePolicyPDFSettings']




class InsureePolicyPDFSettings(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = InsureePolicyIssuanceSettings.objects.all()
    serializer_class = InsureePolicyIssuanceSerializer

class UpdateInsureePolicyPDFSettings(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = InsureePolicyIssuanceSettings.objects.all()
    serializer_class = InsureePolicyIssuanceSerializer
    lookup_field = 'pk'


class InsureePolicyPDFIssuance(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id):
        try:
            company_policy = InsureePolicyIssuanceSettings.objects.all().values(
                'policy',
                'status',
                'premium_amount_due',
                'premium_date_due',
                'premium_last_paid',
                'premium_last_date' ,
                'policy_type',
                'policy_type2',
                'active_premium_interval',
                'Currency',    
            )[0]
        except IndexError as e:
            raise Http404

        valuelist = []
        for (key, value) in company_policy.items():
            if key == 'policy':
                key = key + '__name'
            if value == True:
                valuelist.append(key)

        insuree_policy = list(InsureePolicy.objects.filter(insuree_id = id).values(*valuelist))
        name = InsureePolicy.objects.all().values_list(
                'insuree').annotate(name=Concat(
                    'insuree__first_name',
                    V(' '), 'insuree__last_name', V(''),
                    output_field=CharField()
                    )).filter(insuree_id = id).first()
        data = {
            'valuelist' : valuelist,
            'name': name[1],
            'insuree_policy' : insuree_policy
        }
        template = get_template('cl_policy_issuance.html')
        data_p=template.render(data)
        response = BytesIO()
        pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
        if not pdf_page.err:
            #return HttpResponse(response.getvalue(), content_type='application/pdf')
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            filename = "company_policy_invoice_%s.pdf" %(id)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            #if download: #to enable viewing functionality, uncomment this line and indent the next line.
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        else:
            return HttpResponse("Error Generating PDF")  