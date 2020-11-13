# [Django View](http://pythonstudy.xyz/python/article/306-Django-%EB%B7%B0-View)
##### Date 2020_11_13
---
 ### 1. Django View
> Django에서의 View는 다은 일반 MVC Framework에서 말하는 컨트롤러(Controller)와 비슷한 역활을 한다.
> - View는 필요한 데이터를 모델(혹은 외부)에서 가져와 적절히 가공하여 웹 페이지 결과를 만들도록 컨트롤 하는 역할을 함.
>
> View 들은 Django App안의 Views.py라는 파일에 정의한다.
> - 각 함수가 하나의 View를 정의한다.
> - 각 View는 HTTP Request를 입력 파라미터로 받아들이고 HTTP Response를 반환한다.
>
> ```Python
> from django.http import HttpResponse
> 
> def index(request):
>    return HttpResponse("<h1>Hello, World!</h1>")
> ```
>
> 위 예제는 하나의 View함수를 표한 것
>> 이 함수는 입력으로 항상 request 를 받아들이고, response 를 리턴한다.
>>
>> View는 '**웹페이지 내용을 갖는 HttpResponse 객체**'를 리턴하거나 '**Http404 같은 Exception**'을 리턴한다.
>>
>> 일반적으로 Django에서는 좀더 복잡한 HTML을 처리하기 위해 뷰 템플릿을 사용하며 여기서는 간단한 HTML Text를 포함한 HttpResponse()객체를 반환한다.
>
> ```Python
> from django.http import Http404, HttpResponseNotFound
>
> def error(request):
>     #return HttpResponseNotFound('<h1>not found</h1>')
>     raise Http404("Not Found")
> ```
>
> 위의 예제는 Http404 Exception을 일으키는 것이다.
>
> return이 아닌 raise를 사용하였으며 ```Http404```대신 ```HttpResponseNotFound```또한 사용 가능하다.
>
### 2. MTV 
> Django는 Model, Template, View라는 MTV 패턴을 따른다.
> - MTV에서의 Model은 데이타를 표현하는데 사용되며, 하나의 모델 클래스는 DB에서 하나의 테이블로 표현된다. 
> 
> - MTV의 View는 HTTP Request를 받아 그 결과인 HTTP Response를 리턴하는 컴포넌트로서, Model로부터 데이타를 읽거나 저장할 수 있으며,
> Template을 호출하여 데이타를 UI 상에 표현하도록 할 수 있다.
>
> - MTV의 Template은 Presentation Logic 만을 갖는데 HTML을 생성하는 것을 목적으로 하는 컴포넌트이다.
>
> MTV는 MVC와 유사한 점이 많다.
>
> - Django는 Controller의 역할을 Django Framework자체에서 한다고 본다.(MVC와 조금 다른 차이를 MTV로 설명한다.
>
---
# [Django Template](http://pythonstudy.xyz/python/article/307-Django-%ED%85%9C%ED%94%8C%EB%A6%BF-Template)
---
### 1. Django Template
> Django에서의 Template은 MVC에서의 View와 비슷한 역할을 한다.
> - Template은 View로부터 전달된 데이터를 템플릿에 적용하여 동적인 웹페이지를 만드는데 사용된다.
>
> Template은 HTML 파일로서 Django App 폴더 밑에 "templates" 라는 서브폴더를 만들고 그 안에 템플릿 파일(\*.html)을 생성한다.
>> 단일 App이거나 동일 템플릿명이 없는 경우 사용할 수 있다.
>>
>> Django 개발 가이드라인은 "App폴더/templates/App명/템플릿파일" 처럼, 각 App 폴더 밑에 templates 서브폴더를 만들고 다시 그 안에 App명을 사용하여 서브폴더를 만든 후 템플릿 파일을 그 안에 넣기를 권장한다.
>>
>> ex:```/home/templates/home/index.html``` 
>>
>> 만약의 경우 여러 App들이 동일한 이름의 Template을 가진 경우, View에서 잘못된 Template을 가져올 수 있기 때문에 위 방법을 권장한다.
>
> Template은 HTML로만 작성된 정적인 HTML파일인 경우도 있지만 대부분의 경우 View로 부터 데이터를 전달받아 HTMLTemplate안에 동적으로 치환하여 사용한다.
> 
> index 뷰에서 message 라는 데이터를 index.html 이라는 Template에 전달하고 그 Template 안에서 이를 사용하기 위해서 아래와 같이 사용 할 수 있다.
>
> ```Python
> from django.shortcuts import render
> 
> def index(request):
>   msg = 'My Message'
>     return render(request, 'index.html', {'message': msg})
> ```
>
> 1. View(home/views.py)에서 index()를 정의한다.
>> render는 django.shortcuts 패키지에 있는 함수이며 첫번째 파라미터로 request를, 그리고 두번째 파라미터로 Template을 받아들인다.
>>
>> Template은 index.html으로 지정되어 있으며 이는 home/templates/index.html을 가리킨다.
>>
>> 세번째 파라미터는 Optional이며 View에서 Template에 전달한 데이타를 Dictionary로 전달한다. (Dictionary=>{ key : Data }
>>
>> Dictionary의 Key는 템플릿에서 사용할 키(혹은 변수명)이며 Value는 전달하는 데이터의 내용을 담는다. 여기서는 키 : message , 데이터 : "my Message"
>>
>> 만약 Template파일을 home/templates/home/index.html 에 저장했다면, 두번째 파라미터의 내용을 '**home/index.html**'로 변경한다.
>
> ```HTML
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <title>Title</title>
> </head>
> <body>
>     <h1>{{message}}</h1>
> </body>
> </html>
> ```
>
> 2. Template (home/templates/index.html)에 HTML 문서를 작성한다.
>> body 태그 안에 message를 보면 {{변수명}} 으로 둘러싸인 것은 해당 변수의 값을 그 자리에 치환하라는 의미이다.
>>
>> Django Template은 또한 View로 부터 전달된 다양한 데이터들을 Template에 편리하게 넣을 수 있도록 여러 Template 태그( {% Template태그 %} 와 같은 형태)들을 제공한다.
>
### 2. Template 셋팅
> Django에서는 여러 Template 엔진을 선택하여 사용할 수 있다.
>
> 셋팅은 Django 프로젝트의 settings.py 에서 할 수 있다.
> - 기본 Django Template 엔진을 사용하기 위해서는 settings.py 파일의 TEMPLATES 섹션에서 BACKEND를 django.template.backends.django.DjangoTemplates 로 설정한다.(기본 설정 되어있다.)
>
### 3. Django Template 언어
> Django Template에서 사용하는 특별한 태크 및 문법을 Django Template 언어 (Django Template Language)라 부른다.
>
> Template 언어는 크게 [Template 변수](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_02.md#template-%EB%B3%80%EC%88%98), [Template 태그](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_02.md#template-%ED%83%9C%EA%B7%B8), [Template 필터](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_02.md#template-%ED%95%84%ED%84%B0), [코멘트](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_02.md#%EC%BD%94%EB%A9%98%ED%8A%B8) 등으로 나눌 수 있다.
>
> ##### Template 변수
> Template 변수는 {{''}} 으로 둘러 싸여 있는 변수로서 그 변수의 값이 해당 위치에 치환된다.
> 변수에는 Primitive 데이타를 갖는 변수 혹은 객체의 속성 등을 넣을 수 있다.
> ```HTML
> <h4>
>   Name : {{ name }}
>   Type : {{ vip.key }}
> </h4>
> ```
>
> ##### Template 태그
> 템플릿 태크는 {% 와 %} 으로 둘러 싸여 있다. 이 태그 안에는 if, for 루프 같은 Flow Control 문장에서부터 웹 컨트롤 처럼 내부 처리 결과를 직접 덤프하는 등등 여러 용도로 쓰일 수 있다.
> 아래 처음 부분은 if 와 for 태크를 사용한 예이고, 마지막은 CSRF 해킹 공격에 대응하여 토큰을 넣어주는 csrf_token 태그를 사용한 예이다.
> ```HTML
> {% if count > 0 %}
>     Data Count = {{ count }}
> {% else %}
>     No Data
> {% endif %}
> 
> {% for item in dataList %}
>   <li>{{ item.name }}</li>
> {% endfor %}
> 
> {% csrf_token %}
> ```
> [태그에 대한 자세한 설명](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#ref-templates-builtins-tags)
>
> ##### Template 필터
> Template 필터는 변수의 값을 특정한 포맷으로 변형하는 기능을 한다.
> ```HTML
> #날짜 포맷 지정
> {{ createDate|date:"Y-m-d" }}
> 
> #소문자로 변경
> {{ lastName|lower }}
> ```
>
> ##### 코멘트
> 코멘트를 넣는 방법
> -  한 라인에 코멘트를 적용할 땐 코멘트를 {# 과 #} 으로 둘러싼다.
> ```{# 1 라인 코멘트 #}```
> - 복수 라인 문장을 코멘트할 경우는 문장들을 {% comment %} 태그와 {% endcomment %}로 둘러싼다.
> ```
> {% comment %}  
>   <div>
>       <p>
>           불필요한 블럭
>       </p>
>       <span></span>
>   </div>
> {% endcomment %}
> ```
>
> ##### HTML Escape
> TML 내용 중에 <, >, ', ", & 등과 같은 문자들이 있을 경우 이를 그 문자에 대응하는 HTML Entity로 변환해야 한다.
>
> Django Template에서 이러한 작업을 자동으로 처리하기위해 {% autoescape on %} 템플릿 태그나 escape 라는 필터를 사용한다.
> ```
> {% autoescape on %}     # autoescape 태그
>     {{ content }}
> {% endautoescape %}
>  
> {{ content|escape }}    # escape 필터
> ```
> content라는 변수에 인용부호가 들어 있을때 위 예제와 같이 autoescape 태그나 escape 필터를 이용하 자동으로 변환하게 할 수 있다.
>
> 이러한 변환을 거치지 않는다면 HTML이 중간에 깨지게 된다.
>
> 변환을 거치치 않고 사용하기 위해서는 각 문자를 미리 HTML Entity로 변환해야한다.
>
> # 끝!
> > # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
