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
### 3. articleapp
#### views.py
```Python
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth # 로그인

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accountapp.decorators import account_ownership_required

has_ownership = [account_ownership_required, login_required]
# 본인확인, 로그인 여부 확인 과정
# 리스트로 담아서 사용 가능하다.

class AccountCreateView(View):
    def post(self, request):
        user_id = request.POST.get('username',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)

        if User.objects.filter(username = user_id).exists() == True:
            message = "이미 존재하는 아이디입니다."

        elif password != re_password:
            message = "비밀번호가 다릅니다."

        elif user_id == '' or password == '':
            message = "모든 내용을 입력하세요."

        else:
            User.objects.create(username = user_id, password = make_password(password))
            return render(request, 'accountapp/success.html')

        return render(request, 'accountapp/create.html', {'message': message})

    def get(self, request):
        return render(request, 'accountapp/create.html')


class AccountSuccessView(View):
    model = User
    template_name = 'accountapp/success.html'
    def get(self, request):
        return render(request, 'accountapp/success.html')

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user' # 탬플릿에서 사용하는 user의 객체 이름을 target_user로 다르게 설정해줌
    # 로그인 한 상태에서 자신의 페이지로 들어와 정보를 볼 수 있었지만 이제 다른사람이 그 페이지에 들어가더라도 정상적으로 열람 가능하다.
    template_name = 'accountapp/detail.html'


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class AccountUpdateView(View):
    model = User
    def post(self, request):
        request_user = self.request.user
        origin_password = request.POST.get('origin-password', None)
        new_password = request.POST.get('password', None)
        re_password = request.POST.get('password2', None)
        if check_password(origin_password, request_user.password):
            if new_password == re_password:
                request_user.set_password(new_password)
                request_user.save()
                return HttpResponseRedirect(reverse('accountapp:success'))
            else:
                message = "새로운 비밀번호를 확인해주세요."
        elif origin_password == None or new_password == None or re_password == None :
            message = "모든 정보를 입력해야 합니다.bin()"
        else:
            message = "현재 사용중인 비밀번호를 확인해주세요."
        return render(request, 'accountapp/update.html', {'message': message})
    def get(self, request):
        return render(request, 'accountapp/update.html')


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'
```
#### detail.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}


{% block content %}

<script>
    function SirenFunction(idMyDiv){
        var objDiv = document.getElementById(idMyDiv);
        if(objDiv.style.display=="block"){ objDiv.style.display = "none"; }
        else{ objDiv.style.display = "block"; }
    }
</script>
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
                    <a href="#" onclick="SirenFunction('ArticlDiv'); return false;" class="blind_view">
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
            
            
            
            <div style="border: 1px solid; text-align: left; padding: 4%; margin: 2rem 0; border-radius: 1rem; border-color: #bbb;">
                
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
    function SirenFunction(idMyDiv){
         var objDiv = document.getElementById(idMyDiv);
         if(objDiv.style.display=="block"){ objDiv.style.display = "none"; }
          else{ objDiv.style.display = "block"; }
    }
    </script>
    <style>
        .comment_setting{color:#934545;margin-bottom:30px}
        .comment_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
        .comment_setting .blind_view{font-size:1.14em;font-weight:bold;margin-top:-3px;text-decoration:underline}
        .setting_view { display:none; }
    </style>
    <div class="con_inner">
        <div class="comment_setting">
            <a href="#" onclick="SirenFunction('SirenDiv'); return false;" class="blind_view">
                <h6 class="material-icons" style="">
                more_horiz
                </h6>
            </a>
        </div>
        <div class="setting_view" id="SirenDiv">
            내용보기
        </div>
    </div>
```
