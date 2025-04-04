from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student_details/', views.student_details, name='student_details'),
    path('exam_pattern/', views.exam_pattern, name='exam_pattern'),
    path('instructions/', views.instructions, name='instructions'),
    path('camera_access/', views.camera_access, name='camera_access'),
    path('exam/', views.start_test, name='start_test'),
    path('exam/<str:section_name>/', views.exam_section, name='exam_section'),
    path('feedback/', views.feedback, name='feedback'),
    path('result/', views.result, name='result'),
    path('submit/', views.submit_assessment, name='submit_assessment'),

]

