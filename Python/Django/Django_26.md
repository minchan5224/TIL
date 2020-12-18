# Django 프로젝트
##### Date 2020_12_18
오늘은 이전에 사용했던 것들에서 많이 달라지지 않았습니다.

그래도 구독기능 응용해서 좋아요 싫어요 내일 구현해 볼게요
---

1. deleteView 생성했음.
```
<input type="submit" class="btn btn-danger rounded-pill col-6 mt-3" onclick="return confirm('정말 삭제 하시겠습니까?');">
```
요고 써서 알림한번 더띄움 ㅠ

2. decorator 사용해서 인증과정 간소화.
```from django.contrib.auth.decorators import login_required``` 로그인 인증관련

```from django.utils.decorators import method_decorator``` 데이코레이터 사용관련

본인 확인 과정은 accountapp 내부에 decorators.py 파일을 생성해 아래와 같이 작성한다.

```Python
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 user이 된다.
        if not user == request.user: #그 user이 request의 abs()이 아니라면
            return HttpResponseForbidden() #권한없음 창 띄움.
        return func(request, *args, **kwargs)

    return decorated
    
```
다음 views.py에서 import 하여 사용한다.```from accountapp.decorators import account_ownership_required```

```has_ownership = [account_ownership_required, login_required]``` 를 이용해 리스트에 담아 아래와 같이 사용가능하다.

```Python
@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')

3. profileapp 생성및 작성. (프로필)
```python manage.py startapp profileapp```

settings.py와urls.py 에 app 등록.

profileapp내부에 urls.py생성한뒤 아래 내용 작성(임시)
```Python
from django.urls import path
app_name = 'profileapp'
urlpatterns = [
]
```

같은 위치에 models.py 수정
```Python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # OneToOneField는 1:1관계를 의미한다.
    # on_delete=model.CASCADE 탈퇴하면 프로필도 함께 삭제되도록 하는것.
    # related_name='profile' 이건 requset.user.profile를 통해 바로 연결 가능하도록 설정 해주는것
    # 따로 프로필 객체를 찾을 필요가 없다.
    image = models.ImageField(upload_to='profile/', null=True)
    # 이미지를 받아서 서버 내부의 어느곳에 저장될 것인지 경로를 정해주는것.
    # null=True 는 프로필 사진이 없어도 된다는 뜻.
    nickname = models.CharField(max_length=20, unique=True, null=True)
    # unique=True 닉네임 중복 불허
    message = models.CharField(max_length=100, null=True)
    # 대화명
```

forms.py생성 및 작성
```
from django.forms import ModelForm

from profileapp.models import Profile

class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'nickname', 'message']
```
이젠 마이그레이션 ```python manage.py makemigrations```, ```python manage.py migrate``` 한다.

그리고 CreateView를 구현한다.

이부분의 코드들은 Django실습에서 사용한 코드와 동일한 코드를 재사용했다.

프로필 부분은 크게 바꿀점이 없다고 생각해서다.

html들도 역시 마찬가지다.

accountapp의 detail.html 아래와 같이 수정
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">

        {% if target_user.profile %}<!--proifle이 있다면 시작-->
        <img src="{{ target_user.profile.image.url }}" alt="" style="height: 12rem; width: 12rem; border-radius: 20rem; margin-bottom: 2rem;">
        <br>{{ target_user.profile.nickname }}
        
        {% if target_user == user %}<!--로그인한 사람과 프로필 소유자가 같은지 검증 시작-->
        <a href="{% url 'profileapp:update' pk=target_user.profile.pk %}">
            📝<br>
        </a>
        {% endif %}<!--로그인한 사람과 프로필 소유자가 같은지 검증 끝-->
        {{ target_user.profile.message }}<br>
        {% else %}<!--proifle이 없다면 시작-->
        <h2>
            프로필 미설정
        </h2>
        {% if target_user == user %}<!--로그인한 사람과 프로필 소유자가 같은지 검증 시작-->
        <a href="{% url 'profileapp:create' %}">
            <p>
                프로필 작성
            </p>
        </a>
        {% endif %}<!--로그인한 사람과 프로필 소유자가 같은지 검증 끝-->
        {% endif %}
        
        <div style="margin-top: 3rem;">
            {% if target_user == user %}
            <a class="material-icons" style="box-shadow: 0 0 4px #ccc; border-radius: 10rem; padding: .4rem;" href="{% url 'accountapp:update' %}">
                settings
            </a><!--계정 설정 버튼 보여줌-->
            <a href="{% url 'accountapp:delete' pk=user.pk %}" class = "btn btn-danger rounded-pill col-2 mt-3">
                탈 퇴
            </a>
            {% endif %}
        </div>
        
    </div>

{% endblock %}
```
정리를 조금 했다.

이제 articleapp할거다.

4. articleapp 시작.
늘 그렇듯 스타드앱 해준다.

그리고 settings와 urls에 등록하고 urls에 임시 경로 작성, models, forms작성한다.

그리군 역시 마이그레이션 한다. 다음 views기능 구현과 urls에 경로를 작성한다.
```
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from articleapp.forms import ArticleCreationForm
from articleapp.models import Article

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articleapp.decorators import article_ownership_required
from django.utils import timezone


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

class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'


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
views.py는 위와같이 작성하였다.

CreateView에서는 writer을 저장하기 위해 request를 보낸 사람의pk를 가져와 writer로저장한다.

그리고 현재 시간을 가져와 생성 시간으로 저장해 준다.

나머지 업데이트와 디테일 같은 부분은 크게 다른점은 없다.

articleapp는 전반적으로 수정할 사항이 없기 때문에 django실습에서 진행하였던 내용과 같다.

Django_16.md 파일의 내용부터 시작이다. 기억안나면 다시 찾아보자

list까지 정상적으로 동작하는 것을 확인 하였다.

오늘은 여기가지 할 것이다.

오늘은 프로필과 게시물(article)을 하였고

내일은 댓글기능을 끝마칠 것이다. 

안녕.
