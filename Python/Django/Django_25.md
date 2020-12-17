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
