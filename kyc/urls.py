from django.urls import path

from kyc import views

app_name = 'kyc'


urlpatterns = [
    path('kyc/camera/', views.show_camera, name='show_camera'),
    path('kyc/upload_id/', views.upload_user_id, name='upload_pic'),
    # path('compare_pic/', views.compare_faces, name='compare_faces'),
    path('kyc/upload_template/', views.upload_template_id,
         name='upload_template_id'),
    path('kyc/upload/template/', views.UploadTemplateIdHandler.as_view(),
         name='template_upload'),
    path('kyc/upload/id/', views.UploadUserIdHandler.as_view(),
         name='student_upload'),
    path('kyc/upload/compare/', views.CompareFacesHandler.as_view(),
         name='compare_faces'),
    path('kyc/upload/snapshot/', views.UploadSnapshot.as_view(),
         name='upload_snapshot'),

    path('kyc/ocr/', views.upload_ocr, name='upload_ocr')
]
