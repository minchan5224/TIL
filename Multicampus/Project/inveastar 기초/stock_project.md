### 멀티캠퍼스 인공지능 자연어처리[NLP]기반 기업 데이터 분석.
- 6주차 4~7 (6/17, 18, 19, 20)
---
> 상장 회사 코드이용 네이버 주식 크롤링.(read_html 이용해 웹에있는 파일 바로 읽어옴)
> 
> 총 2400여개 회사의 100페이지(1000일치 주가 정보)정보 획득
> 
> DB(mysql) 저장.(to_sql이용)
> 
> 크롤링 -> DB화.
>
> 최근 업데이트일 지정후 업데이트 기능 학습.
> - 사용한 라이브러리, 프레임워크
>> ```Python
>> import pandas as pd
>> from bs4 import BeautifulSoup
>> from sqlalchemy import create_engine
>> import re
>> import pymysql, calendar
>> import requests
>> ```
----
> 18일엔 어제 작성했던 코드 class로 바꿔줌. ide도 스파이더로 바꿈.
> - 사용한 라이브러리, 프레임워크
>> ```Python
>> import pandas as pd
>> from bs4 import BeautifulSoup
>> from sqlalchemy import create_engine
>> import re
>> import pymysql, calendar
>> import requests
>> from threading import Timer
>> ```
> timer이용해 매일 오후 5시(주식 장 마감 후)에 데이터 크롤링하여 데이터 갱신(업데이트)
> 
> 작은 실습으론 영화예매 코드 클래스로 작성하는 것 했음
>
> 사실 클래스를 많이 안써봐서 보면 이해는 했지만 막상 만들기는 좀 그랬었는데 계속 하다보니 확실히 뭔지 느낌이옴
>
> 만드는 것도 크게 어렵지는 않아서 다행.
>  
> 그리고 클래스 기초 다시 수업.
> - 간단한 계산기..
>> ```Python
>> class FourCal:
>>     def __init__(self, first, second):
>>         self.first = first
>>         self.second = second
>>         
>>     def setdata(self, first, second):
>>         self.first = first
>>         self.second = second
>>     
>>     def add(self):
>>         result = self.first + self.second
>>         return result
>>     
>>     def sub(self):
>>         result = self.first - self.second
>>         return result
>>     
>>     def mul(self):
>>         result = self.first * self.second
>>         return result
>>     
>>     def div(self):
>>         result = self.first / self.second
>>         return result
>> 
>> class MoreFourCal(FourCal):# 상속받음
>>     def pow(self):
>>         result = self.first ** self.second
>>         return result
>> 
>> class SafeFourCal(FourCal):# 상속받음
>>     def div(self): # 부모 클래스가 가지고있던 함수를 재정의함(메서드 오버라이딩)
>>         if self.second != 0:
>>             result = self.first / self.second
>>         else :
>>             result = 0
>>         return result
>> ```
---
> 19일엔 필요한 내용인 1000일치 데이터 2449개 전부 db에 저장(대충 전체 크기는 1000 * 2449)
>
> 사용자가 원하는 정보로 db에서 조회하는 기능 구현.
> 
> 원래는 종목코드 혹은 종목명 그리고 시작 날짜 끝 날짜를 입력받아 데이터 프레임을 전달하는 클래스와 함수 구현이였지만
>
> 전부 구현하고 사용자가 db에 있는 회사의 이름과 코드를 조회하며 자신이 검색하고자하는 회사를 직접 골라서 원하는 정보를 제공하는 클래스와 함수또한 구현.
> 
> 이제 오류처리만 마무리하면 전부 끝인것같다.
> 
---
20일.
> 오류처리 끝.
>
> 코테봤습니다. 요기요.. 문제자체는 어렵지 않았지만 내가 짠 코드가 가장 효율적이였는지, 정확한지 충분히 고려하지 못한것같아 찝찝..
> 
> 어제 작성한 코드 정리. import했을때가 아닌 해당 .py파일에서 실행했을때만 테스트 가능하도록 테스트용 함수 작성.
>
> 전일비(diff) 에 대한 컬럼을 생성 해야할지 아니면 호출해서 전일비를 구할지 아직 고민중.. 
> - 둘다 구현 자체는 쉽지만 어떻게 사용하는게 더 좋은지 아직 잘 모르겠어서.. db에 컬럼을 새로 생성하고 하는게 좋을것 같긴하지만..
> 
> 그리고 지금 구현해둔 클래스로는 배포, 사용 둘다 부적합한것 같다 적합한 인터페이스? 를 PYQT를 이용해 만들어서 사용한다면 좀더 좋을 것 같아서 관련 기능 고민중
> 
> 그래프를 출력해준다거나 2개 그래프 비교 해준다거나 그런것??
>
> 내일도 공부..
