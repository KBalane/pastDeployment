from rest_framework import viewsets, generics
from rest_framework.response import Response

from api.serializers.UpdateBeneficiarySerializer import (BeneficiaryUpdateSerializer, BeneficiaryDeleteSerializer,
                                                         GetBeneficiaryInfoSerilizer, BeneficiaryListSerializer,
                                                         BeneficiaryGetPendingUpdates, BeneficiaryJSONIDSerializer)

from api.serializers.BeneficiarySerializer import TempBeneficiarySerializer, BeneficiarySerializer
from rest_framework.generics import (RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, ListCreateAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.views import APIView

from digiinsurance.models.Beneficiaries import Beneficiaries
from digiinsurance.models.TempBeneficiaries import TempBeneficiaries
from digiinsurance.models.InsureePolicy import InsureePolicy
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models import Q


__all__ = ['AdminGetSpecificBeneficiaryInfo', 'ToDelete', 'DenyBeneficiary',
           'ApproveBeneficiary', 'PendingBeneficiaries', 'BeneficiariesList', 'BeneficiariesUpdate',
           'BeneficiariesDelete', 'GetBeneficiaryInfo', 'GetSpecificBeneficiaryInfo', 'BeneficiaryUpdate2',
           'BeneficiariesStatus', 'BeneficiaryRequestUpdate', 'BeneficiaryRequestDelete',
           'BeneficiaryApproveUpdate3', 'BeneficiaryApproveDelete3', 'BeneficiaryDenyDelete3', 'NewBeneficiary',
           'BeneficiaryDenyUpdate3']


class BeneficiariesList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Beneficiaries.objects.all().order_by('-user_policy')
    serializer_class = BeneficiaryListSerializer

    def get_queryset(self):
        queryset = Beneficiaries.objects.all().order_by('-user_policy')
        user = self.request.query_params.get('user_policy')
        if user:
            queryset = queryset.filter(user_policy=user)
        return queryset


class BeneficiariesStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        queryset = Beneficiaries.objects.all().values(
            'id',
            'beneficiary_status',
            'request_type',
            # 'user_policy_id',
            # 'first_name',
            # 'middle_name',
            # 'last_name',
            # 'birthday',
            # 'birthplace',
            # 'country',
            # 'nationality',
            # 'beneficiary_address',
            # 'relationship',

        ).filter(id=id)
        return Response(queryset)


class BeneficiariesUpdate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryUpdateSerializer


class BeneficiariesDelete(APIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryDeleteSerializer

    def get(self, request, id):
        query = TempBeneficiaries.objects.all().values('beneficiary', 'reason').filter(beneficiary=id)
        return Response(query[0])

    def delete(self, request, id, **kwargs):
        try:

            ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
            ifexists.delete()
        except Exception:
            pass
        return super().delete(request, **kwargs)


class GetBeneficiaryInfo(generics.ListAPIView):
    permissions_classes = (IsAuthenticated,)
    serializer_class = GetBeneficiaryInfoSerilizer

    def get_queryset(self):
        insuree_id = self.kwargs['insuree_id']
        return Beneficiaries.objects.filter(user_policy=insuree_id)


class GetSpecificBeneficiaryInfo(APIView):
    permissions_classes = (IsAuthenticated,)

    # serializer_class=GetBeneficiaryInfoSerilizer

    def get(self, request, insuree_id):
        queryset = Beneficiaries.objects.all().values(
            'user_policy_id',
            'user_policy__insuree',
            'first_name',
            'middle_name',
            'last_name',
            'birthday',
            'birthplace',
            'country',
            'nationality',
            'beneficiary_address',
            'relationship').filter(user_policy__insuree=insuree_id)

        return Response(queryset)

    # class PendingBeneficiaries(ListAPIView):


#     queryset = Beneficiaries.objects.all().filter(beneficiary_status = 'PENDING')
#     serializer_class = GetBeneficiaryInfoSerilizer

class PendingBeneficiaries(APIView):
    def get(self, request, requestType):
        if requestType.lower() == 'update':
            queryset = Beneficiaries.objects.filter(beneficiary_status='PENDING', request_type=requestType).order_by(
                '-created_at')
            serializer_class = BeneficiaryJSONIDSerializer(queryset, many=True)
        elif requestType.lower() == 'add':
            queryset = Beneficiaries.objects.filter(beneficiary_status='PENDING', request_type=requestType).order_by(
                '-created_at')
            serializer_class = BeneficiaryListSerializer(queryset, many=True)
        elif requestType.lower() == 'remove':
            queryset = Beneficiaries.objects.filter(beneficiary_status='PENDING', request_type=requestType).order_by(
                '-created_at')
            serializer_class = BeneficiaryListSerializer(queryset, many=True)
        else:
            pass
            # #get all approved beneficiary for (add requests)
            # queryset2 = Beneficiaries.objects.all().filter(Q(beneficiary_status = 'APPROVED') & Q(request_type = requestType)).order_by('-created_at')
            # serializer_class2 = BeneficiaryListSerializer(queryset2, many = True)

        context = {
            "pending_beneficiaries": serializer_class.data,
            # "approved_beneficiaries":serializer_class2.data,
        }
        return Response(context)


class ApproveBeneficiary(APIView):
    def get(self, request, id):
        update = Beneficiaries.objects.filter(id=id).update(beneficiary_status="APPROVED")
        return Response(update)


class ToDelete(APIView):
    def put(self, request, id):
        try:

            update = Beneficiaries.objects.filter(id=id).update(request_type="Delete", beneficiary_status="PENDING")

            try:
                ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
                ifexists.delete()
            except Exception:
                pass

            birthday = Beneficiaries.objects.values_list('birthday').filter(id=id)
            birthplace = Beneficiaries.objects.values_list('birthplace').filter(id=id)
            country = Beneficiaries.objects.values_list('country').filter(id=id)
            nationality = Beneficiaries.objects.values_list('nationality').filter(id=id)
            beneficiary_address = Beneficiaries.objects.values_list('beneficiary_address').filter(id=id)
            first_name = Beneficiaries.objects.values_list('first_name').filter(id=id)
            middle_name = Beneficiaries.objects.values_list('middle_name').filter(id=id)
            last_name = Beneficiaries.objects.values_list('last_name').filter(id=id)
            relationship = Beneficiaries.objects.values_list('relationship').filter(id=id)
            percentage_of_share = Beneficiaries.objects.values_list('percentage_of_share').filter(id=id)

            queryset = Beneficiaries.objects.all().values_list('user_policy_id').filter(id=id)
            user_policy_inst = InsureePolicy.objects.get(id=queryset[0][0])

            beneficiariesData = Beneficiaries.objects.filter(id=id)

            tempData = TempBeneficiaries.objects.create(
                beneficiary=id,
                birthplace=birthplace,
                country=country,
                birthday=birthday,
                nationality=nationality,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                relationship=relationship,
                percentage_of_share=percentage_of_share,
                beneficiary_address=beneficiary_address,
                reason=request.data.get('reason'),
                request='delete',
                user_policy=user_policy_inst
            )

            # tempData.save()
        except Exception:
            update = "No reason entered."

        return Response(update)


class DenyBeneficiary(APIView):
    def get(self, request, id):
        update = Beneficiaries.objects.filter(id=id).update(beneficiary_status="DENIED")
        ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
        ifexists.delete()
        return Response(update)


class AdminGetSpecificBeneficiaryInfo(APIView):
    # serializer_class=GetBeneficiaryInfoSerilizer

    def get(self, request, id):
        queryset = Beneficiaries.objects.all().values(
            'user_policy_id',
            'user_policy__insuree',
            'first_name',
            'middle_name',
            'last_name',
            'birthday',
            'birthplace',
            'country',
            'nationality',
            'beneficiary_address',
            'relationship',
            'user_policy__policy__category',
            'user_policy__policy_type2',
        ).filter(id=id)

        return Response(queryset)


def view(id):
    beneficary_before = Beneficiaries.objects.all().values(
        'user_policy__insuree',
        'user_policy__insuree__first_name',
        'user_policy__insuree__middle_name',
        'user_policy__insuree__last_name',
        'modified_at',

        'user_policy__policy__name',
        'user_policy_id',
        'user_policy__insuree',

        # beneficiary before
        'first_name',
        'middle_name',
        'last_name',
        'beneficiary_status',
        'request_type',
        'birthplace',
        'country',
        'birthday',
        'nationality',
        'beneficiary_address',

    ).filter(id=id)

    beneficary_after = TempBeneficiaries.objects.all().values(
        'beneficiary',
        'user_policy',
        'first_name',
        'middle_name',
        'last_name',
        'relationship',
        'birthday',
        'birthplace',
        'nationality',
        'country',
        'beneficiary_address',
        'percentage_of_share',
        'reason'
    ).filter(beneficiary=id)

    context = {
        "beneficary_before": beneficary_before,
        "beneficary_after": beneficary_after,
    }
    return Response(context)


class BeneficiaryUpdate2(APIView):
    '''
    To make initial changes, use put.
    To approve a pending change, use post. You won't be able to post without making any changes first.
    
    To deny a pending change, use delete.
    
    Sample put/post request:
    {
            "first_name": "Clyde",
            "middle_name": "C",
            "last_name": "Cornes",
            "relationship": "Brother",
            "birthplace": "Osaka Osaka",
            "country": "Ph",
            "birthday": "1600-05-08",
            "nationality": "Ph",
            "beneficiary_address": "312 Osaka Shiyahahuhaji",
            "reason":"Why are we even living?",
            "percentage_of_share": "69.00"
    }
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        queryset = TempBeneficiaries.objects.all().filter(beneficiary=id)
        serializer_class = TempBeneficiarySerializer(queryset, many=True)

        queryset2 = Beneficiaries.objects.all().filter(id=id)
        serializer_class2 = BeneficiarySerializer(queryset2, many=True)

        context = {
            "beneficary_before": serializer_class.data,
            "beneficary_after": serializer_class2.data,
        }
        return Response(context)

    def put(self, request, id):

        users = Beneficiaries.objects.all().values(
            'first_name',
            'middle_name',
            'last_name',
            'relationship',
            'birthday',
            'birthplace',
            'nationality',
            'country',
            'beneficiary_address',
            'percentage_of_share',
            'user_policy',

        ).filter(id=id).update(
            beneficiary_status='Pending',
            request_type='Update',
        )

        try:
            # this deletes and overwrites the previous pending changes
            # if pending changes still exist
            ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
            ifexists.update(
                beneficiary_status='PENDING',
                request='Update'
            )
        except Exception:
            pass

        tempData = TempBeneficiaries.objects.create(
            beneficiary=id,
            user_policy=InsureePolicy.InsureePolicy.objects.get(user_policy=id),
            first_name=request.data.get('first_name'),
            middle_name=request.data.get('middle_name'),
            last_name=request.data.get('last_name'),
            relationship=request.data.get('relationship'),
            birthplace=request.data.get('birthplace'),
            country=request.data.get('country'),
            birthday=request.data.get('birthday'),
            nationality=request.data.get('nationality'),
            beneficiary_address=request.data.get('beneficiary_address'),
            percentage_of_share=request.data.get('percentage_of_share'),
            reason=request.data.get('reason'),
            request='update',
        )

        return view(id)

    def post(self, request, id):  # approve
        try:
            first_name = TempBeneficiaries.objects.values_list('first_name').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            middle_name = TempBeneficiaries.objects.values_list('middle_name').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            last_name = TempBeneficiaries.objects.values_list('last_name').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            relationship = TempBeneficiaries.objects.values_list('relationship').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            birthplace = TempBeneficiaries.objects.values_list('birthplace').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            country = TempBeneficiaries.objects.values_list('country').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            birthday = TempBeneficiaries.objects.values_list('birthday').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            nationality = TempBeneficiaries.objects.values_list('nationality').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            beneficiary_address = TempBeneficiaries.objects.values_list('beneficiary_address').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            percentage_of_share = TempBeneficiaries.objects.values_list('percentage_of_share').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            user_policy = TempBeneficiaries.objects.values_list('user_policy').filter(
                Q(beneficiary=id) & Q(request='update') & Q(beneficiary_status='PENDING'))
            users = Beneficiaries.objects.all().values(
                'first_name',
                'middle_name',
                'last_name',
                'relationship',
                'birthday',
                'birthplace',
                'nationality',
                'country',
                'beneficiary_address',
                'percentage_of_share',
                'user_policy',
            ).filter(id=id).update(
                first_name=first_name[0][0],
                middle_name=middle_name[0][0],
                last_name=last_name[0][0],
                relationship=relationship[0][0],
                birthday=birthday[0][0],
                birthplace=birthplace[0][0],
                nationality=nationality[0][0],
                country=country[0][0],
                beneficiary_address=beneficiary_address[0][0],
                percentage_of_share=percentage_of_share[0][0],
                user_policy=user_policy[0][0],
                beneficiary_status='APPROVED',
                request_type='Update',
            )

            ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
            ifexists.delete()
        except Exception:
            return Response("Please make changes first.")

        return Response("Beneficiary Approved")

    def delete(self, request, id):  # deny
        users = Beneficiaries.objects.all().values(
            'first_name',
            'middle_name',
            'last_name',
            'relationship',
            'birthplace',
            'country',
            'birthday',
            'nationality',
            'beneficiary_address',
            'percentage_of_share',
            'user_policy',
        ).filter(id=id).update(
            beneficiary_status='DENIED',
            request_type='Update',
        )

        try:
            ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
            ifexists.delete()
        except Exception:
            pass

        return Response("Beneficiary Denied")


class BeneficiaryRequestUpdate(APIView):
    """
    Endpoint to request update for beneficiary. Request is approved/rejected by 'BeneficiaryApproveUpdate3/BeneficiaryApproveUpdate3'.
    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def get(self, request, pk, *args, **kwargs):
        queryset = Beneficiaries.objects.all().filter(id=pk)
        serializer = BeneficiaryGetPendingUpdates(queryset, many=True)

        queryset2 = Beneficiaries.objects.all().values_list('update_fields').filter(id=pk)
        # serializer2 = BeneficiaryJSONSerializer(queryset2 ,many =True)

        # after = serializer2.data

        context = {
            "before": serializer.data,
            "after": queryset2[0][0]  # this returns the raw data without the brackets
            # "after" : json.dumps(after[0], sort_keys=True, indent=3)
        }

        return Response(context)

    def put(self, request, pk, *args, **kwargs):
        # the 'changes' will be transaferred to the jsonfield
        # jsonfield name is update_fields
        beneficiary = Beneficiaries.objects.filter(id=pk)
        serializer = BeneficiaryListSerializer(beneficiary, many=True)
        data = {}
        try:
            beneficiary2 = Beneficiaries.objects.get(id=pk)
            serializer2 = BeneficiaryListSerializer(beneficiary2, data=serializer.data[0])
            if serializer2.is_valid():
                # serializer2.validated_data['beneficiary_status'] = 'PENDING'
                # serializer2.validated_data['request_type'] = 'UPDATE'
                serializer2.validated_data['request_type'] = 'UPDATE'
                serializer2.validated_data['beneficiary_status'] = 'PENDING'
                serializer2.validated_data["update_fields"] = request.data
                serializer2.save()
                data["sucesss"] = "Request Update"
                data["data"] = serializer2.data
                return Response(data=data)
            # else:
            #     return Response ("BeneficiaryRequestUpdate failed to work.")
        except Exception as e:
            return Response(e)


class BeneficiaryRequestDelete(APIView):
    """
    Endpoint to request delete for beneficiary. Request should be approved/rejected by another endpoint.
    Sample data to submit is provided below:
    {
        "reason": "requesting to delete this beneficiary because of relationship change"
    }

    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def put(self, request, pk, *args, **kwargs):
        beneficiary = Beneficiaries.objects.filter(id=pk)
        serializer = BeneficiaryListSerializer(beneficiary, many=True)
        data = {}

        beneficiary2 = Beneficiaries.objects.get(id=pk)
        serializer2 = BeneficiaryListSerializer(beneficiary2, data=serializer.data[0])
        if serializer2.is_valid():
            serializer2.validated_data['request_type'] = 'REMOVE'
            serializer2.validated_data['beneficiary_status'] = 'PENDING'
            serializer2.validated_data['reason'] = request.data["reason"]

            # serializer2.validated_data['update_fields'] =  {
            #     "reason": request.data["reason"],
            #     "request_type": "REMOVE", 
            #     "beneficiary_status": "PENDING", 
            # }
            serializer2.save()
            data["success"] = "Request Delete"
            data["data"] = serializer2.data
            return Response(data=data)

        else:
            return Response("BeneficiaryRequestDelete failed to work.")
        # return Response(data = data)


class BeneficiaryDenyUpdate3(DestroyAPIView):
    """
    Endpoint to deny update requests for beneficiary.

    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def put(self, request, pk, *args, **kwargs):
        beneficiary = Beneficiaries.objects.filter(id=pk)
        serializer = BeneficiaryListSerializer(beneficiary, many=True)

        beneficiary2 = Beneficiaries.objects.get(id=pk)
        serializer2 = BeneficiaryListSerializer(beneficiary2, data=serializer.data[0])
        data = {}
        if serializer2.is_valid():
            # once the 'changes' are now denied,jsonfield will be cleared
            serializer2.validated_data['beneficiary_status'] = 'APPROVED'
            serializer2.validated_data['request_type'] = 'ADD'
            serializer2.validated_data['update_fields'] = ''
            serializer2.save()
            data["sucesss"] = "Beneficiary Update Request Denied"
            return Response(data=data)

        # return super().delete(request, *args, **kwargs)


class BeneficiaryApproveUpdate3(APIView):
    """
    Endpoint to approve update requests for beneficiary.
    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def update(self, request, pk, *args, **kwargs):
        # once the 'changes' are now approved,
        # the jsonfield data will be pulled out and transferred to the main model
        # after tranfer process is complete, jsonfield will be cleared
        beneficiary = Beneficiaries.objects.values_list('update_fields').filter(id=pk)
        # serializer = BeneficiaryJSONSerializer(beneficiary, many=True)

        beneficiary2 = Beneficiaries.objects.get(id=pk)
        serializer2 = BeneficiaryListSerializer(beneficiary2, data=beneficiary[0][0])
        data = {}
        if serializer2.is_valid():
            serializer2.validated_data['beneficiary_status'] = 'APPROVED'
            serializer2.validated_data['request_type'] = 'ADD'
            serializer2.validated_data['update_fields'] = ''
            serializer2.save()
            data["sucesss"] = "Update Successful"
            return Response(data=data)
            # return Response(beneficiary[0][0][0])

        # return Response(beneficiary[0][0][0])
        # return super().update(request, *args, **kwargs)


class BeneficiaryApproveDelete3(APIView):
    """
    Endpoint to approve delete requests for beneficiary.
    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def delete(self, request, pk, *args, **kwargs):
        # once the beneficiary is found
        # it would be permanently deleted in the models

        try:
            ifexists = Beneficiaries.objects.filter(id=pk)
            ifexists.delete()
            return Response({'success': 'Beneficiary Delete Request Approved'})
        except Exception:
            pass
        return super().delete(request, **kwargs)
        # beneficiary = Beneficiaries.objects.filter(id = pk)

        # serializer = BeneficiaryListSerializer(beneficiary, many=True)

        # data = {}

        # beneficiary2 = Beneficiaries.objects.get(id = pk)
        # serializer2 = BeneficiaryListSerializer(beneficiary2, data=serializer.data[0])

        # if serializer2.is_valid():
        #     serializer2.validated_data['update_fields'] = ''
        #     serializer2.validated_data['request_type'] = 'ADD'
        #     serializer2.validated_data['beneficiary_status'] = 'APPROVED'
        #     serializer2.save()
        #     data["sucesss"] = "Beneficiary Delete Request Approved"
        #     return Response(data = data)


class BeneficiaryDenyDelete3(APIView):
    """
    Endpoint to approve or deny delete requests for beneficiary.
    """
    permission_classes = (AllowAny,)
    lookup_field = 'pk'
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def update(self, request, pk, *args, **kwargs):
        # once the 'changes' are now approved,
        # the jsonfield data will be pulled out and transferred to the main model
        # after tranfer process is complete, jsonfield will be cleared
        beneficiary = Beneficiaries.objects.filter(id=pk)
        serializer = BeneficiaryListSerializer(beneficiary, many=True)

        data = {}

        beneficiary2 = Beneficiaries.objects.get(id=pk)
        serializer2 = BeneficiaryListSerializer(beneficiary2, data=serializer.data[0])
        if serializer2.is_valid():
            serializer2.validated_data['beneficiary_status'] = 'APPROVED'
            serializer2.validated_data['request_type'] = 'ADD'
            serializer2.validated_data['reason'] = ''
            # serializer2.validated_data['update_fields'] = ''
            serializer2.save()
            data["sucesss"] = "Beneficiary Delete Request Denied"
            return Response(data=data)
            # return Response(beneficiary[0][0][0])


class NewBeneficiary(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryListSerializer

    def post(self, request, *args, **kwargs):
        serializer = BeneficiaryListSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.validated_data['beneficiary_status'] = 'PENDING'
            serializer.validated_data['request_type'] = 'ADD'
            serializer.save()
            data["sucesss"] = "Beneficiary Upload Request Made"
            context = {
                "id": serializer.data['id'],
                "status": "success"
            }
            return Response(context)
        # return super().post(request, *args, **kwargs)
