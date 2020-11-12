# Django 프로젝트
##### Date 2020_11_12
---
 ### 1. Django 프로젝트
> Django에서 새로운 웹 프로젝트를 만들기 위해서는 django-admin.py라는 Django 관리자 모듈을 사용한다.
>
> 가상환경을 활성화 하고, 프로젝트를 만들 디렉토리로 이동한다.
>
> 아래 예제와 같이 "django-admin startproject [프로젝트명]"을 실행해 새 프로젝트를 생성한다.
>
> 예제에서는 "~/pysrc/myweb"폴더에 새 웹 프로젝트를 만든다.
>
>> ```
>> (venv1) ~$ cd ~/pysrc
>> (venv1) ~/pysrc $ django-admin startproject myweb
>>
>> # Windows일때
>> # (venv1) C:\PySrc> C:\PyEnv\venv1\Scripts\django-admin.exe startproject myweb
>> ```
>
> 위 예제의 명령은 새 프로젝트를 myweb 라는 서브폴더에 생성하고, myweb안에 아래 그림과 같이 몇개의 파일들을 생성한다.
>
> ![이미지이름](./이미지가 있는 폴더/이미지이름.형식)
>
> manage.py 는 웹 프로젝트를 개발, 관리하는데 필요한 여러 기능을 제공한다.
>
> myweb 라는 서브폴더 하위에 4개의 파이썬 파일이 존재한다.
> - settings.py : 웹 프로젝트의 셋팅을 설정하는 파일
> - urls.py : URL 매핑을 위한 파일
>
### 2. Django 서버 실행
> 기본적으로 생성된 웹 프로젝트(myweb)를 먼저 실행해 본다.
>
> 웹 프로젝트로 부터 웹 서비스를 시작하기 위해선 **python manage.py runserver**를 실행하면 된다.
> - 리눅스 혹은 Mac의 경우
>> ```
>> (venv1) ~/pysrc/myweb $ python3 manage.py runserver
>> 혹은
>> (venv1) ~/pysrc/myweb $ ./manage.py runserver
>> ```
> - Windows의 경우
>> ```
>> (venv1) C:\PySrc\myweb> python manage.py runserver
>> ```
>
> 명령들로 Django Development Server가 시작되면 아래와 같은 메시지가 풀력된다.
>
> 메시지의 중간에서 웹 서버의 URL주소(```"http://127.0.0.1:8000"```)를 찾을 수 있으며 웹 브라우저에 해당 주소(localhost)를 이용해 접속하면 웹 페이지를 볼 수 있다.
>
> 웹 브라우저에 표시되는 웹페이지는 Django프레임워크 에서 기본적으로 보여주는 웹 페이지다.
>
> ![이미지이름](./이미지가 있는 폴더/이미지이름.형식)
>
> 혹시라도 8000번 포트가 사용중이면 runserver 뒤에 원하는 [다른 포트 번호](https://webdir.tistory.com/124)를 지정하여 사용하여도 된다.
>> ```
>> python manage.py runserver [원하는 포트 번호]
>> ```
> 웹서버를 정지 하기 위해선 "**manage.py runserver**" 하였던 **터미널** 혹은 **CMD** 창에서 **Ctrl + C**를 누른다.

> # 끝!
>
