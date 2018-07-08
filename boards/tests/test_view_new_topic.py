__author__ = 'yangjian'
__date__ = '2018/7/4 23:10'

from django.test import TestCase
from django.urls import reverse, resolve

from boards.forms import NewTopicForm
from boards.models import Board
from boards.views import new_topic

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_new_topic_view_success_status_code(self):
        #检查发给 view 的请求是否成功
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        #检查当 Board 不存在时 view 是否会抛出一个 404 的错误
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        #检查是否正在使用正确的 view
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        #确保导航能回到 topics 的列表
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

class LoginRequiredNewTopicTests(TestCase):
   def setUp(self):
       Board.objects.create(name='Django', description='Django board.')
       self.url = reverse('new_topic', kwargs={'pk': 1})
       self.response = self.client.get(self.url)

   def test_redirection(self):
       login_url = reverse('login')
       self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
