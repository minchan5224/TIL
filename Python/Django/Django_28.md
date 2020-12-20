# Django 프로젝트
##### Date 2020_12_20
으아아 댓글 더보기/ 줄이기 구현

---
```html
<script>
function RecommendFunction(idMyDiv){
    var objDiv = document.getElementById(idMyDiv);
    if(objDiv.style.display=="block"){
        objDiv.style.display = "none";
        ButtonSetting.innerHTML = "댓글 더보기";

    }
    else{
        objDiv.style.display = "block";
        ButtonSetting.innerHTML = "댓글 접기";
    }
}
</script>

<style>
    .hide_show_setting{color:black;margin-bottom:30px}
    .hide_show_setting button {cursor:pointer;padding:.4rem;border-radius: 10rem; outline:0;box-shadow: 0 0 4px;}
    .hide_show_setting .blind_view{}
    .hide_show_setting_view { display:block; }
</style>
```
기본적인 함수는 위와 같구 ```ButtonSetting.innerHTML = "댓글 더보기";```이 뭐냐면

ButtonSetting라는 아이디를 가진 태그의 텍스트를 "댓글 더보기" 바꾸겠다 입니다. 쉬워요;;

그리고 각 html에서 함수를 이용하기 위한 id들은 text와 pk등으로 구성된 이름으로 새로 만들었습니다.
