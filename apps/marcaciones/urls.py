
from django.urls import path

from apps.marcaciones.views import proceso

app_name = 'marcaciones'

urlpatterns = [
    path('proceso', proceso, name='proceso'),
]
