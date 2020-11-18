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
>>


>
### 2. URL 패턴
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
