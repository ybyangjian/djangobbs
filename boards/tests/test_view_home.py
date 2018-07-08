__author__ = 'yangjian'
__date__ = '2018/7/4 23:09'

from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board
from boards.views import home, BoardListView


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

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)