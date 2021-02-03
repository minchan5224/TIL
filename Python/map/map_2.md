2021_02_02
---
> 일단 오늘은 지도 다루기 전
>
> 엑셀을 읽고 필요한 정보만 이용해 새로운 엑셀을 작성하고 
>
> 크기도 알맞게 조절을 하였다.
> 
> 이제 남은 일은 위도 경도 추출과 위도 경도를 이용한 마커 생성이다.
>
> 엑셀 화이팅..
> ```Python
> import pandas as pd
> import openpyxl
> from openpyxl.utils.dataframe import dataframe_to_rows
> 
> filename = "use_data.xls"
> df = pd.read_excel("경로"+filename, header=0, index_col=0)
> 
> use_datas = {}
> 
> name_list = []
> name_len = 0
> address_list = []
> address_len = 0
> co_existence = []
> open_time = []
> open_time_len = 0
> latitude = []
> latitude_len = 14
> hardness = []
> hardness_len = 14
> for i in range(1, len(df)):
>     name_list.append(str(df.iloc[i][0]))
>     if len(name_list[-1]) > name_len:
>         name_len = len(name_list[-1])
> 
>     if str(df.iloc[i][1]) == 'nan':
>         address_list.append(str(df.iloc[i][2]))
>     else :
>         address_list.append(str(df.iloc[i][1]))
>     if len(address_list[-1]) > address_len:
>         address_len = len(address_list[-1])
> 
>     if str(df.iloc[i][3]) == 'N' or str(df.iloc[i][3])== 'n':
>         co_existence.append('No')
>     else :
>         co_existence.append('Yes')
>     
>     open_time.append(str(df.iloc[i][15]))
>     if len(open_time[-1]) > open_time_len:
>         open_time_len = len(open_time[-1])
>     latitude.append(str(df.iloc[i][17]))
>     hardness.append(str(df.iloc[i][18]))
> 
> use_datas['col1'] = name_list
> use_datas[col2'] = address_list
> use_datas['col3'] = co_existence
> use_datas['col4'] = open_time
> use_datas['col5'] = latitude
> use_datas['co6l'] = hardness
> 
> df2 = pd.DataFrame(use_datas)
> 
> wb = openpyxl.Workbook() # 워크북 객체 생성
> ws = wb.create_sheet(index=0, title='Chart') # Chart라는 이름의 시트 생성
> wb.remove(wb['Sheet']) # 기본적으로 생성되어있던 Sheet 객체 삭제
> ws.column_dimensions['B'].width = name_len # 엑셀의 행 너비 조절하는 코드, 문자열중 가장 긴것의 길이로 이용함
> ws.column_dimensions['C'].width = address_len
> ws.column_dimensions['E'].width = open_time_len
> ws.column_dimensions['F'].width = latitude_len
> ws.column_dimensions['G'].width = hardness_len
> 
> for row in dataframe_to_rows(df2, index=True, header=True): # 행 단위로 반복문 수행 (년도별 매출, 영업이익, 자산총계 등)
>     if len(row) > 1:
>         ws.append(row) # Chart 시트에 행 단위로 하나식 추가.
> 
> wb.save("./google_map_pin/output/"+"파일명.확장자")
> ```
> 내일은 이걸 기반으로 위도 경도가 없는 것의 정보를 습득하고 마커를 찍는 과정을 할 것이다.
>
> 내일도 화이팅!
