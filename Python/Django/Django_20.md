# Django 실습
##### Date 2020_12_7
---
### 모바일 디버깅, 반응형 레이아웃 
###### [39강](https://www.youtube.com/watch?v=qvLYJBzcD_I&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=40)
> 모바일에서 보기 좋은 사이즈로 제공하기 위해 아래의 코드를 head.html에 추가한다.
> ```<meta charset="UTF-8">```의 아래에
> ```
> <meta name="viewport" contnet="width=device-width, initial-scale=1, shrink-to-fit=no">
> ```
> 를 작성한다.
> 
> articleapp의 list.html의 <style>부분에 
> ```
>     .container {
>         padding: 0;
>         margin: 0, auto;
>     }
>     
>     .container a {
>         width: 45%;
>         max-width: 250px;
>     }
> ```
> 
> 위와 같이 2개의 컨테이너를 더 설정 하였으며
> 
> magicgrid.js의 ```let magicGrid = new MagicGrid```에서
> 
> ```gutter: 30,```을 ```gutter: 12,```로 수정 하였다.
> 
> 마지막으로 base.css에 아래의 내용을 추가 하였다.
> ```
> @media screen and (max-width:500px) {
>     html {
>         font-size: 13px;
>     }
> }
> ```
> ~~ 끝!~~
> ~~ 오늘은 [38강](https://www.youtube.com/watch?v=egXJzs06f3Q&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=39)의 학습을 진행 하였다.~~
> ## ~~ 참고한 영상 : [실용주의 프로그래머의 작정하고 장고! Django로 Pinterest 따라하기](https://www.youtube.com/playlist?list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo)~~
