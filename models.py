from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from baseapp.models import Recently
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(Recently):
    STATUS_CHOICE = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    activate = models.BooleanField(default=False)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug,
                                                 ])

class Comment(Recently):
    mail = models.EmailField()
    pseudo = models.CharField(max_length=30)
    body = models.TextField()
    post = models.ForeignKey('Post',
        on_delete=models.CASCADE,
        blank=False,
        related_name='comments')


    def __str__(self):
        return 'Commented by {} in {}'.format(self.pseudo, self.post)
