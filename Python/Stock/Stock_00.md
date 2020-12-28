# Stock Auto
##### Date 2020_12_28
---
오늘은 환경설정과 크레온 계좌를 만들었다.

PC를 바꾼뒤 구름만 사용하였기에 아직 VS코드를 설치하지 않아서 다시 깔아줬다.

크레온에서 제공하는 API를 이용해 간단한 예제를 확인, 실행 하였고

slack를 이용한 봇생성과 메시지 전송(POST)까지 진행 하였다.\

내일은 본격적으로 자동화 코드를 구현하고 

마무리 할 것이다.

```Python
import win32com.client
from slacker import Slacker

slack = Slacker('자신의 토큰을 입력한다.') # OAuth 토큰

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockMst.SetInputValue(0, 'A005930')   #종목 코드 - 삼성전자
objStockMst.BlockRequest()
 
# 현재가 통신 및 통신 에러 처리 
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()
 
# 현재가 정보 조회
name= objStockMst.GetHeaderValue(1)  # 종목명

offer = objStockMst.GetHeaderValue(16)  #매도호가

exFlag = objStockMst.GetHeaderValue(58) #예상체결가 구분 플래그
 
 
if (exFlag == ord('0')):
    Stock_Market_Status = "동시호가와 장중 이외의 시간"
elif (exFlag == ord('1')) :
    Stock_Market_Status = "동시호가 시간"
elif (exFlag == ord('2')):
    Stock_Market_Status = "장중 또는 장종료"
 
slack.chat.post_message('#stock','종목명 : '+name+'\n매도호가 : '+str(offer)+'\n시장 상태 : '+Stock_Market_Status)
```
위의 코드는 삼성전자의 현재가(매도호가)를 slack-bot를 이용해 채팅창으로 전송하는 코드이다.

```Python
import win32com.client
 
 
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥
 
 
print("거래소 종목코드", len(codeList))
for i, code in enumerate(codeList):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    print(i, code, secondCode, stdPrice, name)
 
print("코스닥 종목코드", len(codeList2))
for i, code in enumerate(codeList2):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    print(i, code, secondCode, stdPrice, name)
 
print("거래소 + 코스닥 종목코드 ",len(codeList) + len(codeList2))
```

> # 끝!
> # 참고한 곳 : [조코딩 : 파이썬 주식 투자 자동화](https://www.youtube.com/playlist?list=PLU9-uwewPMe0fB60VIMuKFV7gPDXmyOzp)
