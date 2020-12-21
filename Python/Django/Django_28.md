# Django 프로젝트
##### Date 2020_12_20~21
으아아 댓글 더보기/ 줄이기 구현

---
```html
<script>
function RecommendFunction(idMyDiv){
    var objDiv = document.getElementById(idMyDiv);
    if(objDiv.style.display=="block"){
        objDiv.style.display = "none";
        ButtonSetting.innerHTML = "댓글 더보기";

    }
    else{
        objDiv.style.display = "block";
        ButtonSetting.innerHTML = "댓글 접기";
    }
}
</script>

<style>
    .hide_show_setting{color:black;margin-bottom:30px}
    .hide_show_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
    .hide_show_setting .blind_view{}
    .hide_show_setting_view { display:block; }
</style>
```
기본적인 함수는 위와 같구 ```ButtonSetting.innerHTML = "댓글 더보기";```이 뭐냐면

ButtonSetting라는 아이디를 가진 태그의 텍스트를 "댓글 더보기" 바꾸겠다 입니다. 쉬워요;;

그리고 각 html에서 함수를 이용하기 위한 id들은 text와 pk등으로 구성된 이름으로 새로 만들었습니다.

와 어제부터 얼마나한건지 감이 잘 안잡히지만.

일단 오늘 마무리 하였습니다.

게시물에 대한 좋아요, 싫어요 기능

구독, 구독한 프로젝트(카테고리)를 list.view로 출력 하는것, 관리자 권한을 가진 사람만 프로젝트(카테고리)생성 가능

accountapp의 success.html을 삭제

아래는 프로젝트 앱과 구독 앱의 코드를 첨부하겠습니다.
### rojectapp
```Python
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, DeleteView

from projectapp.forms import ProjectCreationForm
from projectapp.models import Project

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import MultipleObjectMixin

from articleapp.models import Article
from subscribeapp.models import Subscription

@method_decorator(login_required,'get')
@method_decorator(login_required,'post')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projectapp/create.html'

    def get_success_url(self):
        return reverse('projectapp:detail', kwargs={'pk': self.object.pk})

class ProjectDetailView(DetailView, MultipleObjectMixin):
    model = Project
    context_object_name = 'target_project'
    template_name = 'projectapp/detail.html'

    paginate_by = 25

    def get_context_data(self, **kwargs):
        project = self.object
        user = self.request.user

        if user.is_authenticated: # 유저가 로그인 중이라면
            subscription = Subscription.objects.filter(user=user, project=project)
        else:
            subscription = None
        object_list = Article.objects.filter(project=self.get_object()).order_by('-created_at')
        # 현재의 프로젝트에 속한 아티클들만 필터링해서 가져옴
        return super(ProjectDetailView, self).get_context_data(object_list=object_list, subscription=subscription, **kwargs)

class ProjectListView(ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projectapp/list.html'
    
class ProjectDeleteView(DeleteView):
    model = Project
    context_object_name = 'target_project'
    success_url = reverse_lazy('projectapp:list')
    template_name = 'projectapp/delete.html'
```
Views.py입니다 사실 크게 어려운것은 없습니다.
```Python
# models.py
from django.db import models

class Project(models.Model):
    image = models.ImageField(upload_to='project/', null=False)
    title = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=600, null=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
        
# forms.py        
from django.forms import ModelForm
from projectapp.models import Project

class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = ['image', 'title', 'description']
        
        
        
# urls.py
from django.urls import path
from projectapp.views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectDeleteView

app_name = 'projectapp'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', ProjectDeleteView.as_view(), name='delete'),
]
```
위는 models.py와 forms.py,urls.py 입니다.

### subscribeapp

```Python
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views.generic import RedirectView, ListView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from subscribeapp.models import Subscription
from projectapp.models import Project
from articleapp.models import Article
from django.contrib.auth.models import User

@method_decorator(login_required, 'get')
class SubscriptionView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projectapp:detail', kwargs={'pk': self.request.GET.get('project_pk')})

    def get(self, requset, *args, **kwargs):
        project = get_object_or_404(Project, pk = self.request.GET.get('project_pk'))
        # project_pk가진 Project가 없다면 404  오류를 출력해라.
        user = self.request.user

        subscription = Subscription.objects.filter(user=user, project=project)

        if subscription.exists():
            subscription.delete()
        else:
            Subscription(user=user, project=project).save()

        return super(SubscriptionView, self).get(requset, *args, **kwargs)

@method_decorator(login_required, 'get')
class SubscriptionListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'subscribeapp/list.html'
    paginate_by = 20
    # article 전부를 가져오는 것이 아닌 특정 조건(구독여부)를 만족하는 aarticle을 가져올 것
    # 따라서 쿼리셋관련 함수를 새로 작성할 것이다.
    def get_queryset(self):
        projects = Subscription.objects.filter(user=self.request.user).values_list('project')
        # values_list : 값들을 리스트화 시킨다.
        # 따라서 projects에는 구독한모든 프로젝트가 리스트 형식으로 담긴다.
        article_list = Article.objects.filter(project__in=projects).order_by('-created_at')
        return article_list
``` 
위는 views.py입니다.

```Python
# models.py

from django.db import models
from django.contrib.auth.models import User
from projectapp.models import Project


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        unique_together = ('user', 'project')



# urls.py

from django.urls import path
from subscribeapp.views import SubscriptionView, SubscriptionListView
app_name = 'subscribeapp'

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('list/', SubscriptionListView.as_view(), name='list'),
]
```
위는 models.py와 urls.py입니다.

html파일은 추후 업로드 하겠습니다.

내일은 flask로 제작한 챗봇 api를 django로 이식할 예정입니다.

오늘은 이만 안녕

