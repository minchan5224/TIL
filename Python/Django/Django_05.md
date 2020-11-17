# [DB 설정과 Migration](http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API)
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
>> fb = Feedback(name = 'Kim', email = 'kim@test.com', comment='Hi', createDate=datetime.now())
>> 
>> # 새 객체 INSERT
>> fb.save()
>> ```
>>
>> save() 메서드가 호출되면 SQL의 INSERT가 생성, 실행되어 테이블에 데이터가 추가 된다.
>

### 3. DB 설정
> 
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
