# [URL 매핑](http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API)
##### Date 2020_11_17
---
### 1. Django App URL 매핑
> 하나의 프로젝트 내에 여러 Django App이 있다면
> - ~~프로젝트 폴더 내의 urls.py 파일 하나로 모든 URL매핑한다.~~ **(X)**
>
> 각각의 Django App안에 urls.py 파일을 만들고 메인 urls.py 파일에서 각각의 Django App의 urls.py 파일로 URL 매핑을 위탁하게 할 수 있다.
>
> - 다수의 App들을 포함하는 큰 프로젝트의 경우 편리하다.
>
> 메인 URL 파일 (myweb/urls.py)에서 2개의 Django App URL 파일을 include 하여 사용하는 예
>>
>> ![url-mapping](./image/Django06/Django_06_1.png)
>>
>> "feedback/" 으로 시작되는 URL들을 feedback.urls 즉 feedback App 안의 urls.py 에 있는 매핑을 사용
>>
>> "home/" 로 시작되는 URL들을 home.urls 즉 home 폴더 안의 urls.py 에 있는 매핑을 사용
>
> 각 Django App에 있는 urls.py는 메인과 동일한 방식으로 매핑을 정의함
> - 웹 루트(/)가 아닌 현재 App의 상대적 위치를 기준으로 URL경로를 지정
>
> 아래 코드는 각각 home/urls.py와 feedback/urls.py 의 내용이다.
>> ```Python
>> # home/urls.py
>> from django.conf.urls import url
>> from home import views
>> 
>> urlpatterns = [
>>     url(r'^contact', views.contact),
>>     url(r'^about', views.about),
>> ]
>> ```
>> home/urls.py 의 contact 패턴은 실제 메인에서의 home 패턴과 결합하여 "/home/contact" 를 가리킨다.
>> - /home/contact URL은 home.views.contact 함수를 호출하는 것
>>
>> ```Python
>> # feedback/urls.py
>> from django.conf.urls import url
>> from feedback import views
>> 
>> urlpatterns = [
>>     url(r'^list', views.list),
>>     url(r'^add', views.add),
>>     url(r'^update', views.update),
>> ]
>> ```
>> feedback 역시 "/feedback/list" 는 feedback.views.list 함수와 매핑되어 있음을 알 수 있다.
>
### 2. URL 패턴
> Django 2.0 이상 버전에서는 일반적인 URL 패턴 지정을 위해 django.urls.path() 함수를 사용하되, path()에서 지정하지 못하는 복잡한 패턴의 경우 정규표현식을 사용하는 django.urls.re_path() 함수를 사용한다.
> 
> **path() 함수**
> django.urls.path() 함수는 Django 2.0 에서부터 지원된다.
> - path(route, view, kwargs=None, name=None) 와 같이 4개의 파라미터를 받아들일 수 있다.
>
> - 처음 2개의 파라미터는 필수적이며 뒤의 2개는 옵션이다.
>
> - 첫번째 파라미터에는 URL route에서 사용된 경로를 지정, 두번째 파라미터는 해당 URL에 상응하는 View를 지정한다.
>
> - 두번째 파라미터에서 View를 지정하는 방식으로는 function view의 이름을 지정하거나 클래스에 기반한 View (class based view)의 경우 "클래스명.as_view()"와 같이 지정한다.
>
> - 세번째 파라미터에는 Dictionary 형식의 아큐먼트를 옵션으로 지정, 네번째 파라미터에는 path 이름을 지정(path명으로부터 URL 패턴 정보를 찾는 URL Reversing 을 위해 사용
>
>> ```Python
>> from django.urls import path 
>> from home import views
>>  
>> urlpatterns = [
>>     path('', views.index),
>>     path('ads.txt', views.ads),
>> ]
>> ```
>> 첫번째 path() 함수는 공백 즉 디폴트 웹페이지 URL인 경우 home/views.py 에 있는 index() 함수를 호출하도록 표현한 것
>>
>> 두번째 path() 함수는 웹 클라이언트가 "/ads.txt"를 요구했을 때, home/views.py 에 있는 ads() 함수를 호출할 것을 지정한 것
>
> path() 함수의 첫번째 파라미터인 URL 패턴은 완전한 경로를 표시
> - **Ex** : 글로벌 URLconf 파일 (ex: /myweb/urls.py) 에 'accout/login'으로 경로를 지정하면, 이는 '/accout/login/' 경로를 의미
>
> ```/myweb/urls.py from django.urls import path, include import home.views urlpatterns = [ path('accout/login', home.views.login, name='login') ]``` 에서 name='login'은 해당 path() 함수의 경로 데이타에 대한 정보를 나중에 사용하기 위해 임의의 path명을 명명한 것이다.
>
> URL 파라미터로부터 특정 정보를 읽어내는 방법
>> ```Python
>> # myweb/urls.py
>> from django.urls import path
>> import feedback.views
>>  
>> urlpatterns = [
>>     path('feedback/<int:id>/', feedback.views.display)
>> ]
>> </int:id>
>> ```
>> 피드백 Id가 URL 상에 있다고 했을 때, 이 Id를 알아내기 위해 URL 패턴을 "feedback/<id>" 혹은 Id가 숫자인 경우 명시적으로 "feedback/<int:id>"와 같이 지정할 수 있다.
>> - "id" 는 feedback.views.display(request, id) 함수(feedback/views.py)에 전달되는 파라미터명
>
> ```Pytohon
> # feedback/views.py 
> def display(request, id):
>     s = "ID = " + str(id)
>     return HttpResponse(s)
> ```
> <int:id> 표현은 URL에서 파라미터를 캡쳐(Capture)하는 표현으로 콜론(:) 뒤에 있는 id는 View에 전달되는 파라미터명, 콜론 앞에 있는 것(int)은 Path Converter라고 부르는 것이며 View에 값을 전달하기 전에 콜론 앞의 타입으로 적절하게 변환한 후 파라미터로 전달한다.
>
>
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
