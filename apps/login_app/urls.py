from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^main$', views.index),
	url(r'^quotes$', views.landing),
	url(r'^register$', views.register),
	url(r'^newquote$', views.newquote),
	url(r'^addFavorite$', views.addFavorite),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^removeFavorit', views.removeFavorit),
	url(r'^users/(?P<userID>\d+)$', views.userspage),
]