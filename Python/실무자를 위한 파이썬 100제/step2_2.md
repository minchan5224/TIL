### 오랜만에 konlpy!
#### 집안일...등등 오늘은 너무 시간이 없었지만.. 지금이라도 끝내고 겨우 올려요
> 2021/1/1
---
> 가장 편하게? 생각하는 신년사를 위주로 해봤습니다.
>
> 트럼트 대통령 취임사는 영어로 작성된 것이기 때문에 wordcloud를 사용할때 명사의 출현 횟수를 자동으로 계산해주지만
>
> 한글은..안해주니깐.. konlpy로 한번 가공? 해줘야한다.
>
> 일단 ```engin = Hannanum()``` 을 이용했습니다.
>
> 윈도우 환경이라..Mecab Class를 못써서..
>
> 명사만 추출하도록 ```"변수명" = engin.nouns(text)``` 코드를 작성하고
>
> 다음으로 저는 ```[re.sub(r"[,‘’'\-_[\] ]", "", n) for n in nouns if len(n) > 1]```를 이용 필요없는 특수문자를 제거 했습니다.
>
> 그리고 collections의 Counter를 이용해 각각의 명사가 몇번씩 등장하였는지 구합니다.
>
> ```"결과를 담을 변수명" = Counter("등장 횟수 구할 변수를 담은것")``` 과 같이 사용합니다.
>
> 음 그리곤 워드클라우드를 작성하면 끝입니다.
>
```Python
"워드클라우드에 담을 딕셔너리 형식 변수" = dict("위에서 사용한 결과를 담은 변수명".most_common("구할 갯수"))
wordcloud = WordCloud(font_path=('폰트 경로'),
                      background_color='white',
                      width=1200,
                      height=800).generate_from_frequencies("앞에서 구한 워드클라우드에 담을 딕셔너리 형식 변수")

fig = plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

plt.savefig('저장할 경로/파일명.확장자')
```
>
> 위와 같이 한다면 당신도 워드크라우드를 사용할 수 있습니다. 하핳
