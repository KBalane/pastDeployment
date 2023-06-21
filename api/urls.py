from django.urls import include, path, re_path

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from api import views
# InsureePolicyViewSet, PolicyViewSet, TransactionViewSet

from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    # This is for a secure connection for swagger. To allow https.
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


app_name = 'api'
schema_view = get_schema_view(
    openapi.Info(
        title="DigiInsurance API",
        default_version='v1',
        description="",
        terms_of_service="https://apptitude.xyz/terms-of-use/",
        contact=openapi.Contact(email="admin@apptitude.xyz"),
        license=openapi.License(name="BSD License"),
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('insureepolicy', views.InsureePolicyViewSet)
router.register('policy', views.PolicyViewSet)
router.register('transactions', views.TransactionViewSet)
router.register('bank-accounts', views.UserBankAccountViewSet)
router.register('healthQuestions', views.HealthQuestionsViewSet)
router.register('dragonpay/processors', views.DragonpayProcessorViewSet, 'dragonpay-processors')
router.register('company-info', views.CompanyViewSet)
# router.register('recent_applicants', views.recent_applicants)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # BASE URLS
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # <-- Here
    path('login/', views.LoginView.as_view(), name='login'),
    path('test_login/', views.TestLoginView.as_view(), name='test_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('terms', views.TermsAndCondition.as_view(), name="terms_and_condition"),  # Terms and Condition

    # SOCIAL AUTH URLS
    path('auth/signup/google/', views.GoogleSignUp.as_view(), name='Google Signup Login'),
    path('auth/signup/fb/', views.FBSignup.as_view(), name='FB Signup Login'),
    path('auth/signup/apple/', views.AppleSignUp.as_view()),

    # ACCOUNT URLS
    path('account/submitted_id/<int:user_id>/', views.User_ID.as_view(), name='Get ID'),
    path('account/change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('account/forgot-password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('account/reset-password/', views.ResetPassword.as_view(), name='reset_password'),
    path('account/upload-accinfo', views.UploadAccInfo.as_view(), name="upload_account_info"), # Store Account Info (Account Opening)
    path('account/verify-email/<str:token>/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('account/user_phone_verify/', views.PhoneVerification.as_view(), name='user_phone_verify'),
    path('account/user_phone_verify_status/<str:mobile_number>', views.PhoneVerification_check.as_view(),
         name='user_phone_verify_status'),
    path('account/<int:user_id>/update_specific_profile', views.UpdateProfileDetails.as_view(), name='updateprofile'),
    path('account/avatar_selfie/<int:user_id>', views.AvatarSelfie.as_view(), name='get_avatar-selfie'),
    path('account/user_verification/<int:user_id>', views.GetUserVerification.as_view(), name='get_user_is_verified'),
    path('account/kyc_verification/<int:user_id>', views.GetUserKYCVerification.as_view(), name='get_user_kyc_verify'),

    path('terms', views.TermsAndCondition.as_view(), name="terms_and_condition"),  # Terms and Condition

    path('users/<int:id>/update-payment', views.UpdateBankAccount.as_view(), name="Update_Payment_Method"),  # Update Preferred PAyment MEthod

    path('insureepolicy/beneficiary', views.UploadBeneficiaries.as_view(), name="upload_beneficiary"),  # Store Beneficiaries
    path('admin/pending_beneficiary/add/', views.UploadBeneficiaries2.as_view(),
         name="make request (to add) for beneficary"),  # Add Request to Add and Approve Endpoint for Add
    path('admin/pending_beneficiary/add/<int:id>/', views.UploadBeneficiaries2.as_view(),
         name="deny delete request (to add) for beneficary"),  # Add Request to Add and Approve Endpoint for Add

    path('insureepolicy/beneficiary/list', views.BeneficiariesList.as_view(),
         name="list_beneficiary"),  # List of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/status', views.BeneficiariesStatus.as_view(),
         name="displays status for beneficiary"),  # displays status for beneficiary
    path('insureepolicy/beneficiary/<int:id>/update', views.BeneficiariesUpdate.as_view(),
         name="Update_beneficiary"),  # Update of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/delete', views.BeneficiariesDelete.as_view(),
         name="Delete_beneficiary"),  # Delete of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/todelete', views.ToDelete.as_view(),
         name="Delete_beneficiary"),  # request to delete beneficiary
    path('insuree/beneficiary-info/<int:insuree_id>', views.GetSpecificBeneficiaryInfo.as_view(),
         name="get_beneficiary_info"),  # Returns insuree beneficiaries and its policies
    path('insuree/uploadfile', views.UploadSubmittedDocs.as_view(),
         name='upload_submitted_docs'),

    path('account_settings/bank-accounts/<int:pk>', views.GetSpecificBankAccount,
         name="get_insuree_bank_acount"),

    # ADMIN URLS
    path('admin/insureepolicy/question/answer/<int:insureePolicy>', views.ViewHealthQAAndHealthQuestion.as_view(),
         name="view_health_question_answer_count"),
    path('admin/health_questions_answers/<int:id>/manual_validation/',
         views.ManualValidationHealthQuestionAnswers.as_view(), name='update_answer_status'),
    path('admin/investment_product', views.UploadInvestmentProduct.as_view(), name="admin_investment_product"),
    path('admin/recent_applicant/', views.Recent_Application.as_view(), name="Recent_Application"),  # beta version
    path('admin/active_policy_users/', views.Active_Policy_User.as_view(), name="Active_Policy_User"),
    path('admin/active_products/', views.Active_Products.as_view(), name="Active_Products"),
    path('admin/policy_filtering/<str:status_search>/', views.Policy_Filtering.as_view(), name="Policy_Filtering"),
    path('admin/policy_holders/all/', views.Policy_Holders.as_view(), name="policy_holders"),
    path('admin/claims_list/all/', views.Claims_List.as_view(), name="claims_list"),
    path('admin/claims_details/<int:id_search>/', views.Claims_Details.as_view(), name="claims_details"),
    path('admin/admin_list/', views.Admin_List.as_view(), name="admin_list"),
    path('admin/company_bank_info/<int:id_search>/', views.Company_Bank_Info.as_view(), name="company_bank_info"),
    path('admin/admin_update/<int:id>/', views.AdminUpdate.as_view(), name="admin_update"),
    path('admin/admin_edit/<int:id>/', views.Admin_Edit.as_view(), name="admin_edit"),
    path('admin/admin_create/', views.AdminCreate.as_view(), name="admin_create"),
    path('admin/verify/', views.VerifyEmail.as_view(), name="admin-verify"),
    path('admin/send_verification/<str:username>/<str:to_email>/', views.EmailHandler.as_view(),
         name="send_verification"),
    path('admin/account_activate/<str:token>/', views.setInitialPassword.as_view(), name="setInitialPassword"),

    path('insuree_create/', views.CreateInsuree.as_view(), name="CreateInsuree"),

    path('admin/company_details/<int:id_search>/', views.Company_Details.as_view(), name="company_details"),
    path('admin/company/list/', views.CompanyList.as_view(), name="Displays List of companies ordered by newest"),
    path('admin/company/create/', views.CompanyCreate.as_view(), name="Creates a new company"),
    path('admin/company/<int:id>/update/', views.CompanyUpdate.as_view(), name="Updates company details"),
    path('admin/company/<int:id>/update/photos/', views.PhotoCompanyUpdate.as_view(), name="Updates photos"),
    path('admin/userinvestment/', views.GetListOfUserInvestment.as_view(), name='user_investment'),
    path('admin/advertisement/', views.Advertisement.as_view(), name='advertisement'),
    # PUT - Requires Title and Description, #PATCH Doesnt
    path('admin/advertisement/<int:id>/delete/', views.DeleteAdvertisement.as_view(), name='advertisement_delete'),
    path('admin/advertisement/<int:id>/edit/', views.EditAdvertisement.as_view(), name='advertisement_patch'),
    path('admin/advertisement/<int:id>/edit/status/', views.EditAdvertisementStatus.as_view(),
         name='advertisement_edit_status'),
    path('admin/advertisement/status/', views.AdvertisementUpdateStatus.as_view(), name='advertisement_status_update'),
    path('admin/transaction_history/generate_pdf/<int:id_search>/', views.GeneratePDF_Transaction.as_view(),
         name='generate_pdf'),
    # ?download=true/

    path('transactions/history/<int:insuree>/', views.TransactionHistory_Base.as_view(), name='transaction_history'),
    path('claims/claims_history/generate_pdf/<int:id_search>/', views.GeneratePDF_Claims.as_view(),
         name='generate_pdf_claims'),
    path('claims/claims_history/download_pdf/<int:claim_id>/', views.DownloadPDF_Claims.as_view(), name='download_pdf'),
    path('policy/policy-image/<int:id>/', views.PolicyViewImage_Update.as_view(), name='policy-image-update'),
    path('policy/policy-image/create/', views.PolicyViewImage_POST.as_view(), name='policy-image-create'),
    path('admin/claims/approve/<int:claim_id>/', views.ApproveClaims.as_view(), name='Approve Claim'),
    path('admin/claims/disapprove/<int:claim_id>/', views.DeniedClaims.as_view(), name='Denied Claim'),

    path('admin/company_requirements/<int:id>/', views.UpdateCompanyRequirements.as_view(),
         name="Update or Delete Company Requirements"),

    path('company_requirements/<int:id>', views.CompanyRequirementsList.as_view(),
         name='get_company_req'),
    path('company_investment_types/<int:company_id>', views.GetCompanyInvestmentType.as_view(),
         name='company_investment_types'),

    path('admin/policy/<int:pk>/', views.PolicyEdit.as_view(),
         name="Edit Policy"),
    path('admin/policy/fileupdate/<int:pk>/', views.PolicyFileEdit.as_view(),
         name="Edit Policy Files"),
    path('policy/<int:pk>/benefits', views.GetPolicyBenefitsView.as_view(),
         name="get_policy_benefits"),
    path('policy/<int:pk>/benefits/update', views.GetPolicyBenefitsView.as_view(), name="update_policy_benefits"),
    # Updates the benefits of an existing policy
    path('policy/<int:pk>/all', views.GetSpecificPolicyView.as_view(),
         name="get_specific_policy"),
    path('policy/downloadpdf/<int:id>/', views.DownloadPdfPolicy.as_view(),
         name='download_pdf_policy'),
    path('policy/<int:id>/edit', views.EditSpecificPolicy.as_view(),
         name="Edit_Policy"),  # Edit of Policy
    path('policy/<int:id>/edit/package', views.EditPackagePerPolicy.as_view(), name="edit_package_per_policy"),
    # Edit Policy Package
    path('policy/upload_file', views.UploadPolicy.as_view(),
         name='upload_policy'),

    path('insuree/<int:insuree>/transactions', views.GetInsureeTransactionsView.as_view(),
         name="get_insuree_transactions"),

    path('insuree/submitted_claims/<int:insuree_id>/<int:insuree_policy_id>/', views.GetSubmittedClaims.as_view(),
         name="get_insuree_submitted_docs"),
    path('insuree/submitted_docs/<int:insuree_id>', views.GetSubmittedDocs.as_view(),
         name="get_insuree_submitted_docs"),
    path('insuree/download_submitted_docs/<int:insuree_id>/<int:id>', views.DownloadSubmittedDocs.as_view(),
         name="download_submitted_docs"),
    path('insuree/insuree_investment_calc/', views.UserInvestmentCalculator.as_view(),
         name="investment_caculator"),
    path('insuree/upload_insuree_investment/<int:user_id>', views.UserInvestmentUpload.as_view(),
         name='upload_insuree_investment'),
    path('insuree/get_investment_status/<int:insuree_id>', views.GetUserInvestmentStatus.as_view(),
         name='get_investment_status'),

    path('admin/insuree/archive/<int:insuree_id>/', views.ArchiveUser.as_view(),
         name='Set Archive to True'),
    path('admin/insuree/unarchive/<int:insuree_id>/', views.UnArchiveUser.as_view(),
         name='Set Archive to False'),
    path('admin/insureepolicy/details/<int:UserId>/<int:PolicyId>/', views.InsureePolicy_Details.as_view(),
         name='Policy Info for InsureePolicy'),
    path('admin/policy_holder/archive/<int:user_id>/<int:policy_id>/', views.ArchivePolicyHolder.as_view(),
         name='Archive Policy for User'),
    path('admin/policy_holder/unarchive/<int:user_id>/<int:policy_id>/', views.UnArchivePolicyHolder.as_view(),
         name='Un-Archive Policy for User'),
    path('admin/insuree/archived/all/', views.ListOfArchivedUsers.as_view(),
         name='All Archived Users'),
    path('admin/policy_holder/archived/all/', views.ListOfArchivedPolicyHolder.as_view(),
         name='All Archived Policy Holder'),
    path('admin/policy_holder/unarchived/all/', views.ListOfUnArchivedPolicyHolder.as_view(),
         name='All Not Archived Policy Holder'),

    # path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
    # path('admin/company_details/<int:id_search>', views.Company_Details.as_view(), name = "company_details"),
    # path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
    # path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
    # path('admin/company_details/<int:id_search>', views.Company_Details.as_view(), name = "company_details"),
    # path('admin/get_submitted_id/<int:user_id>/', views.SubmittedID.as_view(), name = "get_submitted_id"),

    # ADMIN SIDE URLS
    path('admin/get_average_policy_currentDay', views.GetAveragePolicy_day.as_view(),
         name='get_average_policy_currentDay'),
    path('admin/get_average_policy_currentWeek', views.GetAveragePolicy_week.as_view(),
         name='get_average_policy_currentWeek'),
    path('admin/get_average_policy_currentMonth', views.GetAveragePolicy_month.as_view(),
         name='get_average_policy_currentMonth'),
    path('admin/get_average_policy_currentYear', views.GetAveragePolicy_year.as_view(),
         name='get_average_policy_currentYear'),
    path('admin/get_claims_count_year', views.GetClaimsCompare_year.as_view(),
         name='get_claims_count_year'),
    path('admin/get_claims_count_month', views.GetClaimsCompare_month.as_view(),
         name='get_claims_count_month'),
    path('admin/get_claims_count_week', views.GetClaimsCompare_week.as_view(),
         name='get_claims_count_week'),
    path('admin/get_claims_count_day', views.GetClaimsCompare_day.as_view(),
         name='get_claims_count_day'),
    path('admin/get_policy_paid_percentage_currentMonth', views.GetPaidPolicyPercentage.as_view(),
         name='get_policy_paid_percentage_currentMonth'),
    path('admin/getclient_count_year', views.GetClientCount_year.as_view(), name='get_client_count_year'),
    path('admin/getclient_count_month', views.GetClientCount_month.as_view(), name='get_client_count_month'),
    path('admin/getclient_count_week', views.GetClientCount_week.as_view(), name='get_client_count_week'),
    path('admin/getclient_count_day', views.GetClientCount_day.as_view(), name='get_client_count_day'),

    # ADMIN PENDING BENEFICIARIES

    # to view pending requests (does not work for view update and delete requests)
    path('admin/pending_beneficiaries/<str:requestType>', views.PendingBeneficiaries.as_view(),
         name='Pending Beneficiaries'),
    # to approve a pending ADD request:
    path('admin/pending_beneficiaries/<int:id>/approve/', views.ApproveBeneficiary.as_view(),
         name='Approve Beneficiary'),
    # to deny a pending ADD request:
    path('admin/pending_beneficiaries/<int:id>/deny/', views.DenyBeneficiary.as_view(), name='Deny Beneficiary'),
    path('admin/pending_beneficiaries/<int:id>/', views.AdminGetSpecificBeneficiaryInfo.as_view(),
         name='Beneficiary Info For Aproval'),

    # DONT USE POST
    path('admin/pending_beneficiary/add/', views.UploadBeneficiaries2.as_view(),
         name="make request (to add) for beneficary"),  # Add Request to Add and Approve Endpoint for Add
    path('admin/update_beneficiary/<int:id>/', views.BeneficiaryUpdate2.as_view(), name='Beneficiary Update'),

    # ongoing refactor urls

    # to view pending requests
    path('admin/beneficiaries/pending/<str:requestType>', views.PendingBeneficiaries.as_view(),
         name='Pending Beneficiaries'),

    # UPLOAD/ADD
    # to make an UPLOAD request:
    path('admin/beneficiary/new/', views.NewBeneficiary.as_view(), name='Make Request to Upload'),
    # to approve an UPLOAD request:
    path('admin/beneficiary/new/approve/<int:id>/', views.ApproveBeneficiary.as_view(), name='Approve Beneficiary'),
    # to deny an UPLOAD request:
    path('admin/beneficiary/new/deny/<int:id>/', views.DenyBeneficiary.as_view(), name='Deny Beneficiary'),

    # UPDATE
    # to make an UPDATE request:
    path('admin/beneficiary/update/<int:pk>/', views.BeneficiaryRequestUpdate.as_view(), name='Make Request to Update'),
    # to approve an UPDATE request:
    path('admin/beneficiary/update/approve/<int:pk>/', views.BeneficiaryApproveUpdate3.as_view(),
         name='Approve Beneficiary Update'),
    # to deny an UPDATE request:
    path('admin/beneficiary/update/deny/<int:pk>/', views.BeneficiaryDenyUpdate3.as_view(),
         name='Deny Beneficiary Update'),

    # DELETE/REMOVE
    # to make a REMOVE request:
    path('admin/beneficiary/remove/<int:pk>/', views.BeneficiaryRequestDelete.as_view(), name='Make Request to Delete'),
    # to approve a REMOVE request:
    path('admin/beneficiary/remove/approve/<int:pk>/', views.BeneficiaryApproveDelete3.as_view(),
         name='Approve Beneficiary Delete'),
    # to deny a REMOVE request:
    path('admin/beneficiary/remove/deny/<int:pk>/', views.BeneficiaryDenyDelete3.as_view(),
         name='Deny Beneficiary Delete'),

    # CLAIMS URLS
    path('claims/history/<int:user_id>/', views.ClaimsHistoryPerUser.as_view(), name="claims_history_per_user"),
    path('claims/claims_get/', views.claims_get, name="claims_create"),
    path('claims/claims_history/<int:policyid_filter>/', views.Claims_History.as_view(), name="claims_history"),
    path('claims/uploadclaims/<int:user_id>', views.UploadClaims.as_view(), name='uploadclaims'),
    path('claims/claims_history/generate_pdf/<int:id_search>/', views.GeneratePDF_Claims.as_view(),
         name='generate_pdf_claims'),
    path('claims/claims_history/download_pdf/<int:claim_id>/', views.DownloadPDF_Claims.as_view(), name='download_pdf'),

    # COMPANY URLS
    path('company_requirements/<int:id>', views.CompanyRequirementsList.as_view(),
         name='get_company_req'),
    path('company_investment_types/<int:company_id>', views.GetCompanyInvestmentType.as_view(),
         name='company_investment_types'),
    path('company/faq/', views.CompanyFAQCreate.as_view(), name='Company Questions'),
    path('company/faq/<int:id>/', views.CompanyFAQUpdate.as_view(), name='Company FAQ Update'),
    # DRAGONPAY URLS
    path('dragonpay/postback/payout/', views.dragonpay_payout_postback),
    path('dragonpay/postback/', views.dragonpay_postback),

    path('ad/extracturl/', views.ExtractURL.as_view(), name='Extract URL'),

    path('payment/refno/<int:insureePolicy>/', views.GetTransactionRefNo.as_view(), name='Get Latest Ref No'),
    # Draft a Product
    path('policy/draft/<int:id>/', views.DraftAProduct.as_view(), name='Draft a Product'),

    # Activate a Product
    path('policy/activate/<int:id>/', views.ActivateAProduct.as_view(), name='Activate a Product'),

    path('ad/extracturl/', views.ExtractURL.as_view(), name='Extract URL'),

    path('company_requirements', views.CompanyRequirementsPost.as_view()),

    # HEALTH URLS
    path('healthanswers/batchupload/', views.BatchUploadFinal, name="Batch Upload"),
    path('healthQuestions/<int:id>/update/', views.UpdateHealthQuestion.as_view(),
         name='update_healthQuestions'),  # Update Health Question

    # INSUREE URLS
    path('insureepolicy/extra', views.InsureePolicyViewSet2.as_view(), name='insureepolicy with beneficiary id'),
    path('insureepolicy/question/answer', views.UploadHealthQA.as_view(),
         name="upload_health_question_answer"),  # Store Health Question Answer
    path('insureepolicy/question/<int:insureePolicy>', views.ViewHealthQA.as_view(),
         name="view_health_question_answer"),  # View Health Question Answer
    path('insuree/uploadfile', views.UploadSubmittedDocs.as_view(),
         name='upload_submitted_docs'),
    path('insuree_create/', views.CreateInsuree.as_view(), name="CreateInsuree"),
    path('insuree/<int:insuree>/transactions', views.GetInsureeTransactionsView.as_view(),
         name="get_insuree_transactions"),
    path('insuree/submitted_docs/<int:insuree_id>', views.GetSubmittedDocs.as_view(),
         name="get_insuree_submitted_docs"),
    path('insuree/download_submitted_docs/<int:insuree_id>/<int:id>', views.DownloadSubmittedDocs.as_view(),
         name="download_submitted_docs"),
    path('insuree/insuree_investment_calc/', views.UserInvestmentCalculator.as_view(),
         name="investment_caculator"),
    path('insuree/upload_insuree_investment/<int:user_id>', views.UserInvestmentUpload.as_view(),
         name='upload_insuree_investment'),
    path('insuree/get_investment_status/<int:insuree_id>', views.GetUserInvestmentStatus.as_view(),
         name='get_investment_status'),
    path('insuree_questions/', views.InsureeQuestions.as_view(), name='Questions applicable to the insured.'),

    # INSUREE BENEFICIARY
    path('insureepolicy/beneficiary', views.UploadBeneficiaries.as_view(),
         name="upload_beneficiary"),  # Store Beneficiaries
    path('insureepolicy/beneficiary/list', views.BeneficiariesList.as_view(),
         name="list_beneficiary"),  # List of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/status', views.BeneficiariesStatus.as_view(),
         name="displays status for beneficiary"),  # displays status for beneficiary
    path('insureepolicy/beneficiary/<int:id>/update', views.BeneficiariesUpdate.as_view(),
         name="Update_beneficiary"),  # Update of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/delete', views.BeneficiariesDelete.as_view(),
         name="Delete_beneficiary"),  # Delete of Beneficiaries
    path('insureepolicy/beneficiary/<int:id>/todelete', views.ToDelete.as_view(),
         name="Request to Delete_beneficiary"),  # request to delete beneficiary
    path('insuree/beneficiary-info/<int:insuree_id>', views.GetSpecificBeneficiaryInfo.as_view(),
         name="get_beneficiary_info"),  # Returns insuree beneficiaries and its policies

    # KYC URLS
    path('kyc/template_ids/', views.TemplateIDViewSet.as_view(),
         name='template_ids'),
    path('kyc/upload_id_selfie/<int:user_id>', views.KycHandler.as_view(), name='verify_kyc'),
    path('kyc/update_ID/<int:user_id>', views.UpdateID.as_view(),
         name='update_ID'),
    path('kyc/update_selfie/<int:user_id>', views.UpdateSelfie.as_view(),
         name='update_selfie'),
    path('kyc/lists', views.KYCList.as_view(), name="kyc_list"),

    # NEWSFEED URLS
    path('like_post/<int:user_id>/<int:advertisement_id>/', views.like_post, name='Like Post'),
    path('newsfeed/get/list/', views.NewsfeedList.as_view(), name='newsfeed_get'),
    path('newsfeed/get/detail/<int:pk>/', views.NewsfeedDetailed.as_view(), name='newsfeed_detailed_view'),

    # PAYMENT URLS
    path('api-token-auth/', views.CustomObtainAuthToken.as_view(),
         name='api_token_auth'),
    path('payment/', views.PaymentView2.as_view(),
         name='list of payments'),
    path('payment/<int:user_id>', views.PaymentView.as_view(),
         name='policy_payment'),
    path('payment/<int:user_id>/dragon-pay', views.Dragonpay_redirect_payment.as_view(),
         name='policy_payment'),

    # POLICY URLS
    path('policy/calculator/requirements/<int:policy>/', views.PolicyRequirementsList.as_view(),
         name='Policy Requirements List'),
    path('policy/calculator/requirements/create/', views.PolicyRequirementsCreate.as_view(),
         name='Policy Requirements Create'),
    path('policy/calculator/view/', views.GetPolicyCalculator.as_view(), name="polcy_calculator"),
    path('policy/calculator/calculate/<int:user_id>/<int:policy_id>/', views.PolicyCalculate.as_view(),
         name="polcy_calculate"),
    path(
        'policy/calculator_beta/<int:policy_id>/<int:current_savings>/<int:current_investments>/<int:insurance_coverage>/<int:household_expenses>/<int:liabilities>/',
        views.PolicyCalculateV2.as_view(), name="polcy_calculate"),
    path('policy/terms_per_policy/<int:id_search>/', views.TermsAndConditionPerPolicy.as_view(),
         name="terms_per_policy"),
    path('policy/terms_per_policy/<int:pk>/update', views.UpdateTermsAndConditionPerPolicy.as_view(),
         name="terms_per_policy-update"),

    path('policy/policy-image/<int:id>/', views.PolicyViewImage_Update.as_view(), name='policy-image-update'),
    path('policy/policy-image/create/', views.PolicyViewImage_POST.as_view(), name='policy-image-create'),
    path('policy/<int:pk>/benefits', views.GetPolicyBenefitsView.as_view(),
         name="get_policy_benefits"),
    path('policy/<int:pk>/benefits/update', views.GetPolicyBenefitsView.as_view(), name="update_policy_benefits"),
    # Updates the benefits of an existing policy
    path('policy/<int:pk>/all', views.GetSpecificPolicyView.as_view(),
         name="get_specific_policy"),
    path('policy/downloadpdf/<int:id>/', views.DownloadPdfPolicy.as_view(),
         name='download_pdf_policy'),
    path('policy/<int:id>/edit', views.EditSpecificPolicy.as_view(),
         name="Edit_Policy"),  # Edit of Policy
    path('policy/<int:id>/edit/package', views.EditPackagePerPolicy.as_view(), name="edit_package_per_policy"),
    # Edit Policy Package
    path('policy/upload_file', views.UploadPolicy.as_view(),
         name='upload_policy'),
    path('policy/all', views.GetAllPoliciesView.as_view(),
         name="get_all_policies"),
    path('policy/add_product', views.CreateProduct.as_view(), name="add_product"),  # Path for add policy product form
    path('Policy_Holder/Contact_Info/<int:UserId>/<int:PolicyId>/', views.Policy_Holder_Contact_Info.as_view(),
         name='Policy Holder Contact Info'),
    path('Policy_Holder/Policy_Info/<int:UserId>/<int:PolicyId>/',
         views.Policy_Holder_Policy_Info.as_view(), name='Policy Holder Policy Info'),
    path('Policy_Holder/Personal_Info/<int:UserId>/<int:PolicyId>/', views.Policy_Holder_Personal_Info.as_view(),
         name='Policy Holder Personal Info'),

    # path('policy-image/<int:id>', views.PolicyViewImage.as_view(), name = 'post_policy_image'),

    path('products/most_popular/', views.MostPopularProducts.as_view(), name="MostPopularProducts"),
    path('s1/demo/', views.S1Demo.as_view(), name="S1Demo"),

    # TERMS AND CONDITIONS
    path('admin/terms/get/<int:pk>/', views.GetTermsAndCondition.as_view(), name="View Terms and Condtion PDF"),
    path('admin/terms/add/', views.Terms.as_view(), name="Add New Terms Condition"),
    path('admin/terms/update/<int:pk>/', views.TermsUpdate.as_view(), name="Update Terms Condition"),

    # TRANSACTION URLS
    path('transactions/history/<int:insuree>/', views.TransactionHistory_Base.as_view(), name='transaction_history'),
    path('transactions/history/<int:insuree_id>/<slug:start_date>/<slug:end_date>/<slug:authtoken>/',
         views.TransactionHistory.as_view(),
         name="transactions_history"),

    # USER URLS
    path('users/bank-accounts', views.UserBankAccount.as_view(),
         name="post_bank_account"),
    path('users/<int:id>/update-payment', views.UpdateBankAccount.as_view(),
         name="Update_Payment_Method"),  # Update Preferred Payment MEthod
    path('user_list/', views.UserList.as_view(),
         name='user_list'),
    path('user_favourite/', views.UserFavorite.as_view(), name='View Favourites'),
    path('user_favourite/<int:id>/update/', views.UpdateFavourite.as_view(),
         name='update_userFavourite'),  # Update Health Question()
    path('user/verify/<int:id>', views.UserIsVerified.as_view()),

    # OTHER
    path('Cert-template/<int:id>/', views.CertificateTemplate.as_view(), name='certificate template'),
    path('ad/extracturl/', views.ExtractURL.as_view(), name='Extract URL'),

    # FAQ_GET_ENDPOINT
    path('company/faq/details', views.CompanyFaqDetails.as_view(), name='Displays Company Email and Mobile Number'),

    # Get all terms and conditions
    path('terms_and_conditions/get/', views.GetAllTermsAndCondition.as_view(), name='Get all Terms and Conditions'),
    path('generate_policy_pdf/<int:id_search>/', views.GeneratePDF_Policy.as_view(), name='generate policy pdf'),

    path('payment/dragonpay/<str:txn_id>/', views.GetDragonPayTransactionRefNo.as_view(),
         name='Get Latest DragonPay Ref No'),

    # path('dragonpay_redirect/', views.dragonpay_redirect, name='dragonpay_redirect'),
    # path('dragonpay/postback/payout/',views.dragonpay_payout_postback),
    # path('dragonpay/postback/',views.dragonpay_postback)
    # path('dragonpay_payment_redirect/', views.DragonpayRedirectPayment.as_view(), name= 'dragonpay_payment_redirect'),
    # path('dragonpay_redirect/certificate/', views.certificate_dragonpay_redirect.as_view(), name='certificate_dragonpay_redirect'),
    # path('dragonpay_redirect/voucher/', views.voucher_dragonpay_redirect.as_view(), name='voucher_dragonpay_redirect'),

]

# urlpatterns += [
# #     path('dragonpay_redirect/', views.dragonpay_redirect, name='dragonpay_redirect'),
#     path('dragonpay/postback/payout/',views.dragonpay_payout_postback),
#     path('dragonpay/postback/',views.dragonpay_postback)
# ]

# region non-existent
# path('search/', views.SearchTool.as_view(), name='search'),
# path('home/', views.get_home_view, name='app_home_view'),
# path('app_signup/', views.AppSignupView.as_view(), name='app_signup'),
# path('transactions/', views.TransactionView.as_view()),
# path('account/get_specific_profile/<int:id>', views.)
# path('account/getlist', views.GetInsureeList.as_view(),name = 'getlist'),
# path('account/get_specific_profile/<int:id>', views.)
# path('account/getlist', views.GetInsureeList.as_view(),name = 'getlist'),
# path('account/insurance/user/policies', views.GetUserInsurancePolicies.as_view(), name="upload_account_info"),  # Store Health Question Answers
# path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
# path('company_requirements/Delete_Requirements/<int:id>/delete', views.DeleteRequirements.as_view(), name = "Delete Requirements"),
# path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
# path('admin/company_details/<int:id_search>', views.Company_Details.as_view(), name = "company_details"),
# path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
# path('admin/user_photo_id/<int:pk>', views.User_Photo_ID.as_view(), name = "user_photo_id"),
# path('admin/company_details/<int:id_search>', views.Company_Details.as_view(), name = "company_details"),
# path('admin/get_submitted_id/<int:user_id>/', views.SubmittedID.as_view(), name = "get_submitted_id"),
# path('claims/claims_create/', views.claims_create, name = "claims_create"),
# path('kyc/update_ID_selfie/<int:pk>', views.UpdateIDSelfie.as_view(), name="update_Id_selfie"),
# path('policy-image/<int:id>', views.PolicyViewImage.as_view(), name = 'post_policy_image'),
# endregion
