# Multicampus Projects
---
#### 인공지능 자연어처리[NLP]기반 기업 데이터 분석 과정

#### [구내식당 식수 인원 예측 AI 경진대회](https://dacon.io/competitions/official/235743/overview/description)
---
> colab 일단은 colab에서 진행.
>
> ### 1. 드라이브 마운트
> 
> #### 2. 설정(import, 폰트적용, 데이터 로드)
> 
> 폰트 설치, matplotlib업데이트
>> ```
>> pip install matplotlib -U # 업데이트
>> 
>> !sudo apt-get install -y fonts-nanum # 한글 글꼴 다운로드
>> !sudo fc-cache -fv # 캐시 삭제.
>> !rm ~/.cache/matplotlib -rf 
>> ```
>>
>> ```
>> import numpy as np 
>> import pandas as pd
>> import matplotlib.pyplot as plt
>> import seaborn as sns
>> import warnings # 자잘한 경고 메시지(오류 말고) 안나오게.
>> 
>> warnings.filterwarnings(action='ignore') # 경고 메시지 출력 안함.
>> 
>> plt.rcParams['font.family']=['NanumGothic', 'sans-serif'] # 한글 폰트 적용
>> plt.rcParams['axes.unicode_minus'] = False
>> 
>> train = pd.read_csv('/content/drive/MyDrive/Dacon/data/train.csv') # 드라이브 마운트 하고 train data 읽어옴
>> test = pd.read_csv('/content/drive/MyDrive/Dacon/data/test.csv') # 드라이브 마운트 하고 test data 읽어옴
>> ```
>
> #### 3. 데이터 정제
> drop
>> ```
>> # 일자는 년-월-일 로 구성된다. 사실 월,일 만 필요하다고 생각한다. 365일 마다 순환하는 느낌으로 하는게 좋을것 같으니까. 
>> train['월'] = pd.DatetimeIndex(train['일자']).month # 리스트로 반환, 리스트는 시리즈니까 바로 담는거 가능. 아래도 마찬가지.
>> test['월'] = pd.DatetimeIndex(test['일자']).month
>> 
>> train['일'] = pd.DatetimeIndex(train['일자']).day
>> test['일'] = pd.DatetimeIndex(test['일자']).day
>> 
>> train = train.drop(drops, axis=1)
>> test = test.drop(drops, axis=1)
>> # 월~금요일 은 object즉 str형이라 모델에 넣을 수 없으니 인코딩을 진행해야한다. 일단은 원핫 말고 그냥 카테고라이즈만.
>> def day_to_num(d): # .apply() 할때 사용할 함수 선언, 요일을 숫자로
>>     if d == '월':
>>         return 1
>>     elif d == '화':
>>         return 2
>>     elif d == '수':
>>         return 3
>>     elif d == '목':
>>         return 4
>>     elif d == '금':
>>         return 5
>>  
>> train['요일'] = train['요일'].apply(day_to_num)
>> test['요일'] = test['요일'].apply(day_to_num)
>> 
>> # 필요없는거 drop
>> d_name = ['일자', '조식메뉴', '중식메뉴', '석식메뉴']
>> train = train.drop(d_name, axis=1)
>> test = test.drop(d_name, axis=1)
>> ```
