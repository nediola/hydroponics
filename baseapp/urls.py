from django.conf.urls import include, url

urlpatterns = [
    url(r'^', 'baseapp.views.load_base'),
]