from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from boards.forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})

def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    user = User.objects.first()  # 临时用一个帐号作为登录用户

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(message=form.cleaned_data.get('message'),topic=topic,created_by=user)
        return redirect('board_topics',pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})
