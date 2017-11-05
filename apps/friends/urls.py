from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^friends$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^remove/(?P<friend_id>\d+)$', views.deletefriend), #<--- redirect /reviews/<book_id>
    url(r'^add/(?P<friend_id>\d+)$', views.addfriend),    #<---  redirect /review/<book_id>
    url(r'^user/(?P<friend_id>\d+)$', views.user),    #<--- render user.html
]
