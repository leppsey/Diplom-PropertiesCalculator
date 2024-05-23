from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('Afirst_page/', Afirst_page, name='Afirst_page'),
    path('Afirst_page/Aenter_page/', Aenter_page, name='Aenter_page'),
    path('Afirst_page/Aenter_page/Aresult_page/', Aresult_page, name='Aresult_page'),
    path('Benter_page/', Benter_page, name='Benter_page'),
    path('Benter_page/Bresult_page/', Bresult_page, name='Bresult_page'),
]