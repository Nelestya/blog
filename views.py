from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment
from baseapp.models import Application
from django.core.mail import send_mail
from .forms import CommentPostForm, EmailPostForm

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
        applications = Application.objects.all()
        post = get_object_or_404(Post, slug=post,
                                       status='published',
                                       publish__year=year,
                                       publish__month=month,
                                       publish__day=day)
        try:
            comments = Comment.objects.all().filter(post=post.id)
        except:
            pass

        context = {'post': post,
                   'applications': applications,
                   'comments': comments}

        return render(request, 'blog/post/detail.html', context)



class PostShare(View):
    sent = False

    def get(self, request, post_id):
        form = EmailPostForm()
        post = get_object_or_404(Post, id=post_id, status='published')


        context = {'post': post,
                   'form': form,
                   'sent': self.sent}

        return render(request, 'blog/post/share.html', context)

    def post(self, request, post_id):
        form = EmailPostForm(request.POST)
        post = get_object_or_404(Post, id=post_id, status='published')
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], self.post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'tristand.pro@gmail.com', [cd['to']])
            self.sent = True

        context = {'post': post,
                   'form': form,
                   'sent': self.sent
                   }
        return render(request, 'blog/post/share.html', context)
