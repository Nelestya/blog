from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from baseapp.models import Application

# Create your views here.
class PostList(View):
    """
        list the posts
    """

    def get(self, request):
        posts = Post.published.all()
        applications = Application.objects.all()

        # Pagination
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {'posts': posts,
                   'page': page,
                   'applications': applications}

        return render(request, 'blog/post/list.html', context)

class PostDetail(View):
    """
        Detail of post
    """

    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post,
                                       status='published',
                                       publish__year=year,
                                       publish__month=month,
                                       publish__day=day)
        return render(request, 'blog/post/detail.html', {'posts': posts})
