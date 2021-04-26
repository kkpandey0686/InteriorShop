#
#

from django.urls import path

#
#

from . import views

#
#

urlpatterns = [
    path('update_status/<int:id>/', views.updateStatus, name='updateStatus')
]