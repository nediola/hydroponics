from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'hydroplants.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mainpageapp.urls')),
    url(r'^base/', include('baseapp.urls')),
    url(r'^robot/', include('robotapp.urls')),
]
