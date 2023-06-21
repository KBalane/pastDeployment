from django.urls import path

from telco import views

app_name = 'telco'

urlpatterns = [

    path('profile/<int:user_id>/', views.TelcoProfile.as_view()),
    path('token-verify/<str:token>/', views.TokenVerify.as_view()),
    
    path('address/list/create/', views.AddressViewLC.as_view()),
    path('address/retrieve/update/delete/<int:user>/', views.AddressViewRUD.as_view()),

    # Sim
    path('sim/list/create/', views.SIMDetailsViewLC.as_view()),
    path('sim/retrieve/update/delete/<int:id>/', views.SIMDetailsViewRUD.as_view()),
    path('sim/list/specific/<int:user>/', views.SIMDetailsViewAllByID.as_view()),
    
    # Company
    path('company/list/create/', views.CompanyViewLC.as_view()),
    path('company/retrieve/update/delete/<int:id>/', views.CompanyViewRUD.as_view()),
    path('company/store/files/', views.CompanyStoreFiles.as_view()),
    path('company/retrieve/files/', views.CompanyRetrieveFiles.as_view()),
    path('company/retrieve/file/<int:id>', views.CompanyFileByID.as_view()),

    path('jumio/generate/token/', views.JumioGenerateToken.as_view()),
    path('jumio/account/initiate/', views.JumioInitiateAccount.as_view()),
    path('jumio/account/status/', views.JumioStatusAccount.as_view()),
    path('jumio/account/retrieve/', views.JumioRetrieveAccount.as_view()),

    path('jumio/token/list/create/', views.JumioTokenLC.as_view()),
    path('jumio/token/retrieve/update/delete/<int:id>/', views.JumioTokenRUD.as_view()),
    
    
    
    

]