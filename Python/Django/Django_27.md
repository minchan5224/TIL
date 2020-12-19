# Django 프로젝트
##### Date 2020_12_19
원래 오늘은 댓글과 프로젝트(뭐랄까 카테고리? 가 가장 적절하네요) 만들려고 했습니다.

하지만 그냥 그렇게 하는것보다 댓글에 대댓글(댓글의 댓글)을 구현 하는게 더 좋을 것이라는 생각이 들었습니다.

그래서 만들었습니다.

---

### 당연히 startapp 해야겠죠
기본적인 과정은 [Django_18](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_18.md)과 동일하게 하였습니다.

댓글은 commentapp. 대댓글은 recommentapp으로 만들었습니다.

여기서 각각의 코드는 아래와 같이 작성하였습니다.

1. commentapp
### .py 파일
#### models.py
```Python
from django.contrib.auth.models import User
from django.db import models
from articleapp.models import Article

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='comment')
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')

    content = models.TextField(null=False)

    create_at = models.DateTimeField(auto_now=True)
```
#### forms.py
```Python
from django.forms import ModelForm
from commentapp.models import Comment

class CommentCreationForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```
#### urls.py
```Python
from django.urls import path
from commentapp.views import CommentCreateView, CommentDeleteView, CommentDetailView

app_name = 'commentapp'

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>', CommentDeleteView.as_view(), name='delete'),
    path('detail/', CommentDetailView.as_view(), name='detail'),
]
````
#### views.py
```Python
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView

from commentapp.forms import CommentCreationForm
from commentapp.models import Comment
from articleapp.models import Article

from commentapp.decorators import comment_ownership_required
from django.utils.decorators import method_decorator

from recommentapp.forms import RecommentCreationForm
from django.views.generic.edit import FormMixin

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = 'commentapp/create.html'

    def form_valid(self, form):
        temp_comment = form.save(commit=False) #임시 저장
        temp_comment.article = Article.objects.get(pk=self.request.POST['article_pk'])
        # 리퀘스트에서 받은 post데이터중 article_pk라는 데이터를 article값으로 설정해주는것
        # 즉 create.html에서 hidden으로 보낸 article.pk가 이쪽으로 넘어 오는것
        temp_comment.writer = self.request.user
        temp_comment.save() # 최종적으로 저장
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})
        # object(comment)의 article의 pk를 가진 detail로 되돌아 가는것.

@method_decorator(comment_ownership_required, 'get')
@method_decorator(comment_ownership_required, 'post')
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = 'target_comment'
    template_name = 'commentapp/delete.html'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})

class CommentDetailView(ListView):
    model = Comment
    context_object_name = 'target_comment'
    template_name = 'commentapp/detail.html'
    paginate_by = 2
```
#### decoratorys.py
```Python
from django.http import HttpResponseForbidden
from commentapp.models import Comment

def comment_ownership_required(func):
    def decorated(request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 profile이 된다.
        if not comment.writer == request.user: #그 article request의 profile이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)
    return decorated
```
### .html 파일
#### create.html
```html
{% load bootstrap4 %}

{% block content %}
    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div class="mb-4">
        </div>
        <form action="{% url 'commentapp:create' %}" method="post">
            {% csrf_token %}
            <textarea name="content" cols="40" rows="10" class="form-control" placeholder="댓글을 작성하세요."
                       title="" required="" id="id_content" style="margin-top: 1rem; margin-bottom: 1rem; height: 4rem; white-space: pre-line;"></textarea>
            
            {% if user.is_authenticated %}
            <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
            {% else %}
            <a herf="{% url 'accountapp:login' %}?next={{ request.path }}" class="btn btn-dark rounded-pill col-6 mt-3">
                Login
            </a>
            {% endif %}
            <input type="hidden" name="article_pk" value="{{ article.pk }}">
            <!--이름과 값이 article_pk인 인자를 숨겨서 보내준다.-->
        </form>
    </div>
{% endblock %}
```
#### detail.html
```html
 {% for comment in comments %}   
    <div style="border: 1px solid; text-align: left; padding: 4%; margin: 1rem 0; border-radius: 1rem; border-color: #bbb;">
        <div style="">
            <strong >
                <a href="{% url 'accountapp:detail' pk=comment.writer.pk %}">
                    {{ comment.writer.profile.nickname }}
                </a>
            </strong>
            <h6 style="text-align: right; font-size: small;">
                {{ comment.create_at }}
            </h6>

        </div>
        <div style="margin: 1rem 1rem; word-wrap:break-word;">
            {{ comment.content|linebreaksbr }}
        </div>
        {% if  comment.writer == user %}
        <div style="text-align: right">
            <a href="{% url 'commentapp:delete' pk=comment.pk %}"class="btn btn-danger rounded-pill">
                삭제
            </a>
        </div>
        {% endif %}
        <div style="margin-top: 3rem;">
                {% for recomment in comment.recomment.all %}
                <!--target_article.comment.all = target_article에 외래키로 연결되어 있는 댓글을 전부 가져온다.-->
                {% include 'recommentapp/detail.html' with recomment=recomment %}
                {% endfor %}
                <!--안에 있는 article을 현재 있는target_article과 동기화 시킨다.-->
                {% include 'recommentapp/create.html' with article=target_comment %}
        </div>
    </div>
{% endfor %}
```
#### delete.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div class="mb-4">
            <h4>댓글 삭제 : {{ target_comment.content }}</h4>
        </div>
        <form action="{% url 'commentapp:delete' pk=target_comment.pk %}" method="post">
            {% csrf_token %}
              <input type="submit" class="btn btn-danger rounded-pill col-6 mt-3">
        </form>
    </div>

{% endblock %}
```

2. recommentapp
### .py 파일
#### models.py
```Python
from django.contrib.auth.models import User
from django.db import models
from articleapp.models import Article
from commentapp.models import Comment

class Recomment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # related_name='recomment'  Article.recomment 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 Article.pk 랑 했음 article = Article.pk
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # on_delete=models.SET_NULL 회원 탈퇴시 게시글이 사라지는 것이 아닌 주인이 없는 게시글로 되도록
    # related_name='recomment'  user.recomment 사용하는 것이 더 직관적이기 때문에.
    # 외래키 이용 User.pk 랑 했음 writer = User.pk
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, related_name='recomment')
    # 외래키 이용 Comment.pk 랑 했음 comment = Comment.pk
    content = models.TextField(null=False)

    create_at = models.DateTimeField(auto_now=True)
```
#### forms.py
```Python
from django.forms import ModelForm
from recommentapp.models import Recomment

class RecommentCreationForm(ModelForm):
    class Meta:
        model = Recomment
        fields = ['content']
```
#### urls.py
```Python
from django.urls import path
from recommentapp.views import RecommentCreateView, RecommentDeleteView
app_name = 'recommentapp'

urlpatterns = [
    path('create/', RecommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>', RecommentDeleteView.as_view(), name='delete'),
]
```
#### views.py
```Python
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from recommentapp.forms import RecommentCreationForm
from recommentapp.models import Recomment
from commentapp.models import Comment
from articleapp.models import Article

from recommentapp.decorators import Recomment_ownership_required
from django.utils.decorators import method_decorator


class RecommentCreateView(CreateView):
    model = Recomment
    form_class = RecommentCreationForm
    template_name = 'recommentapp/create.html'

    def form_valid(self, form):
        temp_comment = form.save(commit=False) #임시 저장
        temp_comment.comment = Comment.objects.get(pk=self.request.POST['comment_pk'])
        temp_comment.article = Article.objects.get(pk=self.request.POST['article_pk'])
        # 리퀘스트에서 받은 post데이터중 comment_pk 데이터를 comment 설정해주는것
        # 즉 create.html에서 hidden으로 보낸 comment.pk가 이쪽으로 넘어 오는것
        temp_comment.writer = self.request.user
        temp_comment.save() # 최종적으로 저장
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})
        # object(comment)의 article의 pk를 가진 detail로 되돌아 가는것.

@method_decorator(Recomment_ownership_required, 'get')
@method_decorator(Recomment_ownership_required, 'post')
class RecommentDeleteView(DeleteView):
    model = Recomment
    context_object_name = 'target_comment'
    template_name = 'recommentapp/delete.html'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.request.POST['article_pk']})
```
#### decoratorys.py
```Python
from django.http import HttpResponseForbidden
from recommentapp.models import Recomment

def Recomment_ownership_required(func):
    def decorated(request, *args, **kwargs):
        recomment = Recomment.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 profile이 된다.
        if not recomment.writer == request.user: #그 article request의 profile이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)
    return decorated
```
### .html 파일
#### create.html
```html
{% load bootstrap4 %}

{% block content %}
    <div style="text-align: center; max-width: 450px; margin: 4rem auto;">
        <div class="mb-4">
        </div>
        <form action="{% url 'recommentapp:create' %}" method="post">
            {% csrf_token %}
            <textarea name="content" cols="40" rows="10" class="form-control" placeholder="댓글을 작성하세요."
                       title="" required="" id="id_content" style="margin-top: 1rem; margin-bottom: 1rem; height: 4rem; white-space: pre-line;"></textarea>
            
            {% if user.is_authenticated %}
            <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
            {% else %}
            <a herf="{% url 'accountapp:login' %}?next={{ request.path }}" class="btn btn-dark rounded-pill col-6 mt-3">
                Login
            </a>
            {% endif %}
            <input type="hidden" name="comment_pk" value="{{ comment.pk }}">
            <input type="hidden" name="article_pk" value="{{ comment.article.pk }}">
            <!--이름과 값이 article_pk인 인자를 숨겨서 보내준다.-->
        </form>
    </div>
{% endblock %}
```
#### detail.html
```html
<div style="border: 1px solid; text-align: left; padding: 4%; margin: 1rem 0; border-radius: 1rem; border-color: #bbb;">
    <div style="">
        <strong >
            <a href="{% url 'accountapp:detail' pk=recomment.writer.pk %}">
                {{ recomment.writer.profile.nickname }}
            </a>
        </strong>
        <h6 style="text-align: right; font-size: small;">
            {{ recomment.create_at }}
        </h6>
        {{recomment}}
    </div>
    <div style="margin: 1rem 1rem; word-wrap:break-word;">
        {{ recomment.content|linebreaksbr }}
    </div>
    {% if  recomment.writer == user %}
    <div style="text-align: right">
        <a href="{% url 'recommentapp:delete' pk=recomment.pk %}"class="btn btn-danger rounded-pill">
            삭제
        </a>
    </div>
    {% endif %}
</div>
```
#### delete.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div class="mb-4">
            <h4>댓글 삭제 : {{ target_comment.content }}</h4>
            {{ target_comment.article.pk }}
        </div>
        <form action="{% url 'recommentapp:delete' pk=target_comment.pk %}" method="post">
            {% csrf_token %}
            <input type="submit" class="btn btn-danger rounded-pill col-6 mt-3">
            <input type="hidden" name="article_pk" value="{{ target_comment.article.pk }}">
        </form>
    </div>

{% endblock %}
```
