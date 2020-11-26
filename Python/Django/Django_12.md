# Django 실습
##### Date 2020_11_24
---
### 1. Model, DB 연동 - makemigrations, migrate
> 1. makemigrations
>> 
>> accountapp의 탬플릿인 hello_world.html은 현재 정적이다. 이를 DB와 연동하여 동적으로 바꿔주기 위해 실습을 진행한다.
>> 
>> - models.py에 쓰는 내용을 DB와 연동시킬 python파일로 만들어 주는 작업을 하는 것.
>> 
>> accountapp의 models.py내용 작성
>> ```Python
>> from django.db import models
>> 
>> # Create your models here.
>> 
>> #class 하나가 DB에서 아이템 하나가 된다.
>> 
>> class HelloWorld(models.Model):#models.Model을 상속받아 사용
>>     #원초적인 모델을 가져와서 수정하여 새로운 클래스로 생성하는 작업.
>>     text = models.CharField(max_length=255, null=False) #CharField:문자열들을 포함하는 필드.
>>     #null 이 텍스트/ 에트리뷰트가 없어도 되는지 설정을 해주는것. 있어야 하니까 False로 한것.
>> ```
>> 그 후 터미널에서 ```python manage.py makemigrations``` 명령어 사용
>> ![makemigrations](./image/Django12/Django_11_1.PNG)
>
> 2. [migrate](https://www.youtube.com/watch?v=fz6hYVOer2Y&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=14&t=323)
>> 
>> 지금은 연동이 된 상태가 아니기 때문에 다시 연동시켜주는 명령어를 사용해야한다.
>> 
>> ```python manage.py migrate``` 명령어를 통해 연동 시켜준다.(사진 : migrate)
>> 
>> 많은 내용이 나옴 -> 처음 연동한 것이기 때문에 장고에서 기본으로 제공해주는 DB들 또한 함께 연동됨.
>>
>> ![migrate](./image/Django12/Django_11_2.PNG)
>> 
>> 엑셀로 비교하자면 새로운 시트를 생성하여 안의 내용을 채워주는 기본작업을 하는 것이라 생각하면 된다.
>> 
>> main인 경로 즉 나의 경우는 backend_study에서 settings.py파일로 들어가면 DB에 대한 정보를 볼 수 있다.
>> 
>> - ```DATABASES = {기 타 등 등}```
>> 
>> - 잘못 연동되었다고 지우고 다시하는건 하지말자 관련 명령어가 따로 존재한다.
> 
### 2. HTTP 프로토콜 GET, POST
> 1. HTTP 프로토콜이란.
>> 인터넷 통신에서 사용되는 규약이다.
>> 가장 중요한 것
>>> - GET : 보통 내용을 조회 할때 사용한다. 주소 안에 추가적인 파라미터를 첨부하여 보낸다. ```https://onion.haus/?param1=value1``` '?'부터 파라미터와 값 순서고 더 많은 내용을 첨부하기 위해서는 &로 구분한다. 
>>>
>>> - POST : 보통 사용할 때 서버 내의 정보를 생성/수정 할때 사용한다. GET와 같은 주소를 보낸다고 하더라도 추가적은 BODY라는 응답 외부에 있는 몸통에 데이터를 담아서(숨겨서) 전달한다. 숨긴다고 하더라도 암호화 되어있지는 않다(http의 경우이며, https는 암호화 되어있다).
>
### 3. GET, POST 프로토콜 실습
> 1. POST 프로토콜
>> GET은 브라우저에 넣으면 자동적으로 동작 하지만 POST는 설정을 따로 해줘야 한다.
>> 
>> POST를 사용하기 위해선 .html안에 form을 만들어 주어야 한다.
>> 
>> action 에는 요청을 보낼 주소를 method에는 사용할 방식(post 등)을 명시해야한다.
>> 
>> form 만 있다고 해서 정상적으로 작동하지 않는다.
>>  - 인터렉션 (작용)해야 사용이 가능 여기선 input태그를 작성한다.
>> 
>> 실습중인 창에서 버튼을 클릭해도 아무런 일이 발생하지 않는다.
>> - views.py(요청을 처리하는 곳)에서 post와 get를 나누어 다른 알고리즘을 적용하지 않았기 때문이다.
>> 
>> - views.py에서 반환한 값을 넣을 공간을 hello_world.html에도 작성한다.
>> 
>> **hello_world.html**
>> ```html
>> {% extends 'base.html' %}
>> 
>> 
>> {% block content %}
>> 
>>     <div style="height: 20rem; background-color: #38df81; border-radius: 2rem;  margin: 2rem;">
>>         <h1 style="text-align:center; margin: 2rem 0;">
>>             오늘은 14~강 까지 학습을 진행 중
>>         </h1>
>>         
>>         <form action="/account/hello_world/" method="post">
>>             {% csrf_token %}
>>             <input type="submit" class="btn btn-primary" value="POST">
>>             <!--
>>             class="btn btn-primary"는 부트스트랩의 라이브러리안에 있는 클래스들 중하나.
>>             btn과btn-primary를 동시에 적용하면 primary의 색을 가진 버튼이 그럴듯하게 생성된다
>>             (CSS로 스타일링 할 필요 없다.)
>>             -->
>>         </form>
>>         
>>         <form action="/account/hello_world/" method="get">
>>             {% csrf_token %}
>>             <input type="submit" class="btn btn-primary" value="GET">
>>         </form>
>>         
>>         <h1>
>>             {{ text }} <!--views.py에서 반환한 값을 받는 위치-->
>>         </h1>
>> 
>>     </div>
>> 
>> {% endblock %}
>> ```
>> **views.py**
>> ```Python
>> from django.http import HttpResponse
>> from django.shortcuts import render
>> 
>> # Create your views here. 니가 원하는 뷰를 여따 만들거라.
>> 
>> def hello_world(request):
>>     # return HttpResponse('안녕하세요')
>>     if request.method == "POST":
>>         return render(request, 'accountapp/hello_world.html', context={'text': 'POST METHOD!!!'})
>>         #context는 데이터 꾸러미라고 생각하면 된다. 즉 text라는 이름을 가지고 있고 내용물은 'POST METHOD!!!'이다.
>>     else :
>>         return render(request, 'accountapp/hello_world.html', context={'text': 'GET METHOD!!!'})
>> ```
>
>![get_post_testing](./image/Django12/Django_11_3.png)
>
### 4. POST 통신을 이용한 DB 데이터 저장 실습
> 1. Send POST data
>> **hello_world.html**
>> ```html
>> {% extends 'base.html' %}
>> 
>> 
>> {% block content %}
>> 
>>     <div style="border-radius: 2rem; margin: 2rem; text-align:center;">
>>         <h1 style="font-family: 'Nanum Gothic Coding', monospace;"> <!--'Indie Flower'가 없다면 cursive를 대신 써라.-->
>>             Hello World LIST!
>>         </h1>
>>         
>>         <form action="/account/hello_world/" method="post">
>>             {% csrf_token %}
>>             <div>
>>                 <input type="text" name="hello_world_input"> <!--text 데이터 입력받을 input.-->
>>                 <!--name는 id 와 같은것. 구분하기 위함.-->
>>             </div>
>>             <input type="submit" class="btn btn-primary" value="POST">
>>         </form>
>>         
>>         {% if hello_world_output %}<!--만약 hello_world_output가 있다면 endif 까지의 내용을 생성해라. -->
>>         
>>         <h1>
>>             {{ hello_world_output.text }} <!--views.py에서 반환한 값을 받는 위치-->
>>         </h1>
>>         
>>         {% endif %}
>>     </div>
>> 
>> {% endblock %}
>> ```
> 
> 2. Receive POST data & Save DB
>> **views.py**
>> ```Python
>> from django.http import HttpResponse
>> from django.shortcuts import render
>> from accountapp.models import HelloWorld #models.py에 만들어둔 HelloWorld클래스 사용하기 위해
>> 
>> 
>> def hello_world(request):
>>     if request.method == "POST":
>>         temp = request.POST.get('hello_world_input')
>>         # request에서 POST중'hello_world_input'라는 이름을 가진 데이터를 가져와라.
>>         
>>         new_hello_world = HelloWorld() #객체생성.
>>         new_hello_world.text = temp #text 넣고
>>         new_hello_world.save() #'db.sqlite3'에 저장.
>> 
>>         return render(request, 'accountapp/hello_world.html', context={'hello_world_output': new_hello_world}) #객체를 hello_world.html 반환함. 
>>         # context={'hello_world_output': new_hello_world}는 
>>         # hello_world.html의 {{ hello_world_output.text }}에 new_hello_world값을 넣는다는 뜻.
>>     else :
>>         return render(request, 'accountapp/hello_world.html', context={'text': 'GET METHOD'})
>> ```
>
### 5. DB 정보 접근 및 장고 템플릿 내 for loop
> 이전시간엔(사실 오늘) new_hello_world.save() 를 통해 DB 저장하는 것 까지 했다.
>
> 오늘(그 오늘이 오늘임)은 그 DB에 저장되어 쌓인 것들을 모두 가져와 화면에 출력하는 것을 실습한다.
> 
> 1. views.py파일(accountapp 하위)의 ```hello_world(request)```내용을 수정한다.
>> ```Python
>>         # new_hello_world.save()
>>         # 위 코드는 DB즉 나의 경우는 'db.sqlite3'에 저장하는 코드이다. 해당 코드 하단에
>>         
>>         hello_world_list = HelloWorld.objects.all() #이 코드를 추가하고
>>         #HelloWorld 의 모든 데이터를 전부 가져옴
>>         return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})
>>         #return 의  render()의 파라미터중 context에 넣는 값을 hello_world_list로 위와 같이변경한다.
>>         또한 else에서 return 하는 render의 값도 위와 같도록 수정한다
>> ```
> 
> 2. accountapp/hello_world.html 파일을 수정한다.
>> ```html
>>         {% if hello_world_list %}<!-- views.py에서 이름을 수정하였기 때문에 함께 수정 -->
>>             {% for hello_world in hello_world_list %}<!-- 리스트 = 배열 출력하기 위해선 반복문(for문)필요 -->
>>             <!-- 구조는 파이썬의 for 과 같아보임  for i in [1,2,3,4]  -->            
>>             <h4>
>>                {{ hello_world.text }} <!--받아온 배열/리스트의 값들이 하나씩 출력.-->
>>             </h4>
>>             {% endfor %}
>>         {% endif %}
>> ```
>
> 이후 웹에서 확인을 하면 정상적으로 출력이 된다. 
> 
> 하지만 마지막으로 POST한 값이 새로고침시 계속해서 DB에 저장된다
> 
> POST가 render까지 하였기 때문에 계속해서 POST가 하게 되었다 이를 막기위해 POST한 뒤엔 GET로 돌아가도록 내용을 아래와 같이 수정한다.
>> ```Python
>> def hello_world(request):
>>     # return HttpResponse('안녕하세요')
>>     if request.method == "POST":
>>         
>>         # if 내부의 hello_world_list = HelloWorld.objects.all()이 내용까지는 동일하다
>>         # return 의 내용을 아래와 같이 수정하고
>>         # hello_world_list = HelloWorld.objects.all()를 지운다.
>> 
>>         return HttpResponseRedirect(reverse('accountapp:hello_world'))
>>         # accountapp/urls.py에서 지정해둔 app_name = "accountapp"와
>>         # urlpatterns의 path에 지정해둔 name='hello_world'를 이용한다.
>>         # 또한 그 2개의 해당하는 경로를 만들어줄 reverse를 사용하여 한번더 감싸준다.
>>         # HttpResponseRedirect = accountapp에 있는 hello_world로 재접속 하라 라는 뜻.
>>         
>>     else :
>>         #else의 내용은 아래와 같이 수정한다. return의 내용은 전과 동일하다.
>>         hello_world_list = HelloWorld.objects.all()
>>         return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})
>> ```
> [HttpResponseRedirect](https://valuefactory.tistory.com/605)자세히 알아보기.
>
> ![hello_world_list](./image/Django12/Django_11_4.png)
>
