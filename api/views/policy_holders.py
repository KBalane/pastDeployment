from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.Policy import Policy

from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from datetime import datetime

__all__ = ['Policy_Holders', 'Policy_Holder_Contact_Info', 'Policy_Holder_Personal_Info', 'InsureePolicy_Details',
           'ArchivePolicyHolder', 'UnArchivePolicyHolder', 'ListOfArchivedPolicyHolder', 'ListOfUnArchivedPolicyHolder',
           'Policy_Holder_Policy_Info']


class Policy_Holders(APIView):
    def get(self, request):
        insuree_policy_users = InsureePolicy.objects.values(
            'id',
            'insuree',
            'policy',
            'insuree__last_name',
            'insuree__first_name',
            'insuree__middle_name',
            'insuree__gender',
            'insuree__created_at',
            'policy__name',
            'insuree__user_id',
            'status',
            'policy__category',
            'policy_type2',
        ).filter(insuree__isArchived=False).order_by('-created_at').distinct()
        context = {
            "Policy_Holders": insuree_policy_users
        }
        return Response(context)


class Policy_Holder_Contact_Info(APIView):

    def get(self, request, UserId, PolicyId):
        queryset = InsureePolicy
        insuree_policy_users = InsureePolicy.objects.values(
            'insuree__mobile_number',
            'insuree__tel_number',
            'insuree__email',
            'insuree__home_add',
            'insuree__home_country',
            'insuree__home_zip_code',
            'insuree__current_add',
            'insuree__current_country',
            'insuree__current_zip_code',
            'insuree__employer',
            'insuree__nature_of_business_of_employer'
        )
        try:
            insuree_policy_users = insuree_policy_users.filter(insuree=UserId)
            insuree_policy_users = insuree_policy_users.filter(policy=PolicyId)
            return Response(insuree_policy_users)
        except InsureePolicy.DoesNotExist:
            raise Http404


class Policy_Holder_Personal_Info(APIView):

    def get(self, request, UserId, PolicyId):
        queryset = InsureePolicy
        insuree_policy_users = InsureePolicy.objects.values(
            'insuree__last_name',
            'insuree__civil_status',
            'insuree__gender',
            'insuree__birthday',
            'insuree__age',
            'insuree__nationality',
            'insuree__place_of_birth',
            'insuree__sss',
            'insuree__tin',
            'insuree__occupation',
            'insuree__business',
            'insuree',
            'policy',
        )
        try:
            insuree_policy_users = insuree_policy_users.filter(insuree=UserId)
            insuree_policy_users = insuree_policy_users.filter(policy=PolicyId)
            return Response(insuree_policy_users)
        except InsureePolicy.DoesNotExist:
            raise Http404


class ArchivePolicyHolder(APIView):
    def get(self, request, user_id, policy_id):
        try:
            insuree_policy_users = InsureePolicy.objects.values(
                'insuree__last_name',
                'insuree__first_name',
                'insuree__middle_name',
                'policy__name',
                'insuree__user_id',
                'status',
                'insuree',
                'policy',
                'id',
            )  # .filter(Q(insuree=user_id) & Q(policy=policy_id))#.update(status='Suspended')
            now = datetime.now()
            insuree_policy_users = insuree_policy_users.filter(insuree=user_id)
            insuree_policy_users = insuree_policy_users.filter(policy=policy_id)
            insuree_policy_users = insuree_policy_users.update(status='Suspended', modified_at=now)

            return Response(insuree_policy_users)

        except InsureePolicy.DoesNotExist:
            raise Http404
        # .update(status='Suspended')

        """
        notes: when archiving policy holders, should i archive the user itself?
        or should i archive the policy that the user holds?
        because there are users that have multiple products/policies,
        thats when i asked myself if i should archive the status of the policy that the user holds (insureepolicy status)
        or the specific user in general?
        """


class UnArchivePolicyHolder(APIView):
    def get(self, request, user_id, policy_id):
        try:
            insuree_policy_users = InsureePolicy.objects.values(
                'insuree__last_name',
                'insuree__first_name',
                'insuree__middle_name',
                'policy__name',
                'insuree__user_id',
                'status',
                'insuree',
                'policy',
                'id',
            )  # .filter(Q(insuree=user_id) & Q(policy=policy_id))#.update(status='Suspended')

            insuree_policy_users = insuree_policy_users.filter(insuree=user_id)
            insuree_policy_users = insuree_policy_users.filter(policy=policy_id)
            insuree_policy_users = insuree_policy_users.update(status='Active')
            return Response(insuree_policy_users)
        except InsureePolicy.DoesNotExist:
            raise Http404


class InsureePolicy_Details(APIView):
    """
    Specific details for the Policy that was chosen by the Insuree.
    """

    def get(self, request, UserId, PolicyId):
        queryset = InsureePolicy
        insuree_policy_users = InsureePolicy.objects.all().values(
            'id',
            'policy',
            'insuree',
            'insuree__first_name',
            'insuree__last_name',
            'policy__name',
            'policy__packages',
            'Currency',
            'policy__TPD',
            'policy__ADD',
            'policy__WPTPD',

            'policy__Premium_TPD',
            'policy__Premium_ADD',
            'policy__Premium_WPTPD',

            'insuree__home_add',
            'insuree__home_country',
            'insuree__home_zip_code',

            'insuree__current_add',
            'insuree__current_country',
            'insuree__current_zip_code',
            'insuree__employer',
            'insuree__nature_of_business_of_employer',
        )
        try:
            insuree_policy_users = insuree_policy_users.filter(insuree=UserId)
            insuree_policy_users = insuree_policy_users.filter(policy=PolicyId)
            return Response(insuree_policy_users)
        except InsureePolicy.DoesNotExist:
            raise Http404


class ListOfArchivedPolicyHolder(APIView):
    def get(self, Request):
        archived_PC = InsureePolicy.objects.all().values(
            'insuree__first_name',
            'insuree__middle_name',
            'insuree__last_name',
            'policy',
            'policy__name',
            'policy_type',
            'policy_type2',
            'policy_id',
            'id',
            'InsureePolicy',
            'insuree',
            'insuree__gender',
            'insuree__created_at',
            'insuree__isArchived',
            'status'

        ).filter(insuree__isArchived=True).order_by('-modified_at')

        return Response(archived_PC)


class ListOfUnArchivedPolicyHolder(APIView):
    def get(self, Request):
        archived_PC = InsureePolicy.objects.all().values(
            'insuree__first_name',
            'insuree__middle_name',
            'insuree__last_name',
            'policy',
            'policy__name',
            'insuree',
            'insuree__isArchived',
            'status',
        ).filter(insuree__isArchived=False)

        return Response(archived_PC)


class Policy_Holder_Policy_Info(APIView):

    def get(self, request, UserId, PolicyId):
        insuree_policy_user = InsureePolicy.objects.values(
            'id',
            'insuree',
            'policy_id',
            'policy__name',
            'Currency',
            'policy__TPD',
            'policy__ADD',
            'policy__WPTPD',
            'user_policy',
            'policy_type2',
            'policy__Premium_TPD',
            'policy__Premium_ADD',
            'policy__Premium_WPTPD',
            'created_at',
        )
        packages = Policy.objects.values('packages').filter(id=PolicyId)

        try:
            insuree_policy_user = insuree_policy_user.filter(insuree=UserId)
            insuree_policy_user = insuree_policy_user.filter(policy=PolicyId).latest('user_policy')

            context = {
                "insuree_policy_user": insuree_policy_user,
                "packages": packages,
            }
            return Response(context)
        except InsureePolicy.DoesNotExist:
            raise Http404
