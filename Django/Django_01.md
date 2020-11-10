# Django 훑어보기
##### Date 2020_11_10
---
> ### 모델 설계
>> + Django를 데이터베이스 없이 사용할 수 있더라도 데이터베이스 레이아웃을 파이썬 코드로 표현할 수 있는 [object-relational mapper](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)를 지원한다.
>>
>> + [data-model syntax](https://docs.djangoproject.com/ko/3.1/topics/db/models/)은 모델을 표현할 여러 방법을 제공해준다.
>
> 아래는 간단한 예시!
> ##### mysite / news / models.py 
> ```Python
> 
> from django.db import models
> class Reporter(models.Model):
>     full_name = models.CharField(max_length=70)
> 
>     def __str__(self):
>         return self.full_name
> 
> class Article(models.Model):
>     pub_date = models.DateField()
>     headline = models.CharField(max_length=200)
>     content = models.TextField()
>     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
> 
>     def __str__(self):
>         return self.headline
> ```
>
> ### 설치하기
> 데이터베이스를 자동 생성해주는 Django-command-line을 실행한다.
> ```
> $ python manage.py makemigrations
> $ python manage.py migrate
> ```
>> - [makemigrations](https://docs.djangoproject.com/ko/3.1/ref/django-admin/#django-admin-makemigrations) 명령은 생성 가능한 모델을 찾아 테이블이 존재하지 않을 경우 마이그레이션을 생성합니다.
>> - [migrate](https://docs.djangoproject.com/ko/3.1/ref/django-admin/#django-admin-migrate) 명령은 마이그레이션을 실행하고 사용자의 데이터베이스에 테이블을 생성합니다. 이는 더욱 풍부한 스키마 제어를 선택적으로 제공합니다.
>>
> [마이그레이션 이란?](https://docs.djangoproject.com/ko/3.1/topics/migrations/)
>
> ### API도 많이 제공한다구
>> - API는 즉시 생성되며 코드 생성이 불필요하다.([Python API](https://docs.djangoproject.com/ko/3.1/topics/db/queries/))
>
> [구경가쉴?](https://docs.djangoproject.com/ko/3.1/intro/overview/#enjoy-the-free-api)
>
> ### 동적인 관리자 인터페이스
> 👨‍🍳 : ~~"완성된 집입니다. **근데 이제 단순한 뼈대 세우기를 곁들인게 아닌.**"~~
>> 모델이 정의되면 Django는 인등 된 사용자가 개체를 추가, 변경 및 삭제할 수 있는 전문적인 관리 인터페이스를 자동으로 만들 수 있다!
>>
>> 사용하려면 관리 사이트에 모델을 등록해야한다!~~**명심하라구 하핫**~~
>>
> 예시.. 예시를 보자!🙊
> #### mysite / news / models.py
> ```Python
> from django.db import models
>
> class Article(models.Model):
>     pub_date = models.DateField()
>     headline = models.CharField(max_length=200)
>     content = models.TextField()
>     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
> ```
>
> #### mysite / news / admin.py
> ```Python
> from django.contrib import admin
>
> from . import models
>
> admin.site.register(models.Article)
> ```
>
> Django 앱을 생성하는 하나의 전형적인 작업 흐름은 일단 모델을 만들고 관리자 사이트를 올려서 최대한 빠르게 작동 가능하도록 만드는 것!
>
> 운영자가 데이터 입력을 시작할 수 있게 밖으로 데이터를 표현하는 방법을 개발해야한다.
>
> ### URL 설계
> Django는 깔끔한(아름다운?) URL 설계를 장려하며 URL에 .php 혹은 .asp 같은 불필요한 내용들을 넣지 않습니다!
>
> 앱의 URL을 디자인하려면 URLconf 라는 Python 모듈을 만들어야 합니다.
> - 앱의 목차로 URL 패턴과 Python 콜백 함수 간의 매핑이 포함되어 있다.
> - URLconf는 또한 Python 코드에서 URL을 분리하는 역할을 한다.
>
> #### mysite/news/urls.py
> ```Python
> from django.urls import path
>
> from . import views
>
> urlpatterns = [
>     path('articles/<int:year>/', views.year_archive),
>     path('articles/<int:year>/<int:month>/', views.month_archive),
>     path('articles/<int:year>/<int:month>/<int:pk>/', views.article_detail),
> ]
> ```
> 위 코드는 URL 경로들을 파이썬 콜백 함수들("views")로 연결해 줍니다. 경로를 나타내는 문자열들은 매개 변수 태그들을 사용하여 URL 로부터 값을 "캡처"합니다. 사용자가 페이지를 요청하면, Django 는 각 경로를 순서대로 실행하고, 요청된 URL 과 일치하는 첫번째 것에서 정지하게 됩니다. (만약 아무것도 일치하는 것이 없다면, Django 는 특수한 사례인 404 view 를 호출합니다.) 이 경로들은 로드할 때 정규표현식으로 컴파일 되어 있기 때문에 엄청나게 빠릅니다.👍
> 
> URL 패턴 중 하나가 일치하면 Django는 주어진 뷰를 호출합니다. 뷰는 파이썬 함수로, 각각의 뷰에는 요청 메타데이터가~~(파라미터?, 변수?)~~ 포함된 요청 개체와 패턴에 잡힌 값이 전달 됩니다.
>
> #### Ex
>> 사용자가 URL "/articles/2005/05/39323/"로 요청을 보냄
>>
>>  Django 호출 : news.views.article_detail(request, year=2005, month=5, pk=39323).
>
> ### 뷰 작성하기
> 각각의 뷰는 다음 두가지중 하나를 수행해야할 책임이 있다.
>> 요청된 페이지의 내용을 담고 있는 [HttpResponse](https://docs.djangoproject.com/ko/3.1/ref/request-response/#django.http.HttpResponse) 객체를 반환한다.
>>
>> [Http404](https://docs.djangoproject.com/ko/3.1/topics/http/views/#django.http.Http404) 같은 예외를 발생시킨다.
>
> 일반적으로 뷰는 파라미터들에 따라 데이터를 가져오며 템플릿을 로드하고 템플릿을 가져온 데이터로 렌더링 한다.
> 아래 예시는 위에서 만든 year_archive에 대한 예시 뷰이다.
>
> #### mysite/news/views.py
> ```Python
> from django.shortcuts import render
>
> from .models import Article
>
> def year_archive(request, year):
>     a_list = Article.objects.filter(pub_date__year=year)
>     context = {'year': year, 'article_list': a_list}
>     return render(request, 'news/year_archive.html', context)
> ```
> 해당 예제는 Django의 [템플릿 시스템](https://docs.djangoproject.com/ko/3.1/topics/templates/)을 사용한다!
>
> Django의 템플릿 시스템은 몇몇 강력한 기능을 가지면서 프로그래머가 아닌 사람도 사용하기 어렵지 않도록 간결함을 유지하도록 노력 하였다!
>
> ### 자신만의 템플릿 작성
> Django 템플릿들중 중복을 최소화할 수 있게 하는 템플릿 검색 경로를 가지고 있다.
>
> DIRS 템플릿을 확인하기 위한 디렉토리의 목록을 명시합니다. 만약 첫번째 디렉토리에 템플릿이 존재하지 않으면, 두번째 디렉토리, 그 외 디렉토리를 점검합니다.
>
> news/year_archive.html 템플릿이 있다고 하자!
> #### mysite/news/templates/news/year_archive.html
>```html
> {% extends "base.html" %}
>
> {% block title %}Articles for {{ year }}{% endblock %}
>
> {% block content %}
> <h1>Articles for {{ year }}</h1>
>
> {% for article in article_list %}
>     <p>{{ article.headline }}</p>
>     <p>By {{ article.reporter.full_name }}</p>
>     <p>Published {{ article.pub_date|date:"F j, Y" }}</p>
> {% endfor %}
> {% endblock %}
>```
>
> 변수는 이중 중괄호로 포장한다. {{ article.headline }} 의 뜻 : **“article의 headline 속성의 값을 출력하겠다.”**
> - 마침표는 속성의 조회에만 사용하는 것이 아닌 딕셔너리의 키 조회, 인덱스 조회, 함수 호출에도 사용할 수 있다.
>
> {{ article.pub_date|date:"F j, Y" }}는 유닉스 스타일의 “파이프”(“|” 문자)를 사용한것
> - 파이프는 템플릿 필터를 호출하며 이를 통해 변수의 값을 필터링 할 수 있다.
>
> 사용자는 좋아하는 여러 필터를 함께 연결할 수 있다.
> - 사용자는 [커스텀 템플릿 필터](https://docs.djangoproject.com/ko/3.1/howto/custom-template-tags/#howto-writing-custom-template-filters)를 작성 할 수 있다.
>
> - 사용자는 [커스텀 파이썬 코드](https://docs.djangoproject.com/ko/3.1/howto/custom-template-tags/)인 커스텀 템플릿 태그를 작성할 수도 있다.
>
> Django의 “템플릿 상속” 개념을 사용해 보자!
>> {% extends "base.html" %} 코드가 무슨 일을 하는지 알 수 있다.
>> - "**한 뭉치의 block들이 정의된 ‘base’라는 템플릿을 먼저 로드하고 뒤따르는 block들로 이 block들을 채운다**"
>>
>> - 템플릿 안의 중복을 낮추게 한다 => 각각의 템플릿은 자신이 표현 하려는 내용들만 정의할 수 있게 되기 때문에.
>
> “base.html” 템플릿은 [정적 파일(static files)](https://docs.djangoproject.com/ko/3.1/howto/static-files/)의 사용을 포함하여, 아래의 예시와 같이 보일 것이다!
>
> #### mysite/templates/base.html
> ```html
>{% load static %}
><html>
><head>
>    <title>{% block title %}{% endblock %}</title>
></head>
><body>
>    <img src="{% static 'images/sitelogo.png' %}" alt="Logo">
>    {% block content %}{% endblock %}
></body>
></html>
> ```
