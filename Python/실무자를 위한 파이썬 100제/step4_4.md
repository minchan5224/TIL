### 파이썬으로 엑셀에 이미지 삽입, 수집한 정보 엑셀에 저장
> 2021/1/29
>
> 엑셀을 조작한다!!!
---
> 엑셀에 이미지를 첨부 할 수 있다?
> ```Python
> import openpyxl
> from openpyxl.drawing.image import Image
> 
> image_name = "엑셀에 삽입할 이미지 명.확장자" # 사용할 이미지 이름
> image_path = "../output/" # 사용할 이미지 경로
> 
> img = Image(image_path+image_name) # 이미지 경로이용해 이미지 객체 생성.
> 
> img.width = img.width//10 # 이미지가 너무 커서 1/10로 줄였음
> img.height = img.height//10 # 이미지가 너무 커서 1/10로 줄였음
> 
> wb = openpyxl.Workbook()
> ws = wb.create_sheet(index=0, title="Image") # 새 시트 생성, 이름은 Image
> wb.remove(wb['Sheet']) # 필요없는 시트 삭제
> 
> ws['A1'] = "Google Trend intel and amd" # A1에 이미지의 이름을 적는다.
> ws.add_image(img, 'B3') # 이미지의 왼쪽 위 모서리(시작위치)는 B3이다.
> 
> wb.save("경로/엑셀파일_이름.xlsx") # 저장
> ```
> 저장된 내용은 아래 사진과 같다.
> 
> <img src="./image/step4_4/insert_image.png">
>
> 이미지 삽입은 여기까지..
>
> 이외에도 전부터 몇번 실습 해봤던 크롤링한 자료를 엑셀로 정리하는 것은.
>
>> 1. 크롤링한 정보를 딕셔너리 형 변수에 담는다.
>> 
>> 2. Pandas를 이용해 데이터프레임에 옮겨 담는다.
>>
>> 3. 해당 데이터프레임을 엑셀로 저장한다.
>
> 위의 3가지 과정을 통해 가능하다.
>
> 내일도 좋은하루!
