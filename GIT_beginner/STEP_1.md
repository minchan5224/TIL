#GIT Beginner
------------
>가장 처음 시작할때
```C
git config --global user.name "[your name]"
git config --global user.email "[your email]"
git init
git add [file name]
git commit -m "[commit messge]"
git branch -M main
git remote add origin [your git url]
git push -u origin main
```
>처음 사용 이후 사용시
```C
git add [file name]
git commit -m "[commit messge]"
git push -u origin main
```
>git 명령어
```C
git remote -v    : 연결되어있는 저장소 주소 확인
git remote remove origin    : 이전 remote 삭제시 사용
git clone [your git url]    : git저장소 내용 복사
git pull    : 로컬과 원격 저장소의 상태가 다르다면 동기화할때 사용 ex)push에서 오류 발생시 사용
```
>리눅스 명령어
```C
cd ..    :하위 디렉토리로 이동<br>
rm -r    :삭제 명령어<br>
```
