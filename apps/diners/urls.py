from django.urls import path

from apps.diners.views import proceso, carga, procesa, historico

app_name = 'diners'

urlpatterns = [
    path('proceso', proceso, name='proceso'),
    path('carga', carga, name='carga'),
    path('procesa', procesa, name='procesa'),
    path('historico', historico, name='historico'), 
]
