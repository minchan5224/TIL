# [Django View](http://pythonstudy.xyz/python/article/306-Django-%EB%B7%B0-View)
##### Date 2020_11_13 Django View / Django Template
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
> 
>
### 2. Django App생성
> Django App을 생성하기 위해서는 "**manage.py startapp App명**" 를 실행하면 된다.
> 아래 예제는 아래는 **home** 이라는 **App명**을 사용하여 새로운 **Django App을 생성**하는 명령이다.
>> ```
>> (venv1) ~/pysrc/myweb $ ./manage.py startapp home
>> ```
> 위의 명령을 실행하면 home라는 서브폴더가 생성되고 내부에 Django App에 필요한 기본 파일이 생성된다.
> ![django-create-app](./image/Django_01_3.png)
>
### 3. Django App 사용
> 간단한 웹페이지를 만들어 보기 위해 home/views.py 파일에 다음과 같은 index 함수를 추가한다.
>> ```Python
>> from django.shortcuts import render
>> from django.http import HttpResponse
>> 
>> # Create your views here.
>> def index(request):
>>     return HttpResponse("Hello, World!")
>> ```
>
> 웹 브라우저에서 ```http://127.0.0.1:8000``` 를 실행하면 위의 index 함수를 호출하게 만들기 위해 웹 프로젝트의 (myweb 폴더 안의) settings.py와 urls.py에 아래와 같은 두 가지 셋팅을 추가해 주어야 한다.
> 01. settings.py : INSTALLED_APPS 리스트에 Django App명 (home) 추가
>
> ![settings-for-app](./image/Django_01_4.png)
>
> 02. urls.py : urlpatterns 리스트에 사용할 URL 패턴 추가. url()의 첫번째 파라미터는 [정규표현식(Regular Expression 혹은 RegEx)](http://pythonstudy.xyz/python/article/401)으로 ^$ 은 빈 문자열 즉 루트를 가리킨다.
>
> ![urls-for-app](./image/Django_01_5.png)
>
>위의 셋팅들을 변경하고 웹 서버를 시작하여 접속하면 Hello World 가 정상적으로 표시될 것이다.
>
### 4. PyCharm에서 가상환경 사용하기
> PyCharm에서 위의 Django 프로젝트를 오픈했을 때, 처음에는 django 패키지들을 인식하지 못할 수 있다.
> PyCharm 프로젝트가 가상환경을 사용하고 있지 않기 때문인데, 셋팅을 변경하면 정상적으로 인식한다.
>> #### Mac OS X
>> PyCharm에서 해당 Django 프로젝트를 오픈하고, PyCharm 메뉴 - Preferences 를 선택
>>
>> Project - Project Interpreter에서 콤보 박스 안에서 가상환경 venv1 을 찾아 선택하고 OK를 누른다.
>>
>> 만약 해당 가상환경이 보이지 않으면, 콤보 박스 뒤의 설정 아이콘을 누르고 Add Local을 선택하여 추가
>
> ![pycharm-venv-setting-mac](./image/Django_01_6.png)
>
>> #### Windows
>> PyCharm에서 해당 Django 프로젝트를 오픈하고, File - Settings 메뉴를 선택
>>
>> Project - Project Interpreter에서 콤보 박스 뒤의 설정 아이콘을 누르고 Add Local을 선택
>>
>> 가상환경 venv1 디렉토리 밑의 scripts/python.exe 을 찾아 선택하고 OK를 누른다.
>
> ![pycharm-venv-setting-win](./image/Django_01_7.png)
>
>
> # 끝!

