# [Django Form](http://pythonstudy.xyz/python/article/313-Django-%ED%8F%BC-Form)
##### Date 2020_11_21
---
 ### 1. Django Form
>  Django 프레임워크는 Model 클래스로부터 폼(Form)을 자동으로 생성하는 기능을 제공한다.
>
>> 모델 클래스로부터 폼 클래스를 만들기 위해선
>> 1. django.forms.ModelForm 클래스으로부터 파생된 사용자 폼 클래스를 정의
>>
>> 2. 용자 폼 클래스 안에 Meta 클래스를 정의하고 Meta 클래스 안 model 속성(attribute)에 해당 모델 클래스를 지정(어떤 모델을 기반으로 폼을 작성할 것인지를 Meta.model 에 지정)
>
> #### Model 클래스(./feedback/models.py)
>> ```Python
>> from django.db import models
>>  
>> class Feedback(models.Model):
>>      name = models.CharField(max_length=100)
>>      email = models.EmailField()
>>      comment = models.TextField(null=True)
>>      createDate = models.DateTimeField(auto_now_add=True)
>> ```
>>
>> 위의 Feedback 모델 클래스에 기반하여 **폼 클래스를 만들기 위해 ./feedback/forms.py 를 만들고** 아래와 같이 **폼 클래스 "FeedbackFrom"를 정의**한다.
>>> ```Python
>>> from django.forms import ModelForm
>>> from .models import Feedback
>>>  
>>> class FeedbackForm(ModelForm):
>>>     class Meta:
>>>         model = Feedback
>>>         fields = ['id', 'name','email','comment']
>>> ```
>>> - FeedbackFrom 클래스는 ModelForm로부터 파생된 클래스
>>>
>>> - Meta 안의 model 속성에 "models.Feedback" 모델 클래스를 지정
>>>
>>> - fields는 모델 클래스의 필드들 중 일부만 폼 클래스에서 사용하고자 할 때 지정하는 옵션(위에선 createDate를 뺀 나머지 필드들만 사용하도록 정의)
>> 
> **사용자 폼이 정의되었으면, View와 템플릿에서 이 폼을 사용하게 된다.**
> 
> ```Python
> from django.shortcuts import render, redirect
> from .models import *
> from .forms import FeedbackForm
>  
> def create(request):
>     if request.method=='POST':
>         form = FeedbackForm(request.POST)
>         if form.is_valid():
>             form.save()
>         return redirect('/feedback/list')
>     else:
>         form = FeedbackForm()
>  
>     return render(request, 'feedback.html', {'form': form})
> ```
> 위는 ```./feedback/views.py``` 에 추가된 함수로서 새로운 Feedback 데이타를 추가하기 위한 폼을 핸들링하는 함수다.
> 
> 크게 두 부분으로 나눌 수 있다.
>> #### 1. 데이터를 입력 받는 폼을 보여 주는 부분
>>> 데이터를 입력 받는 폼은 POST가 아닌 부분(else 부분)과 마지막 render 부분으로 입력 부분만 가져오면 다음과 같다.
>>> ```Python
>>> def create(request):
>>>     form = FeedbackForm()
>>>     return render(request, 'feedback.html', {'form': form})
>>> ```
>>> - render()의 첫번째 파라미터는 request를 지정
>>>
>>> - 두번째는 사용할 템플릿 파일을 지정 
>>>
>>> - 세번째 파라미터는 템플릿에 전달한 데이터 또는 객체들을(컨텍스트) 지정
>>>
>>> 컨텍스트는 Dictionary로 전달한다.(여기선 "form"이라는 키에 FeedbackFrom()빈 객체값을 할당하여 전달)
>>>
>>> 위에서 호출하는 템플릿 (./feedback/templates/feedback.html) 예제는 다음과 같다.
>>> ```html
>>> {% extends "base.html" %}
>>> 
>>> {% block content %}
>>>     <p>
>>>         <a href="{% url 'list' %}">Goto Feedback List</a>
>>>     </p>
>>> 
>>>     <div>
>>>         <form method="POST">
>>>             {% csrf_token %}
>>>             {{ form.as_p }}
>>>             <button type="submit">저장</button>
>>>         </form>
>>>    </div>
>>> 
>>> {% endblock content %}
>>> ```
>>> - 템플릿에서 주목할 부분은 View에서 전달한 "form"객체를 템플릿 변수로 사용하는 부분이다.
>>> 
>>> - 예제에선 {{ form.as_p }}와 같이 폼을 <p> 태그를 사용하여 랜더링하도록 한다.(form.as_p는 폼의 각 필드를 p 태그 안에서 레이블과 텍스트로 배치한다)
>>>
>>> - 폼을 랜더링하는 옵션으로 form, form.as_p, form.as_table, form.as_ul 등이 있다.(각 필드를 어떤 HTML 태그로 Wrapping 할 것인가를 지정하는 것)
>>>
>>> - HTML FORM 안에 {% csrf_token %} 를 넣어 준 것(CSRF를 방지하기 위한 기능을 기본적으로 제공, Django에서 HTTP POST, PUT, DELETE을 할 경우 이 태그를 넣어 주어야 한다.)
>>
>> #### 2. 사용자가 데이터를 입력하여 저장버튼을 눌렀을 때 이를 DB에 저장하는 부분
>>
>> 
> 
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
