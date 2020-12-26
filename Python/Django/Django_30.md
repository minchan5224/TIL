# Django 프로젝트
##### Date 2020_12_22

마무리... [코드 보러가기](https://github.com/minchan5224/DjangoProject)

---
```html
<style>
    h2 {
     /* position the text */
        position: absolute;
        left: 0px;
        display: none;
        width: 100%;
        text-align: center;
        margin: 0;
        height: 65%;
        top: 65%;
    }

    img:hover + h2 {
        display: block;
    }

    img:hover {
        opacity: 0.5;
    }
</style>
<div style="margin-top: 2rem;">
    <a href="{{ target_article.image.url }}" target="_blank">
        <img style="width:100%; border-radius: 1rem; margin: 2rem 0" src="{{ target_article.image.url }}" alt="">
        <h2>
            <strong>
                원본을 보려면 클릭 하세요.
            </strong>
        </h2>
    </a>
</div>
```
이미지 위에 커서를 올리면 반투명 해지고 텍스트를 출력하는 코드

해당 코드를 이용하여 articles/list에서는 각각의 article의 title를 제공하고

articles/detail에서는 "원본을 보려면 클릭 하세요." 텍스트를 출력한고 클릭시 원본 이미지를 새탭으로 출력한다.

### 지하철 시간표 api 이식

subway_time.py파일을 가져왔고 POST가 들어왔을때 응답하도록 작성 하였다.

임시로 다른 app에 작성을 하였지만

startapp을 통하여 subwayapp을 만들어 옮길 예정이다.

views.py
```Python
from "views.py가 존재하는 경로상"app import subway_time
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
from datetime import datetime


@method_decorator(csrf_exempt, name='dispatch') # 이거 없으면 csrf관련 오류가 발생한다. 이쪽에서만 csrf를 해제해준다.
class SubwayTimeView(View):
    template_name = 'articlelikeapp/subway.html'
    def post(self, request):
        content = self.request.body
        content = json.loads(content)
        content = content['userRequest']
        content = content['utterance']
        KST = datetime.now(timezone('Asia/Seoul'))
        dataSend = subway_time.main_service(content, KST)
        return JsonResponse(dataSend)
```
위와같이 viwes.py를 작성하고 template은 혹시몰라 그냥 아래와 같이 작성하였다.
```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block content %}
{% csrf_token %}
{% endblock %}
```
딱히 뭐 들어있는 것도 없다.
urls.py는 ```path('subway/', SubwayTimeView.as_view(), name='subway'),```처럼 간단히 작성하면 끝이다.

이제 진짜 끝이다.

영상을 보고 배우고 처음 시작한 Django프로젝트였다.

처음엔 2주 가량 걸릴것이라 생각했다. 

하다보니 하루에 8~10시간은 앉아서 계속 여러 방법을 사용해보고 생각해본것 같다.

4일? 5일? 정도 재미있었다. 

역시 배운것은 응용을 여러가지로 해야하는것 같다. 

오늘은 여기까지.

[코드 보러가기](https://github.com/minchan5224/DjangoProject)
