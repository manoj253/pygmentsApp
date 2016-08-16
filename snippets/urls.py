from django.conf.urls import url
from .import views
urlpatterns = [
	url(r'^$', views.index,name='index'),
	url(r'^create/$',views.createSnippet,name='createSnippet'),
	url(r'^pygview/(?P<pk>[0-9]+)/$',views.pygView,name='pygView'),
	url(r'^list/$',views.pyg_list,name='list'),
	url(r'^pygview/(?P<pk>[0-9]+)/edit/$',views.pyg_edit,name='edit'),

]