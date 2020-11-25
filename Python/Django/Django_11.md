# Django 실습
##### Date 2020_11_24
---
### 1. CSS파일 분리
> CSS파일이란 디자인파일만 따로 분리해둔 것이라고 보면 된다.
> 
> html파일에서 sytle속성을 따로 관리를 하는 것 -> 보통 개발패턴
> 
> 따로 분리하기전 static에 관한 설정을 해야함
> 
> static -> 정적 -> CSS 자바스크립트 폰트 등 자주 변경하지 않는 에셋, 파일들을 말함.
>
> 프로젝트와 앱 별로 따로 관리한다. Static files (CSS, JavaScript, Images)
>
> settings.py 의 맨 하단에 있는 STATIC_URL 아래에
> ```STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')```을 추가한다.
> - ROOT폴더 경로 설정.(터미널에서 python manage.py collectstatic 하였을때 static파일이 모일 위치.)
>
> 위에서 설정한 settings.py의 STATIC_ROOT 아래에
> ```Python
> STATICFILES_DIRS = [
>     #BASE_DIR / "static", 난 이거 에러나서 바꿈
>     os.path.join(BASE_DIR, "static"), #이걸로 바꿈
> ]
> ```
> 를 추가한다.
> 
> 앱에 종속되어 있지 않은(프로젝트 전체에서 관리가 가능한.) static폴더 생성한다. (사진참고)
>> ![srtarapp_accountapp](./image/Django10/Django_10_1.png)
> 
> 그 후 내부에 base.css 파일을 생성한다.
>
> ```Python
> .BS_footer_logo{
>     font-family: 'Indie Flower', cursive;
> }
> ```
> 위의 내용으로 base.css를 작성한뒤. footer.html의 내용을 아래와 같이 수정한다.(영상 8분쯤)
> ```
>             <h6 class="BS_footer_logo"> <!--여기 내용만 변경됨.-->
>                 Backend Study
>             </h6>
> ```
> 아직까지는 footer.html에 수정한 내용을 토대로 base.css에 접근해 사용할 수 없다.
>
> 사용이 가능하도록 하기위해 base.html의 <head> 내용을 담고 있는 head.html에 해당 내용을 추가한다.
> ```Python
>     <!-- DEEFAULT CSS LINK -->
>     <link rel="stylesheet" type="text/css" href="{% static 'base.css' %}">
> ```
> ```<!-- GOOGLE FONT LINK -->```가 달린 부분 하단에 작성하면 된다.
>
> ```href="{% static 'base.css' %}"```이 부분을 통해 base.css에 해당하는 경로를 장고가 알아서 랜더링 하여 실제 브라우저에 넘겨줘 css파일을 템플릿에서 사용이 가능하게 해준다.
>
> 최종 base.css내용
> ```Python
> .BS_logo{
>     font-family: 'Indie Flower', cursive;
> }
> 
> .BS_footer_button{
>     font-size: .6rem;
> }
> 
> .BS_footer{
>     text-align:center;
>     margin-top: 2rem;
> }
> 
> .BS_header{
>     text-align:center;
>     margin: 2rem 0;
> }
> ```
> footer.html내용
> ```Python
>     <hr>
>     <div class="BS_footer">
>         <div class="BS_footer_button">
>             <span>공지사항</span> |
>             <span>제휴문의</span> |
>             <span>서비스 소개</span>
>         </div>
>         <div style="margin-top: 1rem">
>             <h6 class="BS_logo">
>                 Backend Study
>             </h6>
>         </div>
>     </div>
> ```
> header.html내용
> ```
>     <div class="BS_header">
>         <div>
>             <h1 class="BS_logo">
>                 Backend Study
>             </h1>
>         </div>
>         <div>
>             <span>nav1</span> | 
>             <span>nav2</span> | 
>             <span>nav3</span> | 
>             <span>nav4</span>
>         </div>
>     </div>
>     <hr>
> ```
> 
### 2. CSS 핵심
> 간단하게 html을 꾸미기 위한 디자인 묶음이라고 볼 수 있다.
> 
> [DISPLAY속성](https://www.youtube.com/watch?v=T1I9CsvHruQ&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=12&t=100)<!--(12강 1:40~5:08)-->
>> 각각의 태그마다 디스플레이 속성이 있다.
>> - Block : 모든 태그에는 부모가 존재. 부모의 최대한의 넓이를 가져가며 블럭의 모양의 형태를 가지는 것. 높이는 따로 설정하지 않으면 기본 설정 혹은 내용물에 맞춰서 크기 결정, 태그가 여러게 있다면 아래로 쌓임
>>
>> - Inline : 글씨가 들어가 있다면 글씨의 높이 만큼만 가져감(just text line height "in" line). 태그가 여러게 있다면 옆으로(오른쪽으로) 쌓임
>>
>> - Inline block : inline와 block가 섞인것 블록임에도 인라인처럼 옆으로 쌓임.
>>
>> - None  : 태그상으론 존재하지만 시각화하면 없음, 말 그대로 없음. visibility의 hidden과는 다름 hidden은 존재하지만 안보여주는 것이고 None는 그냥 없는것.
>
> [SIZE 척도에 대한 값들](https://www.youtube.com/watch?v=T1I9CsvHruQ&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=12&t=311)
>> Responsive, 반응형 사이트를 만들기 위해서 신경써야함 -> 화면의 크기가 다르다(폰 노트북 데스크탑 등)
>> 
>> - px : 픽셀, 항상 고정된값. 즉 절대값이라고 생각하면 된다.
>> 
>> - em : 부모의 단위가 커지면 함께 증가한다. 작아져도 함께 작아진다. 하지만 부모가 여러개 있을때 증가하는 단위가 배로 증가한다. (2배 증가해야할때 2*2=4배 증가하는 경우 생김.)
>> 
>> - rem : 거의 모든 곳에서 사용. root HTML에 적용된 기본적인 폰트 사이즈의 증/감에 따라 함께 증/감 한다.(보통 1rem은 16픽셀 이다.)
>> 
>> - % : 가끔씀
>
### 3. CSS 디스플레이 속성, rem 단위 실습.
> 
> default는 따로 지정하지 않으면 block속성을 따른다.
> 
> 잠시 accountapp/templates/accountapp/hello_world.html의 내용을 다음과 같이 수정하여 실습을 진행 하였다.
> ```Python
> {% block content %}
>     <style>
>         .testing {
>             background-color: white;
>             height: 3rem;
>             width: 3rem;
>             margin: 1rem;
>         }
>     </style>
> 
>     <div style="height: 20rem; background-color: #38df81; border-radius: 2rem;  margin: 2rem;">
>         <h1 style="text-align:center; margin: 2rem 0;">
>             오늘은 11~13강 까지 학습을 진행 하였습니다.
>         </h1>
>         <div class="testing" style="display: block;">block</div>
>         <div class="testing" style="display: inline;">inline</div>
>         <div class="testing" style="display: None;">None</div>
>         <div class="testing" style="display: inline-block;">inline-block</div>
>         <div class="testing">default</div>
>         
>     </div>
> {% endblock %}
> ```
> # 끝! 
> 오늘은 [13강](https://www.youtube.com/watch?v=D3DMvHsn9Ss&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=13) 까지 학습을 진행 하였다.
> # 참고한 영상 : [실용주의 프로그래머의 작정하고 장고](https://www.youtube.com/playlist?list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo)
