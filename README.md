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
![주문(옵션)](https://user-images.githubusercontent.com/22442843/212725276-e0801e9b-6605-4b18-b1d7-3e85e3054bd9.png)

## API List

### 주문

| Method | Path | Description |
|:------:|:----:|:-----------:|
| POST   | /orders/ | 주문 생성 |
| GET    | /orders/ | 주문 조회 |
| GET    | /orders/{order_id}/ | 주문 상세 조회 |

### 장바구니

| Method | Path | Description |
|:------:|:----:|:-----------:|
| POST   | /carts/ | 장바구니 생성 |
| GET    | /carts/ | 장바구니 조회 |

### 상품

| Method | Path | Description |
|:------:|:----:|:-----------:|
| GET    | /products/{product_id}/ | 상품 상세 조회 |



## Qustion
 - [ ] CASECADE가 많을 경우 (nginx가 터진다거나, DB 연결 시간이 끊긴다거나) timeout이 발생하는데 이를 해결할 수 있는 방법이 있을까요?
      - Celery를 사용해서 비동기 처리를 하면 해결할 수 있다.?
      
 - [ ] related_name가 없을 경우에는 어떻게 접근할 수 있을까요?
   - 역참조를 하기 위해서는 related_name을 지정해주어야 한다.?

## Why?

  ### Why API가 2개 필요한가?
 - 유저가 장바구니에서 원하는 상품을 선택해 한 번에 주문하는 기능 (POST)
 - 유저가 상품의 옵션을 선택 후 주문서를 생성하는 기능 (POST)

## TODO Refeator
 - 순수 함수 만들기 (필수)
 - 복잡한 함수 class 형태로 바꾸기 (필수)
 - query 파일 분리  (필수)
 - type hint 작성 (필수)