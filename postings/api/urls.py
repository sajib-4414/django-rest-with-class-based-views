from .views import BlogPostRudView, BlogPostApiView
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    url(r'^$', BlogPostApiView.as_view(), name='post-listcreate'),
]