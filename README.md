# Cheapest-Convenience
[DB Project] Recommend the cheapest convenience store to buy

## Period
22.10 ~ 22.11

## Background
고려대학교 세종캠퍼스 주변에는 3개의 편의점(세븐 일레븐, GS25, CU 편의점)이 있다. 이 세 편의점 모두 하나의 상품에 대해 가격이 다르거나 할인율이 다를 수 있다. 

이러한 상황을 모두 고려하여 어떤 물건을 특정 개수만큼 구매했을 때, 가장 저렴하게 구매할 수 있는 편의점이 어딘지 궁금했다.

전공 선택 과목인 데이터베이스 수업에서 배운 SQL을 기반으로 이를 알려주는 웹을 개발하고자 한다.

## Role 
데이터베이스에서 SQL로 입력 받은 데이터를 추출해서 가장 저렴한 상품을 계산하는 알고리즘 작성
  - cheapest_convenience_recommend.py

## Tech Stack
| Framework | Django |
|:---:|:---:|
| Language | Python |
| Database | MySQL |

## Data
- **dbproject** 편의점 데이터베이스
- **result** 과자, 음료, 라면 시연 영상
- **cheapest_convenience_recommend.py** 가장 저렴한 상품을 계산하는 함수 

## Expected Outcomes
고려대학교 학생들은 원하는 물품을 특정 개수만큼 구매할 때 가장 저렴한 편의점을 식별할 수 있다. 이로써 돈을 절약하면서도 필요한 물품을 구매할 수 있게 된다.

또한, 편의점을 일일이 방문하여 가격을 비교하거나 할인 정보를 확인하는 번거로움을 줄일 수 있습니다. 웹 애플리케이션을 사용하면 빠르게 다양한 편의점의 정보를 비교하여 최적의 선택을 할 수 있다.


## Future Work
실제로 편의점과 협업하여 매일 발주 품목 및 할인 기간을 데이터베이스에 업데이트하여 실제로 연동되는 웹을 개발할 수 있을 것으로 기대된다.

  


