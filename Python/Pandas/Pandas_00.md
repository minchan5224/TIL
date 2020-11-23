# [Pandas 란](http://pythonstudy.xyz/python/article/408-pandas-%EB%8D%B0%EC%9D%B4%ED%83%80-%EB%B6%84%EC%84%9D)
##### Date 2020_11_23
---
### 1. pandas 개요
> 데이타 분석(Data Analysis)을 위해 널리 사용되는 파이썬 라이브러리 패키지다.
>
> 아나콘다에선 pandas를 기본적으로 라이브러리로 제공 한다. 하지만 아나콘다를 사용하지 않는다면 따로 설치 해야한다(pip install pandas)
>
### 1. pandas 사용법
> pandas는 라이브러리 임으로 사용하기 위해선 ```import```해야한다. 주로 ```import pandas as pd```형식을 사용한다.
>
> pandas는 크게 3가지의 자료구조를 지원한다. 1차원의 Series 2차원의 DataFrame 3차원의 Panel이다.
> 
> #### Series
>> Series는 1차원 구조이며 배열/리스트과 같은 일련의 시퀀스 데이터를 받아들인다.
>>
>> 별도의 인덱스 레이블을 지정하지 않는다면 자동으로 0부터 시작하는 정수(디폴트) 인덱스를 사용한다.
>> ```Python
>> data = [1, 3, 5, 7, 9]
>> s = pd.Series(data)
>> ```
>> ![pandas-series](./image/Pandas_00/Pandas_00_1.png)
>
> #### DataFrame
>> 2차원 구조인 DataFrame은 행과 열이 테이블(표)데이터를 받아들인다.
>>
>> 열(column)을 dict의 키로, 행(row)을 dict의 값으로 한 Dictionary데이터를  pd.DataFrame()를 이용해 Data Frame 자료구조로 변환한다.
>> ```Python
>> data = {
>>     'year': [2016, 2017, 2018],
>>     'GDP rate': [2.8, 3.1, 3.0],
>>     'GDP': ['1.637M', '1.73M', '1.83M']
>> }
>> 
>> df = pd.DataFrame(data)
>> ```
>> ![pandas-dataframe](./image/Pandas_00/Pandas_00_2.png)
>
> #### Panel
>> Axis 0 (items), Axis 1 (major_axis), Axis 2 (minor_axis) 등 3개의 축을 가지고 있다.
>>
>> Axis 0은 그 한 요소가 2차원의 DataFrame에 해당한다.
>>
>> Axis 1은 DataFrame의 행(row)에 해당한다.
>>
>> Axis 2는 DataFrame의 열(column)에 해당한다.
>
### 3. 데이타 엑세스
> 다양한 방법을 통해 데이터를 엑세스할 수 있다.
>
> 가장 간단한 방식으로 pandas 자료구조에 대해 인덱싱 혹은 속성(Attribute)을 사용하는 방법이 있다.
>
> 위에서 생성한 DataFrame인 df을 이용
>> ```df['year']``` 혹은 ```df.year``` DB에서 select year과 동일.
>> ![pandas-data-access_1](./image/Pandas_00/Pandas_00_3.png)
>>
>> ```df[df['year'] > 2016]``` 2016보다 큰 년도만 고른다.
>> ![pandas-data-access_2](./image/Pandas_00/Pandas_00_4.png)
>> 
>> ```Python
>> sum = df['GDP rate'].sum()
>> avg = df['GDP rate'].mean()
>> print(sun, avg)
>> # GDP rate의 합을 sum에 GDP rate의 평균을 avg에 담아서 출력.
>> ```
>> ![pandas-data-access_2](./image/Pandas_00/Pandas_00_5.png)
>>
>> ```df.describe()``` 기본적인 통계치 모두 표시
>> ![pandas-data-access_2](./image/Pandas_00/Pandas_00_6.png)
>
> 
### 4. 외부 데이타 읽고 쓰기
> CSV 파일, 텍스트 파일, 엑셀 파일, SQL 데이타베이스, HDF5 포맷 등 다양한 외부 리소스에 데이타를 읽고 쓸 수 있는 기능을 제공한다.
>
> 가장 많이들 궁금해 하는 엑셀의 경우를 예로 들겠다.
>
> ```Python
> df = pd.read_excel('파일경로/파일명.xlsx')
> ```
> 변수명이 df인 이유는 DataFrame형식이기때문이다.
> 
> 읽을 파일의 확장자에 따라 read_['여기'] 를 수정하여 사용하면 된다.
>
> 엑셀 형식으로 저장하기 위해선 pip install을 통해 [엑셀쓰기를 위한 패키지](https://hodubab.tistory.com/92)를 다운 받아야한다.
>
> # 끝!
> # 참고한 블로그 : [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/)
