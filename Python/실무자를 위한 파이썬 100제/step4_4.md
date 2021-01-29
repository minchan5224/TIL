### 파이썬으로 엑셀 행/열 위치 변경(DataFrame.T), 차트 그리기.
> 2021/1/24
>
> 엑셀을 조작한다!
---
> 이것도 은근히 사용할 일이 많을 것이라 생각한다.
>
> 뭐.. 논문이나.. PDF로 저장한 이력서? 포트폴리오? 에서 회사에서 원하는 키워드가 적혀있는지 판단해 서류를 검증?
>
> 음... 더 다양한것이 지금은 생각이 안나지만 사용할 곳은 많을 것으로 생각된다.
>
> ```Python
> import openpyxl # 엑셀 사용을 위해
> from openpyxl.chart import BarChart, Reference # 엑셀 차트 사용을 위해
> from openpyxl.utils.dataframe import dataframe_to_rows # 데이터프레임의 행(가로) 단위로 반복문을 수행할때 사용
> 
> import pandas as pd # 엑셀을 읽어올때 사용
> 
> filename = "financials.xlsx"
> 
> df = pd.read_excel("../data/"+filename, header=0, index_col=0)
> tdf = df.T # 행, 열의 위치를 바꿔 저장한다. (연도를 x축에 반영하기 위해)
> 
> wb = openpyxl.Workbook() # 워크북 객체 생성
> ws = wb.create_sheet(index=0, title='Chart') # Chart라는 이름의 시트 생성
> wb.remove(wb['Sheet']) # 기본적으로 생성되어있던 Sheet 객체 삭제
> 
> for row in dataframe_to_rows(tdf, index=True, header=True): # 행 단위로 반복문 수행 (년도별 매출, 영업이익, 자산총계 등)
>     if len(row) > 1:
>         ws.append(row) # Chart 시트에 행 단위로 하나식 추가.
>           
> chart = BarChart() # 객체 생성
> chart.type = "col" # col은 수직 막대 그래프. bar을 이용하면 수평 막대 그래프
> chart.style = 10 # 스타일 지정
> chart.title = "매출액/영업이익" # 타이틀 설정
> chart.y_axis.title = "금액(억원)" # y축 타이틀
> chart.x_axis.title = "연도" # x축 타이틀
> 
> # Reference클래스는 시트에서 참조하는 셀의 영역을 지정할 때 사용
> data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=5) # 막대 그래프에 표시할 데이터 범위를 지정하고 변수 data에 저장 
> cats = Reference(ws, min_col=1, min_row=2, max_row=5) # x 축에 사용할 셀의 범위를 지정하여 cats변수에 저장.
> # 차트 객체에 데이터를 담는다.
> chart.add_data(data, titles_from_data=True) # 데이터 값 전달
> chart.set_categories(cats) # x축 범위 값을 입력해 x축 값을 범주로 표시.
> chart.shape = 4
> ws.add_chart(chart, "A8") # A8셀에 차트 삽입.
> 
> wb.save(os.path.join("../output/"+"financials_barchart.xlsx")) # 엑셀 저장.
> ```
> 위에서 dt.T가 그냥 가장 신기했다.
>
> 너무 짧아서 그런가... 
>
> 해당 문법의 자세한 설명을 찾아봤다 [[보기](https://pandas.pydata.org/pandas-docs/version/0.25.0/reference/api/pandas.DataFrame.T.html)] 
>
> 오늘은 여기까지 ...
>
> 내일도 좋은하루!
