from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from .views import PostDetail, PostList, PostShare, Admin_Post_Preview

app_name = 'blog'
urlpatterns = [
    url(r'^$', PostList.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^share/(?P<post_id>\d+)/$', PostShare.as_view(), name='post_share'),
    url(r'^admin/post/(?P<post_id>\d+)/$', staff_member_required(Admin_Post_Preview.as_view()), name='admin_post_preview'),
    ]
