# Django 프로젝트
##### Date 2020_12_17
오늘부터 다시 시작합니다.
---
진짜로 처음부터 다시했습니다.

accountapp 을 만들고 시작 하였습니다.

기본적인 settings.py, urls.py를 설정하고 accountapp 의 urls.py, views.py를 작성하였습니다

작성을 하고 ```python manage.py makemigrations```, ```python manage.py migrate```명령어를 통해 DB를 만들었습니다.

```Python
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.models import User
from accountapp.forms import AccountUpdateForm

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth # 로그인


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

# class AccountUpdateView(UpdateView):
#     model = User
#     form_class = AccountUpdateForm
#     context_object_name = 'target_user'
#     success_url = reverse_lazy('accountapp:success')
#     template_name = 'accountapp/update.html'

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
```
오늘 작성한  views.py부터 보겠습니다.

class형식으로 작성하려 노력했습니다.

솔직히 함수형보다는 뭔가 유지보수가 더 편할 것 ? 같다는 생각이 들어서 그랬습니다.

AccountCreateView부터 보면 html파일에 사용자가 입력한 값을 POST방식으로 전달받어 사용합니다.

간단하게 ID와 2개의 패스워드를 받기로 했습니다.(패스워드 오타 방지)

그 뒤 User에 존재하는 ID와 사용자가 입력한 ID가 같은지 검증하는 과정을 거친뒤.

각각 필요한 메시지를 출력하기 위한 과정을 지나 

사용자가 입력한 ID와 PW를 User에 등록합니다. 이때 PW는 make_password를 사용해 암호화 하여 저장합니다.

그리고 적절한 방식으로 return 합니다.

---

다음으론 AccountSuccessView를 보겠습니다.

간단히 말하면 그냥 회원가입 성공 또는 비밀번호 변경 성공시 띄울 창을 간단히 만든 것 입니다.

model는 User을 template는 'accountapp/success.html'를 사용 하였고

일반 View를 상속받아 만든 것이기 때문에 def post와 get를 직접 작성 해야합니다.
```
def get(self, request):
        return render(request, 'accountapp/success.html')
```
get의 경우는 위와 같이 간단히 구현 할 수 있습니다.

---

다음으론 AccountUpdateView먼저 진행 하겠습니다.

기본적인 원리는 CreateView와 동일합니다.

전에 실습을 할 때에는 pk가 필요한 상태로 작동 되도록 하였지만

지금은 pk를 url에 사용하지 않도록 하였습니다.

request를 보낸 사용자의 패스워드만 변경 가능하도록 하였기 때문입니다.

2개의 패스워드를 입력받은후 2개가 같을대 그리고 이전에 사용하던 패스워드와 등록된 패스워드가 같을때

새로운 패스워드로 변경되도록 하였습니다.

이곳 또한 일반 View를 상속받아 사용하였기에 
```
def get(self, request):
        return render(request, 'accountapp/update.html')
```
위와 같이 간단히 작성 합니다.

---
다음은 AccountDetailView입니다.

간단합니다. DetailView를 상속 받아 작성하였습니다.

사용할 모델, 탬플릿에서 사용할 user객체 이름, 탬플릿명을 작성합니다.

---
---

### urls.py
(accountapp)
```Python
from django.urls import path
from accountapp.views import AccountCreateView,AccountSuccessView, AccountDetailView, AccountUpdateView
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'accountapp'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accountapp/login.html'), name='login'),
    # LoginView 같은 경우는 템플릿을 지정해줘야 한다.(직접 만들것임.)
    path('logout/', LogoutView.as_view(), name='logout'),
    # LoginView와 LogoutView 둘다 import 필요.
    
    path('create/', AccountCreateView.as_view(), name='create'),
    path('success/', AccountSuccessView.as_view(), name='success'),
    
    path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
    path('update/', AccountUpdateView.as_view(), name='update'),
]
```

### create.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div class="mb-4"><!--margin-bottom-->
            <h4>회 원 가 입</h4>
        </div>
        <div>
            {{ message }}
        </div>
        <form action="{% url 'accountapp:create' %}" method="post">
            <!--action 내부엔 요청을 보내는 url이 필요하다. 여기서는 일원화(어떤 앱에서:어떤 라우팅으로 가라.) 할것이다.-->
            {% csrf_token %}
            
            <div class="form-group">
              <label for="username">사용자 이름</label>
              <input 
              type="text" 
              class="form-control" 
              id="username" 
              placeholder="사용자 이름"
              name="username">   
              <!-- 이 name 값으로 정보가 전달된다 -->
            </div>
            
            <div class="form-group">
              <label for="password">비밀번호</label>
              <input type="password" 
              class="form-control"
               id="password"
                placeholder="비밀번호"
                name= "password">
            </div>
            <div class="form-group">
              <label for="re_password">비밀번호 확인</label>
              <input 
              type= "password" 
              class="form-control"
               id="re_password"
                placeholder="비밀번호 확인"
                name = "re_password">
            </div>
            
              <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
        </form>
    </div>

{% endblock %}
```

### login.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div>
            <h4>Login</h4>
        </div>
        <form action="" method="post">
            {% csrf_token %}
            {% bootstrap_form form %}
            <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
            <!--rounded-pill는 버튼의 외형을 동글동글한 걸로 바꿈(클래스) col-6 은 부모의 크기의 절반(12가 최대이며 100%를 뜻함) mt-3은 margin-top의 3배라는 뜻-->
        </form>
    </div>

{% endblock %}
```

### update.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        <div class="mb-4">
            <h4>회원정보 수정</h4>
        </div>
        <h5>
           ID : {{ user.username }}
        </h5>
        <h5 textcolor = red>
           {{ message }}
        </h5>
        <form action="{% url 'accountapp:update' %}" method="post">
            <!--action 내부엔 요청을 보내는 url이 필요하다. 여기서는 일원화(어떤 앱에서:어떤 라우팅으로 가라.) 할것이다.-->
            {% csrf_token %}
            
            <div class="form-group">
              <label for="origin-password">사용하던 패스워드</label>
              <input type="origin-password" 
              class="form-control"
               id="origin-password"
                placeholder="비밀번호"
                name= "origin-password">
                
            </div>
            <div class="form-group">
              <label for="password">새 비밀번호</label>
              <input type="password" 
              class="form-control"
               id="password"
                placeholder="비밀번호"
                name= "password">
            </div>
            
            <div class="form-group">
              <label for="password2">새 비밀번호 확인</label>
              <input 
              type= "password" 
              class="form-control"
               id="password2"
                placeholder="비밀번호 확인"
                name = "password2">
            </div>

              <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
        </form>
    </div>

{% endblock %}
```

### success.html
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}

    <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
        
        <div class="mb-4"><!--margin-bottom-->
            <h4>가 입 완 료</h4>
        </div>
        
        <h1>
            {{ user.username }}
            {{ user.is_authenticated }}
            {{ message }}
        </h1>
    </div>

{% endblock %}
```

오늘 작성한 간단한 html파일들 입니다.

오늘은 이만 정리하도록 하겠습니다. 안녕★

내일은 이제 Article 과 Comments를 진행 해보도록 하겠습니다.

