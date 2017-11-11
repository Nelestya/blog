from django.http import HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment
from baseapp.models import Application
from django.core.mail import send_mail
from .forms import CommentPostForm, EmailPostForm
from baseapp.views import FieldsView

# Create your views here.
class PostList(FieldsView):
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
                   'fields': self.fields,
                   }

        return render(request, 'blog/post/list.html', context)


class PostDetail(FieldsView):
    """
        Detail of post
    """
    applications = Application.objects.all()

    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post,
                                       status='published',
                                       publish__year=year,
                                       publish__month=month,
                                       publish__day=day)

        try:
            comments = Comment.objects.all().filter(post=post.id)
        except:
            pass

        comment_form = CommentPostForm()

        context = {
                    'post': post,
                    'fields': self.fields,
                    'comments': comments,
                    'comment_form': comment_form
                    }

        return render(request, 'blog/post/detail.html', context)


    def post(self, request, year, month, day, post):

        post = get_object_or_404(Post, slug=post,
                                       status='published',
                                       publish__year=year,
                                       publish__month=month,
                                       publish__day=day)
        try:
            comments = Comment.objects.all().filter(post=post.id)
        except:
            pass

        comment_form = CommentPostForm(request.POST)

        if comment_form.is_valid():
            try:
                cf_cleaned = comment_form.cleaned_data
                print(cf_cleaned)
                insert_db = Comment.objects.create(pseudo=cf_cleaned['pseudo'], mail=cf_cleaned['mail'], body=cf_cleaned['body'], post_id=post.id)
                insert_db.save()
                comment_form = CommentPostForm()
            except Exception as e:
                flag = "Exception while processing. (%s)" % e




        context = {'post': post,
                   'fields': self.fields,
                   'comments': comments,
                   'comment_form': comment_form
                   }

        return render(request, 'blog/post/detail.html', context)



class PostShare(FieldsView):
    sent = False
    applications = Application.objects.all()

    def get(self, request, post_id):
        form = EmailPostForm()
        post = get_object_or_404(Post, id=post_id, status='published')


        context = {'post': post,
                   'fields': self.fields,
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
            send_mail(subject, message, 'youradress.mail@host.com', [cd['to']])
            self.sent = True

        context = {'post': post,
                   'form': form,
                   'fields': self.fields,
                   'sent': self.sent
                   }
        return render(request, 'blog/post/share.html', context)

class Admin_Post_Preview(FieldsView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'admin/blog/preview.html', {'post': post})
