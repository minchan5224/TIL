# Django 실습
##### Date 2020_12_8
---
1. 모바일 디버깅, 반응형 레이아웃 
###### [39강](https://www.youtube.com/watch?v=qvLYJBzcD_I&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=40)
> 모바일에서 보기 좋은 사이즈로 제공하기 위해 아래의 코드를 head.html에 추가한다.
> ```<meta charset="UTF-8">```의 아래에
> ```
> <meta name="viewport" contnet="width=device-width, initial-scale=1, shrink-to-fit=no">
> ```
> 를 작성한다.
> 
> articleapp의 list.html의 <style>부분에 
> ```
>     .container {
>         padding: 0;
>         margin: 0, auto;
>     }
>     
>     .container a {
>         width: 45%;
>         max-width: 250px;
>     }
> ```
> 
> 위와 같이 2개의 컨테이너를 더 설정 하였으며
> 
> magicgrid.js의 ```let magicGrid = new MagicGrid```에서
> 
> ```gutter: 30,```을 ```gutter: 12,```로 수정 하였다.
> 
> 마지막으로 base.css에 아래의 내용을 추가 하였다.
> ```
> @media screen and (max-width:500px) {
>     html {
>         font-size: 13px;
>     }
> }
> ```
2. ProjectApp (게시판) 구현[40강](https://www.youtube.com/watch?v=ISwzXvwvBxQ&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=41)
> ```python manage.py startapp projectapp```명령어를 통해 projectapp생성
> 
> settings.py에 projectapp등록
> 
> urls.py 에 경로 설정
> 
> models.py 작성
> ```Python
> from django.db import models
> 
> class Project(models.Model):
>     image = models.ImageField(upload_to='project/', null=False)
>     title = models.CharField(max_length=20, null=False)
>     description = models.CharField(max_length=600, null=False)
>     created_at = models.DateTimeField(auto_now=True)
> ```
> 
> forms.py 작성
> ```Python
> from django.forms import ModelForm
> from projectapp.models import Project
> 
> class ProjectCreationForm(ModelForm):
>     class Meta:
>         model = Project
>         fields = ['image', 'title', 'description']
> ```
> 
> 마이그레이션 작업.
> 
> ```python manage.py makemigrations```
> 
> ```python manage.py migrate```
> 
> views.py 작성
> ```Python
> from django.shortcuts import render
> from django.views.generic import CreateView, DetailView, ListView
> 
> from projectapp.forms import ProjectCreationForm
> from projectapp.models import Project
> 
> from django.urls import reverse
> from django.utils.decorators import method_decorator
> from django.contrib.auth.decorators import login_required
> 
> @method_decorator(login_required,'get')
> @method_decorator(login_required,'post')
> class ProjectCreateView:
>     model = Project
>     form_class = ProjectCreationForm
>     template_name = 'projectapp/create.html'
> 
>     def get_success_url(self):
>         return reverse('projectapp:detail', kwargs={'pk': self.object.pk})
> 
> class ProjectDetailView:
>     model = Project
>     context_object_name = 'target_project'
>     template_name = 'projectapp/detail.html'
> 
> class ProjectListView:
>     model = Project
>     context_object_name = 'project_list'
>     template_name = 'projectapp/list.html'
>     pagiante_by = 25
> ```
> create.html 작성
> ```html
> {% extends 'base.html' %}
> {% load bootstrap4 %}
> 
> {% block content %}
> 
>     <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>         <div class="mb-4">
>             <h4>게시물 작성</h4>
>         </div>
>         <form action="{% url 'projectapp:create' %}" method="post" enctype="multipart/form-data">
>             {% csrf_token %}
>             {% bootstrap_form form %}
>               <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
>         </form>
>     </div>
> 
> {% endblock %}
> ```
> detail.html 작성
> ```html
> {% extends 'base.html' %}
> {% load bootstrap4 %}
> 
> {% block content %}
> 
>     <div>
>         <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>             
>             <img src="{{ target_project.image.url }}" alt="" style="height: 12rem; width: 12rem; border-radius: 20rem; margin-bottom: 2rem; object-fit: cover;">
>             <h2>
>                 {{ target_project.title }}
>             </h2>
>             <h5>
>                 {{ target_project.desxription }}
>             </h5>
>         </div>
>     </div>
> 
> {% endblock %}
> ```
> list.html 작성
> ```
> {% extends 'base.html' %}
> {% load static %}
> {% load bootstrap4 %}
> 
> {% block content %}
> <style>
>     .container {
>         padding: 0;
>         margin: 0, auto;
>     }
> 
>     .container div {
>         display: flex;
>         justify-content: center;
>         align-items: center;
>         border-radius: 1rem;
>     }
>     
>     .container img {
>         width: 7rem;
>         height: 7rem;
>         object-fit: cover;
>         border-radius: 1rem;
>     }
> 
> </style>
>     {% if project_list %}
>     <div class="container">
>         {% for project in project_list %}
>         <a href="{% url 'projectapp:detail' pk=project.pk %}">
>             {% include 'snippets/card_project.html' with project=project %}
>         </a>
>         {% endfor %}
>     </div>
>     <script src="{% static 'js/magicgrid.js' %}"></script>
>     {% else %}
>     <div class="text-center">
>         <h1>
>             😢 게시물이 없습니다! 😢
>         </h1>
>     </div>
>     {% endif %}
> 
>     {% include 'snippets/pagination.html' with page_obj=page_obj %}
>     <!-- 페이지 버튼 만들어 주는것 연결 -->
> 
>     <div style="text-align: center">
>         <a href="{% url 'projectapp:create'%}" class="btn btn-dark rounded-pill col-3 mt-3 mb-3">
>             게시글 작성
>         </a>
>     </div>
>     
> {% endblock %}
> ```
> 
> 기본 적인 틀은 article의 list.html과 비슷하다. 
> 
> 다음은 project에서 사용할 card를 수정한다
> 
> 이름은 card_project.html이다.
> ```
> <div style="display: block; text-align: center">
>     <img src="{{ project.image.url }}" alt="">
>     <h5 class="mt-2">
>         {{ project.title | truncatechars:8 }}
>     </h5>
> </div>
> ```
> 
> 그후 base.css에 아래의 코드를 추가한다.
> ```
> a {
>     color: black;
> }
> 
> a:hover {
>     color: black;
>     text-decoration: none;
> }
> 
> .BS_header_nav {
>     margin: 0 0.5rem;
> }
> 
> .BS_header_navbar {
>     margin: 1rem 0;
> }
> ```
> 
> 마지막으론 header.html을 수정한다.
> ```Python
>      <div class="BS_header">
>         <div>
>             <h1 class="BS_logo">
>                 Backend Study
>             </h1>
>         </div>
>         <div class="BS_header_navbar">
>             <a href="{% url 'articleapp:list' %}" class="BS_header_nav">
>                 <span>Article</span>
>             </a> | 
>             <a href="{% url 'projectapp:list' %}" class="BS_header_nav">
>                 <span>Project</span>
>             </a> | 
>             {% if not user.is_authenticated %}<!--이 유저가 로그인이 되어있지 않다면. Login을 보여준다.-->
>             <a href="{% url 'accountapp:login' %}?next={{ request.path }}" class="BS_header_nav">
>                 <span>Login</span>
>             </a> | 
>             <a href="{% url 'accountapp:create' %}" class="BS_header_nav">
>                 <span>SignUp</span>
>             </a>
>             {% else %}
>             <a href="{% url 'accountapp:detail' pk=user.pk %}" class="BS_header_nav">
>                 <!--urls.py에서 detail/<int:pk> 하였기 때문에 pk=user.pk를 통해 pk를 넘겨준다.-->
>                 <span>MyPage</span>
>             </a> | 
>             <a href="{% url 'accountapp:logout' %}?next={{ request.path }}" class="BS_header_nav"><!--그대로-->
>                 <span>Logout</span>
>             </a>
>             {% endif %}
>         </div>
>     </div>
>     <hr>
> ```
> 오늘은 여기까지 
> 
> 집 컴퓨터가 벌써 8년째 생존해 있다 이제 갈때가 된것같다 그래서 폐업하는 PC방에 컴퓨터를 사러 간다.
> 
> 조심히 다녀오겠습니다.
> 
# 끝!
오늘은 [40강](https://www.youtube.com/watch?v=ISwzXvwvBxQ&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=41)의 학습을 진행 하였다.
## 참고한 영상 : [실용주의 프로그래머의 작정하고 장고! Django로 Pinterest 따라하기](https://www.youtube.com/playlist?list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo)
