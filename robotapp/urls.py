from django.conf.urls import include, url

urlpatterns = [
    url(r'^', 'robotapp.views.load_robot'),
]