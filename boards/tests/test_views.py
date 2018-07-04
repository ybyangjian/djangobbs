from django.test import TestCase
from django.urls import reverse, resolve

from boards.forms import NewTopicForm
from boards.models import Board,Topic,Post
from boards.views import home,board_topics,new_topic


# Create your tests here.


class HomeTests(TestCase):
    '''
    python manage.py test  运行命令
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django',description='DJango版块')
        url = reverse('home')
        self.response = self.client.get(url)
    def test_home_view_status_code(self):
        '''
        测试访问主页返回的状态码是不是200
        :return:
        '''
        self.assertEqual(self.response.status_code,200)

    def test_home_url_resolves_home_view(self):
        '''
        将浏览器发起请求的URL与urls.py模块中列出的URL进行匹配，用于确定URL / 返回 home 视图
        :return:
        '''
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics',kwargs={'pk',self.board.pk})
        self.assertContains(self.response,'herf="{0}"'.format(board_topics_url))

class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topic_url = reverse('board_topics',kwargs={'pk':1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(board_topic_url)
        self.assertContains(response,'href="{0}"'.format(homepage_url))
        self.assertContains(response,'href="{0}"'.format(new_topic_url))

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


