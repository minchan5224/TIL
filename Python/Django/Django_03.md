# [Django Model](http://pythonstudy.xyz/python/article/308-Django-%EB%AA%A8%EB%8D%B8-Model)
##### Date 2020_11_14
---
 ### 1. Django Model
> Django에서의 Model은 데이터 서비스를 제공하는 Layer이다.
> - Model은 각 Django App안에 기본적으로 생성되는 models.py 모듈 안에 정의한다.
>
> - models.py 모듈 안에 하나 이상의 모델 클래스를 정의할 수 있다.
>
> - 하나의 오델 클래스는 DB에서 하나의 테이블에 해당된다.
>
>> 아래의 그림에선 feedback라는 새로운 Django App을 생성 하였다.
>>
>> feedback App 폴더 안에 있는 models.py 파일에 새로운 모델 클래스를 추가 하였다.
>> ![create-model](./image/Django_03_2.png)
>>
>> Django 모델은 "django.db.models.Model"에서 파생된 클래스이며 모델의 필드는 클래스의 Attribute로 표현되며 테이블의 컬럼에 해당한다.
>>
>> 위의 그림에서 Feedback라는 클래스가 models.Model의 파생클래스 이며 클래스 안에 4개의 클래스 변수(혹 Class Attribute)가 있다.
>>
>> 만약 Primary Key가 지정되지 않는다면 모델에 Primary Key 역할을 하는 id필드가 자동으로 추가되고 DB테이블 생성시 자동으로 id 컬럼이 생성된다.
>>
>
### 2. 필드 타입
> 
>
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
