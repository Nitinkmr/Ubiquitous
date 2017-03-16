from django.conf.urls import url
import views

urlpatterns = [
    url(r'validate/',views.validate_account,name='validate'),
    url(r'get_details',views.get_details,name='details')
]
