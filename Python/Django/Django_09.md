# [Static 파일](http://pythonstudy.xyz/python/article/314-Static-%ED%8C%8C%EC%9D%BC)
##### Date 2020_11_22
---
 ### 1. Static 파일
> 웹 사이트는 일반적으로 자바스크립트, CSS, 이미지등 다양한 파일을 사용한다.
>
> 이러한 파일들을 Django에선 Static파일 이라 부르며 이 파일들을 체계적으로 관리하기 위해 일반적으로는 Django 프로젝트 홈 디렉토리(settings.py에서의 BASE_DIR) 밑에 "static"이라는 서브 폴더를 생성하여 그곳에 static파일을 넣는다.
>
> ```/static``` 폴더에 리소스별로 서브 폴더를 생성하여 static 파일을 관리하는 예. ![static-folder](./image/Django09/Django_09_1.png) 
> 
> static 폴더에 파일들을 넣고 사용하기 위해선 ```settings.py```파일에서 static 파일들을 찾는 경로를 나타내는 STATICFILES_DIRS라는 변수를 설정해야한다.
>
> BASE_DIR/static 폴더 하나를 지정한 예시(경로는 여러 개일 수도 있다.)
> ```Python
> STATIC_URL = '/static/'
> STATICFILES_DIRS = [
>     os.path.join(BASE_DIR, 'static'),
> ]
> 
> # 또는
> 
> STATIC_URL = '/static/'
> STATICFILES_DIRS = ( os.path.join('static'), )
> ```
>> 모든 Django App에 공통적으로 적용되는 Base템플릿을
>
### 2. Django App의 Static 폴더
> 
### 3. Static 파일 사용
>
### 4. collectstatic
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
