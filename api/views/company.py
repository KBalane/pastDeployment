from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView


from api.serializers.CompanySerializer import CompanySerializer, CompanyRequirementsSerializer
from rest_framework.permissions import AllowAny
from digiinsurance.models.Company import Company
from digiinsurance.models.CompanyRequirements import CompanyRequirements


from rest_framework.response import Response
from rest_framework import status


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer


#    filter_backends = (DjangoFilterBackend,)
#    filter_fields = ('name', )


class CompanyRequirementsList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CompanyRequirementsSerializer

    def get_queryset(self):
        company_req_id = self.kwargs['id']
        return CompanyRequirements.objects.filter(company=company_req_id)


class CompanyRequirementsPost(CreateAPIView):
    permission_classes = (AllowAny,)

    queryset = CompanyRequirements.objects.all()
    serializer_class = CompanyRequirementsSerializer


class CompanyList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Company.objects.all().order_by('-id')
    serializer_class = CompanySerializer


class CompanyCreate(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer


class CompanyUpdate(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer


class UpdateCompanyRequirements(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = CompanyRequirements.objects.all().order_by('id')
    serializer_class = CompanyRequirementsSerializer

    # def delete(self, request, id):
    #     try:
    #         instance = self.queryset.get(id=id)
    #         self.perform_destroy(instance)
    #         return Response("DELETED")
    #     except:
    #         raise Http404("No matching Company Requirement found")


class PhotoCompanyUpdate(APIView):

    def put(self, request, id):
        queryset = Company.objects.all().values_list('logo', 'cover').filter(id=id)
        path_logo = "%d/logo/" % id
        path_cover = "%d/cover/" % id

        # If no data passed get existing data from DB 
        if request.data.get('logo') == None:
            logo = queryset[0][0]
        else:
            logo = request.data.get('logo')
            logo = path_logo + str(logo)

        if request.data.get('cover') == None:
            cover = queryset[0][1]
        else:
            cover = request.data.get('cover')
            cover = path_cover + str(cover)

        update = Company.objects.all().values('id').update(
            logo=logo,
            cover=cover
        )

        return Response(status=status.HTTP_200_OK)


class CompanyFaqDetails(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        company_faq_details = Company.objects.all().values(
            'id',
            'email',
            'mobile_number'
        )

        context = {
            'company_faq_details': company_faq_details
        }

        return Response(context)
