from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('enter_page/', enter_page, name='enter_page'),
    path('enter_page/result_page/', result_page, name='result_page'),
]