### 파이썬으로 워드파일 작성하기.
> 2021/1/20
>
> 필드를 이용해 워드의 내용을 자동으로 채운다! 
---
> 이건 쫌 많이 유용하다고 생각한다.
>
> 뭐 고객에게 주문 영수증 발급? 등 비슷한 문서작업을 자동으로 처리하는것이 가능하다.
>
> 하지만 모든 문서작업이 그렇듯 사용할 양식은 직접 구성하고 필드를 배치해야한다.
>
> 그 다음부턴 엑셀이든 json이든 데이터를 이용해 해당 파일을 알맞게 작성이 가능해진다.
>
> ```Python
> from mailmerge import MailMerge # word파일을 사용하기 위해
> from datetime import datetime as dt # 현재 시간을 받오기 위해
> import pandas as pd # 엑셀을 읽어와 데이터프레임 단위로 사용하기 위해
> 
> template_filename = 'fax_cover_template.docx' # 사용할 word 파일 명
> document = MailMerge("../data/"+template_filename) # word 파일 양식을 읽어온다.
> 
> respondents_filename = 'fax_respondents_list.xlsx' # 데이터를 이용할 엑셀 명
> respondents = pd.read_excel("../data/"+respondents_filename) # 사용할 엑셀을 읽어온다.
> 
> respondents_list = [] # 엑셀에서 읽어온 데이터를 딕셔너리로 옮겨담은뒤 순서대로 적재할 리스트.
> 
> today = '%s년 %s월 %s일'%(dt.now().year, dt.now().month, dt.now().day) # 현재 시간 사용 양식에 맞게 획득
> 
> for index in respondents.index:
>     new_respondent = {} # 임시로 저정할 딕셔너리
>     new_respondent['name'] = respondents.loc[index, 'name'] # 각각의 엑셀 필드별 데이터를 적절한 딕셔너리 key에 적재한다.
>     new_respondent['fax'] = respondents.loc[index, 'fax']
>     new_respondent['phone'] = respondents.loc[index, 'phone']
>     new_respondent['date'] = today
>     new_respondent['title'] = respondents.loc[index, 'title']
>     new_respondent['memo'] = respondents.loc[index, 'memo']
>     respondents_list.append(new_respondent) # 완성된 딕셔너리를 리스트에 적재한다.
>     
> document.merge_templates(respondents_list, separator='page_break') # 정리된 리스트를 이용해 word파일을 작성한다.
> output_filename = 'fax_dover_multi_pages_excel_data.docx' # 내보낼 워드 파일명 지정.
> document.write("../output/"+output_filename)# 작성한 word파일을 저장한다.
> ```
>
> 실습 과정은 워드파일에 하나의 데이터를 작성하는 것
>
> 여러 페이지를 작성하는것
>
> 엑셀에 있는 데이터를 이용해 작성하는 것 가지 진행 하였다.
>
> 내일은 엑셀을 더 깊게 사용하는 것을 실습 할 것이다.
>
> 화이팅!
