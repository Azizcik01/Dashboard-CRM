from django.urls import path
from dash.views import emp, about, create, edit, delete, index
from dash.services.auth import sign_in, sign_up, step_two, re_otp



urlpatterns = [
    
    path('', index, name='index'),

    #       Ishchi
    path('ishchi/', emp, name='emp'),
    path('ishchi/about/<int:pk>', about, name='about'),
    path('ishchi/create/', create, name='create'),
    path('ishchi/edit/<int:pk>', edit, name='edit'),
    path('ishchi/delete/<int:pk>/<int:conf>', delete, name='delete'),


    #       Auth
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-up/', sign_up, name='sign-up'),
    path('otp/', step_two, name='otp'),
    path('resent/', re_otp, name='re-otp')
    

]
