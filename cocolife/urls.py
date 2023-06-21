from django.urls import path

from cocolife import views

app_name = 'cocolife'

urlpatterns = [
    # Auth
    path('auth/register/', views.AuthRegister.as_view()),
    path('auth/send_verification/email/<str:email>', views.EmailVerificationHandler.as_view()),
    path('auth/account/activate/email/<str:token>', views.VerifyEmail.as_view()),
    # path('auth/verify/mobile/<str:email>', views.MobileOTPHandler.as_view()),

    # Features
    path('features/', views.Features.as_view()),
    path('features/<int:id>/', views.FeaturesById.as_view()),

    # Product Insuree
    path('productinsuree/create/', views.ProductInsureeCreate.as_view()),
    path('productinsuree/<int:id>/', views.ProductInsureeUpdate.as_view()),
    # path('productinsuree/<int:id>/summary/',views.ProductInsureeSummary.as_view()),

    path('payment/<int:id_search>/products/',
         views.ProductInsureeList.as_view()),

    # Policy Owner
    path('policyowner/<int:pk>/', views.PolicyOwnerbyID.as_view()),
    path('policyowner/all/', views.PolicyOwner.as_view()),

    # Products
    path('products/', views.Products.as_view()),
    path('products/create/', views.ProductCreate.as_view()),
    path('products/<int:id>/', views.ProductByID.as_view()),
    path('products/proposal/', views.GetProductProposal.as_view()),
    # path('package/<int:product_id>/', views.PackageByID.as_view()),
    # path('variant/<int:package_id>/', views.VariantByID.as_view()),
    path('products/<int:id>/', views.ProductByID.as_view()),
    path('products/proposal/', views.GetProductProposal.as_view()),
    path('products/purchase/', views.PurchaseProduct.as_view()),
    # path('package/<int:product_id>/', views.PackageByID.as_view()),
    # path('variant/<int:package_id>/', views.VariantByID.as_view()),
    path('products/like/info/', views.ProductLikeinfo.as_view()),
    path('products/like/<int:product_id>/<int:user_id>/', views.like_product),
    path('products/like/<int:product_id>/', views.ProductDetailed.as_view()),


    # Beneficiary
    path('beneficiary/<int:id>/', views.BeneficiaryByID.as_view()),
    path('beneficiary/', views.Beneficiary.as_view()),

    # Underwriting
    path('underwriter/all/', views.UnderwriterAll.as_view()),
    path('underwriter/<int:pk>/', views.Underwriter.as_view()),
    path('underwriter/<str:status>/', views.UnderwriterStatus.as_view()),

    # Advertisement
    path('advertisement/', views.PostAdvertisement.as_view()),
    path('advertisement/update_status/',
         views.UpdateAdvertisementStatus.as_view()),

    # Coco Insuree
    path('insuree/<int:id>/liked/articles/',
         views.LikedNewsFeedList.as_view()),
    path('insuree/all/', views.CocoInsuree.as_view()),
    path('insuree/<int:user_id>/', views.CocoInsureeById.as_view()),
    # path('insuree/profile/', views.CocoInsureeProfile.as_view()),
    path('cocoinsuree/<int:id>/policies/', views.CocoInsureePolicies.as_view()),


    # Newsfeed
    path('newsfeed/', views.NewsFeedList.as_view()),
    path('newsfeed/article/<int:id>/', views.NewsFeedDetailed.as_view()),
    path('newsfeed/article/like/<int:advertisement_id>/<int:user_id>/', views.like_post),

    # HealthQuestion
    path('healthquestion/', views.HealthQuestionViewSet.as_view()),
    path('healthquestion/<int:age>/', views.CLHealthQuestionBaseOnAge.as_view()),
    # path('healthquestion/<int:pk>/', views.ManageHealthQuestion.as_view()), #Manage Healthquestions

    # HealthQuestionAnswers
    path('healthquestion/answers/', views.CLHealthQAViewSet.as_view()),
    path('healthquestion/answers/<int:pk>/', views.CLHealthQuestionManage.as_view()),

    # KYC
    path('kyc/upload/<int:user_id>/', views.CLKycHandler.as_view()),
    #     path('kyc/update_id/<int:user_id>/', views.CLUpdateID.as_view()),
    #     path('kyc/update_selfie/<int:user_id>/', views.CLUpdateSelfie.as_view()),
    
    # Generate insuree policy pdf
    path('generate_insuree_policy_pdf/<int:id_search>/', views.CLGeneratePDF_Policy.as_view()),
    
    # to be updated
    path('insuree_policy/issuance/settings/', views.InsureePolicyPDFSettings.as_view()),
    path('insuree_policy/issuance/settings/<int:pk>/', views.UpdateInsureePolicyPDFSettings.as_view()),
    path('insuree_policy/pdf/<int:id>/', views.InsureePolicyPDFIssuance.as_view()),
    path('ipa/prem/calculator/', views.IPAPremiumCalculator.as_view()),
    path('agent/assist/', views.AgentAssisted.as_view()),
 
    #payment / billing
    path('payment/<int:user_id>/dragon-pay/', views.CLDragonpay_redirect_payment.as_view()),
    path('payment/dragon-pay/<str:txn_id>/', views.CL_GetDragonPayTransactionRefNo.as_view()),
    path('payment/transactions/all/', views.Transactions.as_view()),
    path('payment/<int:user_id>/', views.CLPaymentView.as_view()),
    #path('billingx/', views.CLPaymentBeta.as_view()),

    # App Stat
    path('stats/downloads/', views.AppDownloadCount.as_view()),
    path('stats/users/', views.CocoInsureeStats.as_view()),

    path('yrct10/', views.YRCT10.as_view()),

    path('yrct10/<int:age>/<int:face_amount>/',views.YRCT10.as_view()),

    # Company Information
    path('companyinformation/pdf/', views.CompanyInformation.as_view()),
]
