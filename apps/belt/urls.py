from django.conf.urls import url

from . import views  # This line is new!

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^create$', views.createItem),
    url(r'^delete$', views.deleteItem),
    #url(r'^removefromlist$', views.removeFromlist),
    #url(r'^addtolist$', views.addTolist),
    # url(r'^additem$', views.addItem),
    url(r'^add$', views.add),
    url(r'^wish_items/(?P<number>\d+)$', views.viewItem)
]