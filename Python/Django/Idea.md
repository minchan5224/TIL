> 생각 정리
---
> 1. 지하철 챗봇
>> #### 공공데이터 포털에서 제공받는 Data를 내 Server에서 가지고 있게 한다.
>> - 응답속도를 빠르게 하기 위해
>>
>> #### 어떤 방식으로 Data를 저장 할 것인가. 
>> - Nosql을 사용할 것인가 RDBMS를 사용할 것인가.(Json을 쓸지 Csv를 쓸지도 포함)
>> 
>> #### 요청한 시점의 시간을 통해서만 시간표를 검색하는 것이 아닌 사용자가 지정한 시간도 검색 가능하게
>> - 어떤 방식으로 시간을 전달 받을 것인가(메시지로 받겠지만 2개 이상의 메시지로 받을 것인지 1개의 메시지로 처리 할 것인지)
>> 
>> #### 시간표 시간으 정확성을 더 높이기 위해선 무슨 방법이 있을까?
>> - 네이버, 다음의 시간표 정보를 크롤링 할 것인지
>> 
>> - 크롤링 하기 위해선 어떤 방식으로 해야 할 것인지
>> 
>> - robots.txt에서 크롤링을 허용 하지 않을 땐 어떻게 할 것인지.
