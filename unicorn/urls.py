from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'unicorn.views.index'),
    url(r'^about$', 'unicorn.views.about'),
    url(r'^blog$', 'unicorn.views.blog'),
    url(r'^games/', include('games.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

 	url(r'^accounts/profile/(?P<id>\d+)/$','games.views.profile'),
    url(r'^accounts/profile/$','games.views.profile'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    #(r'^profiles/', include('profiles.urls')),
)
