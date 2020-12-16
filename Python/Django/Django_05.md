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
> 데이터를 읽어오기 위해서는 Django 모델의 Manager("모델클래스.object")를 사용
> - "Feedback"이라는 모델의 경우 "Feedback.object"를 사용 (**객체명이 아닌 클래스명을 사용**)
>
> Django Model API에서 기본적으로 제공하는 여러 쿼리 메서드들이 있다.
>> 
>> Feedback 모델 클래스 기준으로 예를 든다.
>>
>> - all() : 테이블 데이터를 전부 가져오기 위해서는 Feedback.objects.all() 과 같이 all() 메서드를 사용
>> ```Python
>> # Feedback 테이블의 모든 데이타의 id와 name 컬럼을 출력예시 
>> for f in Feedback.objects.all():
>>     s += str(f.id) + ' : ' + f.name + '\n'
>> ```
>>
>> - get() : 하나의 Row만을 가져오기 위해서는 get() 메서드를 사용
>> ```Python
>> # Primary Key (일반적으로 id 컬럼)가 1인 row를 가져온다.
>> row = Feedback.objects.get(pk=1)
>> print(row.name)
>> ```
>>
>> - filter() : 특정 조건에 맞는 Row들을 가져오기 위해서는 filter() 메서드를 사용 
>> ```Python
>> # name 필드가 '삥' 인 데이타만 가져온다.
>> rows = Feedback.objects.filter(name='삥')
>> ```
>>
>> - exclude() : 특정 조건을 제외한 나머지 Row들을 가져오기 위해서는 exclude() 메서드를 사용 
>> ```Python
>> # name 필드가 '빵'이 아닌 데이터만 가져온다.
>> rows = Feedback.objects.exclude(name='빵')
>> ```
>>
>> - count() : 데이터의 갯수(row 수)를 세기 위해 count() 메서드를 사용한다. ```n = Feedback.objects.count()```
>>
>> - order_by() : 데이타를 키에 따라 정렬하기 위해 order_by() 메서드를 사용, order_by() 안에는 정렬 키를 나열할 수 있다(앞에 -가 붙으면 내림차순)
>> ```Python
>> # id를 기준으로 올림차순, createDate로 내림차순으로 정렬
>> rows = Feedback.objects.order_by('id', '-createData')
>> ```
>>
>> - distinct() : 중복된 값은 하나로만 표시하기 위해 distinct() 메서드를 사용(SQL의 SELECT DISTINCT 와 같은 효과)
>> ```Python
>> # '뽕'필드가 중복되는 경우 한번만 표시하게 된다.
>> rows = Feedback.objects.distinct('뽕')
>> ```
>>
>> - first() : 데이타들 중 처음에 있는 row만을 리턴 
>> ```Python
>> # '😍'필드로 정렬했을 때 처음 row를 리턴한다.
>> rows = Feedback.objects.order_by('😍').first()
>> ```
>>
>> - last() : 데이타들 중 마지막에 있는 row만을 리턴
>> ```Python 
>> # '👻'필드로 정렬했을 때 마지막 row를 리턴
>> rows = Feedback.objects.order_by('👻').last()
>> ```
>>
> 위의 쿼리 메서드들은 실제 데이터 결과를 리턴하기 보다 쿼리 표현식([QuerySet](https://lqez.github.io/blog/django-queryset-basic.html))을 리턴
> - 여러 메서드들을 체인처럼 연결하여 사용할 수 있다.
>> 여러 체인으로 연결되어 리턴된 쿼리가 해석되어 DB에 실제 하나의 쿼리를 보낸다.
>> 
>> ```Python
>> # 여러 메서드들을 사용하여 체인으로 연결
>> row = Feedback.objects.filter(name='Kim').order_by('-id').first()
>> ```
>
### 4. UPDATE
> 데이터를 수정하기 위해 먼저 수정할 Row 객체를 얻은 후 변결할 필드를 수정한다.
>
> 마지막에 save()메서드를 호출하면 SQL의 UPDATE가 실행되어 테이블에 데이터가 갱신된다.
>
>> ```Python
>> # id가 1인 Feedback 객체에 이름을 변경하는 코드
>> fb = Feedback.objects.get(pk=1)
>> fb.name = '꿩'
>> fb.save()
>> ```
>
### 5. DELETE
> 데이터를 삭제하기 위해 먼저 수정할 Row 객체를 얻은 후 얻은 후 delete() 메서드를 호출한다.
>> ```Python
>> #  id가 2인 Feedback 객체를 삭제하는 코드
>> fb = Feedback.objects.get(pk=2)
>> fb.delete()
>> ```
>
> # 끝!  
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
