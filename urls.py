from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from .views import PostDetail, PostList, PostShare

app_name = 'blog'
urlpatterns = [
    url('$', PostList.as_view(), name='post_list'),
    url('(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', PostDetail.as_view(), name='post_detail'),
    url('share/(?P<post_id>\d+)/$', PostShare.as_view(), name='post_share')
    ]
