from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'list/$', 'games.views.listgames'),
    url(r'submitgamebasic/$', 'games.views.submitgamebasic'),
    url(r'submitgamebasic/(?P<jam>\d+)/$', 'games.views.submitgamebasic'),
    url(r'submitgameplatforms/(?P<id>\d+)/$', 'games.views.submitgameplatforms'),
    url(r'submitgamecategories/(?P<id>\d+)/$', 'games.views.submitgamecategories'),
    url(r'submitgamemedia/(?P<id>\d+)/$', 'games.views.submitgamemedia'),
    url(r'submitgamecontact/(?P<id>\d+)/$', 'games.views.submitgamecontact'),
    url(r'submitgamepublish/(?P<id>\d+)/$', 'games.views.submitgamepublish'),
    url(r'submitgamepublished/(?P<id>\d+)/$', 'games.views.submitgamepublished'),

    url(r'game/(?P<id>\d+)/$', 'games.views.showgame'),
    url(r'editgamebasic/(?P<id>\d+)/$', 'games.views.editgamebasic'),
    url(r'editgameplatforms/(?P<id>\d+)/$', 'games.views.editgameplatforms'),
    url(r'editgamecategories/(?P<id>\d+)/$', 'games.views.editgamecategories'),
    url(r'editgamemedia/(?P<id>\d+)/$', 'games.views.editgamemedia'),
    url(r'editgamecontact/(?P<id>\d+)/$', 'games.views.editgamecontact'),

    url(r'jam/(?P<id>\d+)/$', 'games.views.showjam'),


    url(r'rategame/(?P<id>\d+)/(?P<type>\d+)/$', 'games.views.rategame'),


)
