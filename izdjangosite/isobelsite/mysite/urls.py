from django.conf.urls import url
from mysite import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^projects/$', views.AboutPageView.as_view(), name='projects'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^thanks/$', views.thanks, name='thanks'),
]