# Django 프로젝트
##### Date 2020_12_15
오늘부터 시작합니다.
하지만 내일은 알바...
---
1. models.py 작성
> ```Python
> from django.db import models
> 
> # Create your models here.
> 
> class User(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
>     username = models.CharField(max_length=20,verbose_name = 'ID')
>     # verbose_name  관리자페이지에서 보여지는 이름
>     password = models.CharField(max_length=20,verbose_name = 'PW')
>     registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='RegistrationTime') 
>     # 저장되는 시점의 시간을 자동으로 삽입해준다.
> 
>     # class Meta:
>     #     db_table = 'test_user'
>     # 테이블명 지정 설정을 안하면 자동으로 클래스명+app이름과 같은 형식으로 이름 설정
> ```
> 
> 2. 마이그레이션 파일 생성및 마이그레이션 DB에 반영
> ```python manage.py makemigrations``` 생성
> 
> ```python manage.py migrate``` 반영
> 
> 3. admin에 Model Class 등록및 슈퍼계정 생성
> 작성한 model클래스를 등록해 admin에서 사용하기 위해서
> 
> 같은 폴더의 admin.py에 아래 내용을 작성한다.
> ```Python
> from django.contrib import admin
> from .models import User
> # 같은 경로의 models.py에서 User라는 클래스를 임포트한다.
> 
> class UserAdmin(admin.ModelAdmin) :
>     # admin.ModelAdmin을 상속받으면 admin페이지에서 어떠한 Column을 관리할지에 대한 설정이 가능
>     list_display = ('username', 'password')
>     # list_display엔 관리자 페이지에서 볼 Column을 기입.
> 
> 
> admin.site.register(User, UserAdmin) #site에 등록
> ```
> 
> 터미널에 ```python manage.py createsuperuser```명령어를 사용해 슈퍼계정 생성.
> 
> 3. 회원가입 페이지 설정 
> 
> 회원가입 내맘대로 커스텀이 가능해졌다.
> 
> 이거 끝내는것만 시간이 엄청 걸렸다..
> 
> ```Python
> class AccountCreateView(View):
>     def post(self, request):
>         user_id = request.POST.get('username',None)
>         password = request.POST.get('password',None)
>         re_password = request.POST.get('re_password',None)
> 
>         if User.objects.filter(username = user_id).exists() == True:
>             message = "이미 존재하는 아이디입니다."
> 
>         elif password != re_password:
>             message = "비밀번호가 다릅니다."
> 
>         elif user_id == '' or password == '':
>             message = "모든 내용을 입력하세요."
> 
>         else:
>             User.objects.create(username = user_id, password = make_password(password))
>             return render(request, 'accountapp/success.html')
> 
>         return render(request, 'accountapp/create.html', {'message': message})
> 
>     def get(self, request):
>         return render(request, 'accountapp/create.html')
> 
> 
> class AccountDetailView(DetailView):
>     model = User
>     context_object_name = 'target_user' # 탬플릿에서 사용하는 user의 객체 이름을 target_user로 다르게 설정해줌
>     # 로그인 한 상태에서 자신의 페이지로 들어와 정보를 볼 수 있었지만 이제 다른사람이 그 페이지에 들어가더라도 정상적으로 열람 가능하다.
>     template_name = 'accountapp/detail.html'
> ```
> 일단 회원가입은 위외같이 간단히 정리 하였다. 
> 
> 함수형보다 클래스형으로 하는것이 좋을 것 같다는 그냥 혼자만의 생각에 이렇게 구성 하였다.
> 
> 사실 로그인 view도 별 다를건 없다.
> 
> 오래걸린 이유는 단지 어떤 함수가 있는지랑 어떤 문법으로 써야하는지 하나도 몰랐어서
> 
> 처음부터 하나하나 다 써보면서 확인했다.
> 
> 무식해 보여도 난 이게 가장 받아들이가 편하다.
> 
> ```Python
> class AccountLoginView(View):
>     def post(self, request):
>         login_user_id = request.POST.get('username',None)
>         login_password = request.POST.get('password',None)
> 
>         if not (login_user_id and login_password):
>             message = "아이디와 비밀번호를 모두 입력해주세요."
>         else : 
>             user = User.objects.get(username=login_user_id) 
>             #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
>             if check_password(login_password, user.password):
>                 request.session['user'] = user.id 
>                 #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
>                 #세션 user라는 key에 방금 로그인한 id를 저장한것.
>                 return redirect('accountapp:success')
>             else:
>                  message = "비밀번호를 틀렸습니다."
> 
>         return render(request, 'accountapp/login.html', {'message': message})
> 
>     def get(self, request):
>         return render(request, 'accountapp/login.html')
> ```
> 로그인 뷰는 회원가입 뷰 다음에 작성한거라 3분도 안걸린것같다.
> 
> 개념자체는 뭐 POST받아서 DB의 값과 비교해서 검증하는 거니 딱히 어려운건 없었다.
> 
> 임시로 successView를 만들었다 
> 
> 아무래도 회원가입이나 로그인후 눈에 보이는게 필요할것 같아서 그냥 대충 만들었다.
> 
> 그래도 깔끔하니 보기 좋다.
> 
> 내일은 알바다 일찍자야해서 오늘은 여기가지만 하겠다.
> 
> html파일은 내일 같이 정리해서 올릴것이다 (아마도)
> 
> 그럼 오늘은 20000 안녕
> 
> ps.
> 추가로 할일 html들 내용수정
> 
> 전에 쓰던거 들고온거라 필요없는 내용이 너무 많음
> 
> 깔끔하게 정리
> 
> 부트스트랩은 설치 했음.
> 
> 내일도 좋은하루.
> 
> urls.py는 아래와 같아졌다.
> ```Python
> from django.urls import path
> from accountapp.views import AccountCreateView, AccountDetailView, AccountSuccessView, AccountLoginView
> from django.contrib.auth.views import LoginView, LogoutView
> app_name = 'accountapp'
> urlpatterns = [
>     path('login/', AccountLoginView.as_view(), name='login'),
>     # # LoginView 같은 경우는 템플릿을 지정해줘야 한다.(직접 만들것임.)
>     # path('logout/', LogoutView.as_view(), name='logout'),
>     # # LoginView와 LogoutView 둘다 import 필요.
>     path('create/', AccountCreateView.as_view(), name='create'),
>     # 최종적인 url은 /user/create 된다.
>     path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
>     path('success/', AccountSuccessView.as_view(), name='success'),
> ] 
> ```
> 
> 
