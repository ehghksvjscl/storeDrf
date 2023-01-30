## Installation steps

1. python3이 설치 되어 있는지 확인 하십시요
2. repository를 clone 하세요
3. `virtualenv venv`를 사용해서 가상환경을 만드세요
4. `source venv/bin/activate`를 이용해서 가상환경을 활성화 하세요

- 윈도우 환경 : `source venv\Scripts\activate`

5. `pip install -m pip install -U pip wheel`를 통해 pip 최신버전으로 업그레이드 하세요
6. `pip install -r requirements.txt`를 통해 패키지를 다운로드 받으세요
7. `python manage.py test`를 통해 테스트를 실행 하세요.
8. `python manage.py runserver`를 통해 실행 시키세요.

## Commit Message Type

|    Type    | Description                                                                |
| :--------: | -------------------------------------------------------------------------- |
|   `feat`   | 새로운 기능 추가                                                           |
|   `fix`    | 버그수정                                                                   |
|   `docs`   | 문서 수정                                                                  |
|  `style`   | 스타일 관련 기능(코드 포맷팅, 세미콜론 누락, 코드 자체의 변경이 없는 경우) |
| `refactor` | 코드 리펙토링                                                              |
|   `test`   | 테스트 코드, 리펙토링 테스트 코드 추가                                     |
| `chore   ` | 빌드 업무 수정, 패키지 매니저 수정(ex .gitignore 수정 같은 경우)           |

## ERD

![주문(옵션)](https://user-images.githubusercontent.com/22442843/212725276-e0801e9b-6605-4b18-b1d7-3e85e3054bd9.png)

## API List

### 주문

| Method |        Path         |  Description   | Status Code |
| :----: | :-----------------: | :------------: | :---------: |
|  POST  |      /orders/       |   주문 생성    |     201     |
|  GET   |      /orders/       |   주문 조회    |     200     |
|  GET   | /orders/{order_id}/ | 주문 상세 조회 |  200, 404   |

### 장바구니

| Method |  Path   |  Description  | Status Code |
| :----: | :-----: | :-----------: | :---------: |
|  POST  | /carts/ | 장바구니 생성 |     201     |
|  GET   | /carts/ | 장바구니 조회 |     200     |

### 상품

| Method |          Path           |  Description   | Status Code |
| :----: | :---------------------: | :------------: | :---------: |
|  GET   | /products/{product_id}/ | 상품 상세 조회 |  200, 404   |

## 피드백

- [ ] 컨벤션 적용하기 (black)
- [x] status code에 대한 일관성 - 200은 성공을 의미하고, 201은 생성을 의미합니다. - 400은 클라이언트의 요청이 잘못되었을 때를 의미합니다. - 제가 생각하는 404코드는 "데이터가 없는 것이 에러인 상황"에서는 404를 사용합니다. - 또한 "데이터가 없어도 이상하지 않는 상황"에서는 200을 사용합니다. - 즉 GET orders 같은 경우는 200, orders/{order_id}/ 같은 경우는 404를 사용합니다.
