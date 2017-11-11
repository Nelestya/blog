from django.test import TestCase
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.test import Client
from django.utils import timezone
from .models import *
# Create your tests here.

TEST_RECEIVER_EMAIL = b"mail@host.com"
TEST_SENDER_EMAIL = b"mail@host.com"
CHARSET = "UTF-8"

USER_COMMENT_PARAMS = {
    'mail': '',
    'pseudo': '',
    'body': '',
    'post': '',
    }

POST_PARAM_ADMIN_published = {
    'title':'phase test',
    'slug':'phase test',
    'author':'1',
    'body':'Test Phase',
    'publish':timezone.now(),
    'status':'published',
    'image': None,
    'image_description': None,

}

POST_PARAM_ADMIN_draft = {
    'title':'phase test',
    'slug':'phase test',
    'author':'1',
    'body':'Test Phase',
    'publish':timezone.now(),
    'status':'draft',
    'image': None,
    'image_description': None,

}
class BlogTestModelCreation(TestCase):
    pass
    
class BlogIndexViewTests(TestCase):
    def test_page_list_nopost(self):
        """
        if no post display page
        """
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
