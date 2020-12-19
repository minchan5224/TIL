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

### 1. commentapp
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
<!--버튼 클릭시 보이기 숨기기 기능 구현.-->
<script>
    function SettingFunction(idMyDiv){
        var objDiv = document.getElementById(idMyDiv);
        if(objDiv.style.display=="block"){ objDiv.style.display = "none"; }
        else{ objDiv.style.display = "block"; }
    }
</script>
<style>
    .hide_show_setting{color:black;margin-bottom:30px}
    .hide_show_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
    .hide_show_setting .blind_view{}
    .hide_show_setting_view { display:none; }
</style>

{% for comment in comments %}   
    <div style=" padding: 4%; margin: 1rem 0; border-radius: 1rem; background-color: #edfcf8">
        {% if  comment.writer == user %}<!--작성자랑 리퀘스트 보낸사람이 같을때-->
        <div class="comment_setting_inner" ><!--버튼 생성(누르면 삭제 버튼 나오게)-->
            <div class="hide_show_setting">
                <strong style=" text-align: left;">
                    <a href="{% url 'accountapp:detail' pk=comment.writer.pk %}">
                        {{ comment.writer.profile.nickname }}
                    </a>
                </strong>
                <div style="text-align: right; margin: -1.6rem 0">
                    <a href="#" onclick="SettingFunction('{{comment.pk}}'); return false;" class="blind_view">
                        <h6 class="material-icons"><!--버튼 아이콘-->
                            more_horiz
                        </h6>
                    </a>
                </div>
            </div>
        </div>
        {% else %}<!--리퀘스트 보낸게 작성자가 아닐때 닉네임출력-->
            <strong style=" text-align: left;">
                <a href="{% url 'accountapp:detail' pk=comment.writer.pk %}">
                    {{ comment.writer.profile.nickname }}
                </a>
            </strong>
        {% endif %}
        <div style="margin: 1rem 1rem; word-wrap:break-word; "><!--댓글 내용 출력-->
            {{ comment.content|linebreaksbr }}
        </div>
        <div style="text-align: right; font-size: small;"><!--작성일-->
            <h6 style="font-size: small;">
                {{ comment.create_at }}
            </h6>
            <div class="comment_setting_view" id="{{comment.pk}}"><!--위에서 버튼 눌렀을때 숨겨져있던 버튼이 보여지는 부분-->
                <a href="{% url 'commentapp:delete' pk=comment.pk %}"class="btn btn-outline-danger rounded-pill" style="font-size: small;">
                    삭제
                </a>
            </div>
        </div>
        {% if comment.recomment.count != 0 %}<!--대댓글이 있다면. 실행-->
            <div class="recomment_view_setting_inner" ><!--버튼 보이기 감추기 구현-->
                <div class="hide_show_setting">
                    <a href="#" onclick="SettingFunction('RecommentsDiv'); return false;" class="blind_view">
                        <h6 class="material-icons" style="font-size: 0.6em; text-decoration:underline;">
                            답글 더보기<!--대댓글이 있다면 더보기 버튼 활성화. 누르면 대댓글 나옴-->
                        </h6>
                    </a>
                </div>
                <div class="recomments_setting_view" id="RecommentsDiv" style="text-align: right; font-size: 0.8em;"><!--대댓글가져오는 부분-->
                    <div style="margin-top: -3rem;">
                        {% for recomment in comment.recomment.all %}
                        <!--target_article.comment.all = target_article에 외래키로 연결되어 있는 댓글을 전부 가져온다.-->
                        {% include 'recommentapp/detail.html' with recomment=recomment %}
                        {% endfor %}
                        <!--안에 있는 article을 현재 있는target_article과 동기화 시킨다.-->
                        {% include 'recommentapp/create.html' with article=target_comment %}
                    </div>
                </div>
            </div>
            
        {% endif %}
        
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

### 2. recommentapp
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
<!--버튼 클릭시 보이기 숨기기 기능 구현.-->

<style>
    .hide_show_setting{color:black;margin-bottom:30px}
    .hide_show_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
    .hide_show_setting .blind_view{}
    .hide_show_setting_view { display:none; }
</style>


<div style="float: left; width: 10%;"> <!--대댓글 화살표-->
    <h5 class="material-icons" style="border-radius: 10rem; padding: .4rem; margin-top: 1rem; margin-right: 1rem;"><!--subdirectory_arrow_right-->
    subdirectory_arrow_right
    </h5>
</div>
    
<div style="text-align: left; padding: 4%; margin: 1rem 0; border-radius: 1rem; float: left; width: 90%;background-color: #e0faf3">
    {% if  recomment.writer == user %}<!--작성자랑 리퀘스트 보낸사람이 같을때-->
        <div class="recomment_setting_inner" ><!--버튼 생성(누르면 삭제 버튼 나오게)-->
            <div class="hide_show_setting">
                <strong style=" text-align: left;">
                    <a href="{% url 'accountapp:detail' pk=recomment.writer.pk %}">
                        {{ recomment.writer.profile.nickname }}
                    </a>
                </strong>
                <div style="text-align: right; margin: -1.6rem 0">
                    <a href="#" onclick="SirenFunction('{{recomment.pk}}'); return false;" class="blind_view">
                        <h6 class="material-icons"><!--버튼 아이콘-->
                            more_horiz
                        </h6>
                    </a>
                </div>
            </div>
        </div>
    {% else %}<!--리퀘스트 보낸게 작성자가 아닐때 닉네임출력-->
    <div>
        <strong >
            <a href="{% url 'accountapp:detail' pk=recomment.writer.pk %}">
                {{ recomment.writer.profile.nickname }}
            </a>
        </strong>
    </div>
    {% endif %}
    <div style="margin: 1rem 1rem; word-wrap:break-word;"><!--댓글 내용 출력-->
        {{ recomment.content|linebreaksbr }}
    </div>
    <div>
        <h6 style="text-align: right; font-size: 0.8em;"><!--작성일-->
            {{ recomment.create_at }}
        </h6>
        <div class="hide_show_setting_view" id="{{recomment.pk}}" style="text-align: right;"><!--위에서 버튼 눌렀을때 숨겨져있던 버튼이 보여지는 부분-->
            <a href="{% url 'recommentapp:delete' pk=recomment.pk %}"class="btn btn-outline-danger rounded-pill" style="font-size: 0.8em;">
                삭제
            </a>
        </div>
    </div>

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
### 3. articleapp
#### views.py
```Python
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from articleapp.forms import ArticleCreationForm
from articleapp.models import Article

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articleapp.decorators import article_ownership_required
from django.utils import timezone

from commentapp.forms import CommentCreationForm
from django.views.generic.edit import FormMixin


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/create.html'

    def form_valid(self, form):
        temp_article = form.save(commit=False) # 임시저장
        temp_article.writer = self.request.user # 지금 리퀘스트를 보낸 사람을 writer로 저장
        temp_article.created_at = timezone.localtime()
        temp_article.save() #저장
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})

class ArticleDetailView(DetailView, FormMixin):
    # FormMixin을 이용해 다중 상속을 받는다.
    model = Article
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'
    form_class = CommentCreationForm
    # 필요한 form을 가져온다.


@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/update.html'
    context_object_name = 'target_article'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html'

class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 25
    # 하나의 페이지에 몇개의 객체를 보여줄 것인지
    # Pagination을 하면 page_obj를 사용할 수 있다.
```
#### detail.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}


{% block content %}

<style>
    .articl_setting{color:black;margin-bottom:30px}
    .articl_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
    .articl_setting .blind_view{font-size:1.5em}
    .articl_view { display:none; }
</style>

    <div>
        <div style="text-align: center; max-width: 500px; margin: 2rem auto;">
            <h1>
                {{ target_article.title }}
            </h1>
            <div style=" margin-top: 2rem">
                <h6 style="text-align: right; font-size: small;">
                    {{ target_article.created_at }}
                </h6>
            </div>
            <div class="articl_setting_inner"style="text-align: right;">
                <div class="articl_setting" style="text-align: right; margin-top: 1rem;">
                    {{ target_article.writer.profile.nickname }}
                    <a href="#" onclick="SettingFunction('ArticlDiv'); return false;" class="blind_view">
                        <h6 class="material-icons" style="font-size: medium; box-shadow: 0 0 4px #ccc; border-radius: 10rem; padding: .4rem;">
                            more_vert
                        </h6>
                    </a>
                </div>
                <div class="articl_view" id="ArticlDiv" style="text-align: right;">
                    <a href="{% url 'articleapp:update' pk=target_article.pk %}" class="btn btn-outline-primary rounded-pill col-2.3" style="font-size: small;">
                        게시물 수정
                    </a>
                    <a href="{% url 'articleapp:delete' pk=target_article.pk %}" class="btn btn-outline-danger rounded-pill col-2.3" style="font-size: small;">
                        게시물 삭제
                    </a>
                </div>
            </div>
            
            
            <img style="width:100%; border-radius: 1rem; margin: 2rem 0" src="{{ target_article.image.url }}" alt="">
            
            <div style="text-align: left; margin-top: 1rem;">
                <p>
                    {{ target_article.content }}
                </p>
            </div>
            
            
            
            <div style="text-align: left; padding: 4%; margin: 2rem 0; border-radius: 1rem; background-color: #f6fefc; font-size: 1em;">
                
                {% if target_article.comment.count == 0 %}
                        첫 댓글을 작성하세요!
                {% else %}
                <!--target_article.comment.all = target_article에 외래키로 연결되어 있는 댓글을 전부 가져온다.-->
                {% include 'commentapp/detail.html' with comments=target_article.comment.all %}
                <!--안에 있는 article을 현재 있는target_article과 동기화 시킨다.-->
                {% endif %}
                {% include 'commentapp/create.html' with article=target_article %}
                
            </div>            
        </div>
    </div>

{% endblock %}
```

### 4. 버튼 누르면 내용나오는것 구현
```
    <script>
    function ExFunction("내가 원하는 div id"){
         var objDiv = document.getElementById(idMyDiv);
         if(objDiv.style.display=="block"){ objDiv.style.display = "none"; }
          else{ objDiv.style.display = "block"; }
    }
    </script>
    <style> 그냥 스타일 설정부분
        .comment_setting{color:#934545;margin-bottom:30px}
        .comment_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
        .comment_setting .blind_view{font-size:1.14em;font-weight:bold;margin-top:-3px;text-decoration:underline}
        .setting_view { display:none; } 초기값
    </style>
    <div class="con_inner">
        <div class="comment_setting">
            <a href="#" onclick="SirenFunction('SirenDiv'); return false;" class="blind_view">
                <h6 class="material-icons" style="">
                more_horiz
                </h6>
            </a>
        </div>
        <div class="setting_view" id="내가 원하는 div id"> 위에서 선언한 ExFunction의 파라미터로 id를 전달하여 사용한다.
            내용보기
        </div>
    </div>
```

난 base.html에 스크립트 작성하여 어디서든 함수만 호출해서 사용하도록 하였다

base.html의 내용은 아래와 같다
```html
<!DOCTYPE html>
<html lang="ko">

{% include 'head.html' %}

<body style="background-color: #f5feff">
    <!--버튼 클릭시 보이기 숨기기 기능 구현.-->
    <script>
    function SettingFunction(idMyDiv){
        var objDiv = document.getElementById(idMyDiv);
        if(objDiv.style.display=="block"){ objDiv.style.display = "none"; }
        else{ objDiv.style.display = "block"; }
    }
    </script>
    
    {% include 'header.html' %}
    
    {% block content %}
    {% endblock %}

    {% include 'footer.html' %}
    
</body>
</html>

```
