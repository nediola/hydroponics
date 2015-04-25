from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    # url(r'^$', 'hydroplants.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'mainpageapp.views.authenticate'),
    url(r'login/', 'mainpageapp.views.login'),
    url(r'logout/', 'mainpageapp.views.logout'),
]