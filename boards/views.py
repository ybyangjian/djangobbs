from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView

from boards.forms import NewTopicForm, PostForm
from .models import Board, Topic, Post


# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

#贴子列表
def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    #获取回复帖子的数量
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request,'topics.html',{'board':board,'topics':topics})

class TopicsListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board,pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


#创建新贴子
@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(message=form.cleaned_data.get('message'),topic=topic,created_by=request.user)
            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})

#贴子详情
def topic_posts(request,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request,'topic_posts.html',{'topic':topic})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return  super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def reply_topic(request,pk,topic_pk):
    topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts',pk=pk,topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})

#编辑帖子 ,登录的用户才可以修改
@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    #关键字参数名称
    pk_url_kwarg = 'post_pk'
    #传递到模板的参数
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    #设置额外的字段
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)


