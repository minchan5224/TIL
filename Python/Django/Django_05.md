# [Django 모델 API](http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API)
##### Date 2020_11_17
---
 ### 1. Django 모델 API
> 모델 클래스를 정의하게 되면  Django는 데이터를 추가/갱신하고 읽을 수 있는 다양한 DB API들을 자동으로 제공한다.
> - Django가 ORM서비스를 제공함에 따른것, DB를 편리하게 핸들링할 수 있다.
>
### 2. INSERT
> 데이터를 삽입하기 위해선 먼저 모델(테이블에 해당)로부터 객체를 생성하고, 그 객체의 save() 메서드를 호출하면 된다.
>
>> **Feedback() 생성자 안에 필요한 필드 값들을 채운 후 save() 메서드를 호출하는 코드**
>>
>> ```Python
>> from feedback.models import *
>> from datetime import datetime
>> 
>> # Feedback 객체 생성
>> fb = Feedback(name = '삥빵뽕', email = '삥빵뽕@test.com', comment='ㅋㅋ ㄹㅃㅃ', createDate=datetime.now())
>> 
>> # 새 객체 INSERT
>> fb.save()
>> ```
>>
>> save() 메서드가 호출되면 SQL의 INSERT가 생성, 실행되어 테이블에 데이터가 추가 된다.
>

### 3. SELECT
> Django는 기본으로 모든 Django클래스에 대해 "objects"라는 Manager(```django.db.models.Manager```)객체를 자동 추가한다.
> - objects의 이름은 변경 가능하다.
>
> Manager를 통해 특정 데이터를 필터링과 정렬이 가능하며 이외의 여러 기능을 사용할 수 있다.
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
