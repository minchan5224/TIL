작정하고 장고 46강 - Why Docker? 서비스 배포로 들어가며

https://www.youtube.com/watch?v=PqMKZ-taMvI&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=46

이제부턴 장고보다는 도커에 초점을 맞추어 배포를 어떻게 더 쉽게 하는지, 유지보수를 더 쉽게 하는지.

지금까지 장고 내부의 여러 app들을 만들었다.
 - Django container를 만들기 위해.

Django container를 만든것을 기반으로 Docker안에 하나의 컨테이너로서 소스들을 넣을 것이다.

이 도커 시스템을 VULTR라는 가상 서버 시스템을 빌려 서비스 할것이다.(나는 아직 구름 사용)

왜 도커를 쓰는가.
- Docker is Everywhere : 이미 많은 곳에서 사용중이며 필수적인 요소로 자리잡고있다.

- Docker is FAST : 빠르다!

Docker란?
- 기존과 다른 가상화(Virtualization) 기반(기존 가상화에 비해 속도가 매우 빠르다.)
>> RedHat과 AWS에서는 아래 그림과 같이 표현한다.
[]()
- 컨테이너 개념을 이용해 일반 OS를 사용하는 것과 큰 차이가 없을 정도로 속도가 빨라졌다.

- 같은 환경의 격리된 컨테이너를 사용할 수 있다.

- 한번의 환경설정 작업(image)을 거치면 컨테이너를 이용해 구축이 용이해진다.
>> class와 instance의 관계와 비슷
