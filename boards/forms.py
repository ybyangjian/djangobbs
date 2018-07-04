__author__ = 'yangjian'
__date__ = '2018/6/29 15:06'

from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(),max_length=4000,help_text='文本的最大长度为4000。')

    class Meta:
        model = Topic
        fields = ['subject','message']