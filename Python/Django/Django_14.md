# Django 실습
##### Date 2020_11_28
---
### 1. UpdateView를 이용한 비밀번호 변경 구현
> 1. Views.py에 AccountUpdateView 생성
>> ```Python
>> class AccountUpdateView(UpdateView):
>>     model = User
>>     form_class = UserCreationForm
>>     success_url = reverse_lazy('accountapp:hello_world')
>>     template_name = 'accountapp/create.html'
>> ```
> 2. urls.py에 경로(라우팅) 추가
>> ```Python
>> from accountapp.views import AccountUpdateView
>> urlpatterns = [
>> 
>>     ...
>>     
>>     path('update/<int:pk>', AccountUpdateView.as_view(), name='update'),
>> ]
>> ```
>> 
> 3. update.html생성
>> ```html
>> {% extends 'base.html' %}
>> {% load bootstrap4 %}
>> 
>> {% block content %}
>> 
>>     <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>>         <div class="mb-4">
>>             <h4>회 원 정 보 수 정</h4>
>>         </div>
>>         <form action="{% url 'accountapp:update' pk=user.pk %}" method="post">
>>             <!--지금 로그인 되어있는 회원의 정보를 수정할 것임 pk=user.pk 사용. -->
>>             {% csrf_token %}
>>             {% bootstrap_form form %}
>>               <input type="submit" class="btn btn-dark rounded-pill col-6 mt-3">
>>         </form>
>>     </div>
>> 
>> {% endblock %}
>> ```
>> 
> 4. detail.html수정
>> 회원정보를 보는 창에서 로그인중인 회원과 열람하는 회원이 같을경우 회원정보를 수정하는 버튼을 제공한다.
>> ```html
>> {% extends 'base.html' %}
>> {% load bootstrap4 %}
>> 
>> {% block content %}
>> 
>>     <div>
>>         <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>>             <p>
>>                 {{ target_user.date_joined }}<!--언제 가입했는지.-->
>>             </p>
>>             <h2>
>>                 {{ target_user.username }}
>>             </h2>
>>             
>>             {% if target_user == user %}
>>             <a href="{% url 'accountapp:update' pk=user.pk %}">
>>                 <p>
>>                     정보 수정
>>                 </p>
>>             </a>
>>             {% endif %}
>>         </div>
>>     </div>
>> 
>> {% endblock %}
>> ```
> 5. ```self.fields['username'].disabled = True``` 'username' 비활성
>> ![changeinfo]()
>> 
>> 사진과 같이 지금은 아이디와 비밀번호 둘다 수정이 가능하다. 
>> 
>> 이는 원하지 않는 상황이다 그러므로 수정하기 위해 다음 과정을 진행한다.
>> 
>> accountapp내부에 forms.py파일을 생성한다.
>> 
>> 그리고 그 파일은 views.py의 AccountUpdateView클래스에서 사용한
>> 
>> UserCreationForm을 상속받아 살짝 커스터마이징을 할 것이다.
>> 
>> ```Python
>> from django.contrib.auth.forms import UserCreationForm
>> 
>> class AccountUpdateForm(UserCreationForm):
>>     def __init__(self, *args, **kwargs):
>>         super().__init__(*args, **kwargs)
>> 
>>         self.fields['username'].disabled = True
>>         # 위의 코드가 없다면 AccountUpdateForm와 UserCreationForm 가 같다.
>>         # 하지만 위의 코드가 있다면 초기화 이후 'username'의 값을 비활성시킨다.
>>         # 또한 누군가가 임의로 값을 바꾸어 보내더라도 비활성화 되어있기 때문에 서버에 적용되지 않는다.
>> ```
>> 위와 같이 파일을 작성 하였다.
>> 
>> 이후 viwes.py에서 아래와 같이 적용 시킨다.
>> 
>> ```Python
>> from accountapp.forms import AccountUpdateForm
>> 
>> class AccountUpdateView(UpdateView):
>>     ...
>>     form_class = AccountUpdateForm
>>     ...
>> ```
>> 아래 그림과 같이 아이디 부분이 비활성화 된것을 확인할 수 있다.
>> ![changeinfo_2]()
> 
### 2. DeleteView기반 회원탈퇴 구현
> 1.Views.py에 AccountDeleteView 생성
>> ```Python
>> from django.views.generic import DeleteView
>> 
>> ...
>> 
>> class AccountDeleteView(DeleteView):
>>     model = User
>>     success_url = reverse_lazy('accountapp:login')
>>     template_name = 'accountapp/delete.html'
>> ```
>> 
> 2. urls.py에 경로(라우팅) 추가
>> ```Python
>> from accountapp.views import AccountDeleteView
>> 
>> ...
>> 
>> urlpatterns = [
>>     ...
>>     path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete'),
>> ]
>> ```
> 3. delete.html 작성
>> ```html
>> {% extends 'base.html' %}
>> {% load bootstrap4 %}
>> 
>> {% block content %}
>> 
>>     <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>>         <div class="mb-4"><!--margin-bottom-->
>>             <h4>회 원 탈 퇴</h4>
>>         </div>
>>         <form action="{% url 'accountapp:delete' pk=user.pk %}" method="post">
>>             {% csrf_token %}
>>               <input type="submit" class="btn btn-danger rounded-pill col-6 mt-3">
>>         </form>
>>     </div>
>> 
>> {% endblock %}
>> ```
> 4. detail.html에 delete버튼 추가.
>> ```html
>>             <a href="{% url 'accountapp:delete' pk=user.pk %}">
>>                 <p>
>>                     탈 퇴
>>                 </p>
>>             </a>
>> ```
>> 정보수정 버튼 아래에 추가.
