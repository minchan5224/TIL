### 파이썬으로 PDF파일의 TEXT수집하기.
> 2021/1/22
>
> PDF파일의 TEXT를 수집한다.
---
> 이것도 은근히 사용할 일이 많을 것이라 생각한다.
>
> 뭐.. 논문이나.. PDF로 저장한 이력서? 포트폴리오? 에서 회사에서 원하는 키워드가 적혀있는지 판단해 서류를 검증?
>
> 음... 더 다양한것이 지금은 생각이 안나지만 사용할 곳은 많을 것으로 생각된다.
>
> ```Python
> # pip install PyPDF2, pip install pdfminer.six 를 적힌 순서대로 하라고함.. (PyPDF2먼저, pdfminer.six는 그다음)
> import PyPDF2
> from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
> from pdfminer.converter import TextConverter
> from pdfminer.layout import LAParams
> from pdfminer.pdfpage import PDFPage
> from io import StringIO
> 
> # PyPDF2로 페이지 수 계산
> filename = "north_korea_economic_growth.pdf"
> fp = open("../data/"+filename, 'rb')
> total_pages = PyPDF2.PdfFileReader(fp).numPages
> print(total_pages)
> fp.close()
> 
> # pdfminer로 페이지별 텍스트 수집
> page_text = {} # 각 페이지 번호를 key로 사용하고 텍스트를 value 로 저장할 딕셔너리
> for page_no in range(total_pages):
>     rsrcmgr = PDFResourceManager() # pdf리소스 매니저 객체
>     retstr = StringIO() # str을 파일처럼 정리, pdf파일 내용을 담는다.
>     codec = 'utf-8'
>     laparms = LAParams() # 분석을 위한 파라미터 설정
>     device = TextConverter(rsrcmgr, retstr, codec = codec, laparams=laparms)
>     fp = open("../data/"+filename, 'rb')
>     password = None
>     maxpages = 0
>     interpreter = PDFPageInterpreter(rsrcmgr, device) # PDF 인터프리터 생성.
>     caching = True
>     pagenos = [page_no]
>     
>     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
>                                   caching=caching, check_extractable=True):
>         # PDFMiner 라이브러리의 PDFPage 모듈을 이용해 각 페이지에서 텍스트 추출
>         # get_pages()함수에 사용할 변수는 위에서 만들어둔 값들을 사용
>         
>         interpreter.process_page(page) # PDF인터프리터(번역기) 객체에 process_page() 메소드 적용함
>         # 각 페이지의 문자열이 파일 형태로 변환되어 StringIO(=retstr) 객체로 저장
>         
>         
>     page_text[page_no] = retstr.getvalue()
>     # StringIO(=retstr)의 값을 value에 저장한다 key는 page_no 다.
>     
>     
>     fp.close()
>     device.close()
>     retstr.close()
>     # 사용 끝났으니 파일, 디바이스(텍스트변환기), StringIO객체를 닫는다.
> ```
> 실행해보니
>
> \n , \t등 공백을 처리하면 더 깔끔할것 같다.
>
> 사용할 곳이 몇가지 더 생각났다.
>
> 정부에서 발행한 통계문서? , 계획서? 등의 텍스트를 분석할때 수집하기 위한 용도로 사용하면 편리할것이다.
>
> 오늘은 면허 필기도 봤습니다. 
>
> 면허 따야하는뎅..
>
> 화이팅...
