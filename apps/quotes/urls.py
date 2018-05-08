from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^users/(?P<posted_by>\d+)', views.users),
	url(r'^add', views.add),
	url(r'^logout', views.logout),
	url(r'^quotes', views.home),
	url(r'^login', views.login),
	url(r'^main', views.index)
]