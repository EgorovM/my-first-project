from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='help'),
    url(r'^(?P<order_id>[0-9]+)/$', views.order, name='order'),
]
