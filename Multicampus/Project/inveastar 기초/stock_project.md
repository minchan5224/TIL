### 멀티캠퍼스 인공지능 자연어처리[NLP]기반 기업 데이터 분석.
- 6주차 4~5 (6/17, 18)
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
>> ```
