## Installation steps

1. python3이 설치 되어 있는지 확인 하십시요
2. repository를 clone 하세요
3. `virtualenv venv`를 사용해서 가상환경을 만드세요
4. `source venv/bin/activate`를 이용해서 가상환경을 활성화 하세요

- 윈도우 환경 :  `source venv\Scripts\activate`

5. `pip install -m pip install -U pip wheel`를 통해 pip 최신버전으로 업그레이드 하세요
6. `pip install -r requirements.txt`를 통해 패키지를 다운로드 받으세요
7. `python manage.py runserver`를 통해 실행 시키세요.

## Commit Message Type

| Type          | Description                                      |
|:-------------:|--------------------------------------------------|
| `feat`        | 새로운 기능 추가                                  |
| `fix`         | 버그수정                                          |
| `docs`        | 문서 수정                                         |
| `style`       | 스타일 관련 기능(코드 포맷팅, 세미콜론 누락, 코드 자체의 변경이 없는 경우)|
| `refactor`    | 코드 리펙토링                 |
| `test`        | 테스트 코드, 리펙토링 테스트 코드 추가              |
| `chore   `    | 빌드 업무 수정, 패키지 매니저 수정(ex .gitignore 수정 같은 경우)    |

## ERD
![store_DRF](https://user-images.githubusercontent.com/22442843/212633160-a9642eab-61c3-4894-88d2-21471e3c38ec.png)