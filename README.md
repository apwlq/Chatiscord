# Chatiscord
디스코드 채널의 채팅을 Web채팅으로 만들어 줍니다.
윈도우에서 작동하지않는 오류 수정 중  
2023-06-12 윈도우에서 작동하지않는 오류 해결완료.
> 문제 원인
- 코드에서 사용하는 스레딩과 `asyncio` 라이브러리 간의 충돌 때문에 발생
> 해경 방법
- `nest_asyncio` 라이브러리를 사용
\


  
  
  
  
![example](https://raw.githubusercontent.com/apwlq/Chatiscord/master/example.gif?raw=true)
