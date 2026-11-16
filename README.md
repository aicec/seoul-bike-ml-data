# 서울 따릉이 대여량 — 수업 데이터

충북대학교 「Python 활용 머신러닝 및 딥러닝 특강」(AICEC) 수업용 데이터입니다. 원본은 **Seoul Bike Sharing Demand**(UCI Machine Learning Repository, 서울시 공공데이터 · 기상청 자료, CC BY 4.0)이며, 열 이름을 정리하고 2018년 11월을 「숨긴 달」로 떼어 두었습니다.

Colab에서 아래 한 셀로 바로 읽습니다. 다운로드할 것이 없습니다.

```python
import pandas as pd
BASE = "https://raw.githubusercontent.com/aicec/seoul-bike-ml-data/main/"
bikes = pd.read_csv(BASE + "bikes_hourly.csv")
```

## 파일
| 파일 | 내용 | 쓰는 날 |
|---|---|---|
| bikes_hourly.csv | 2017-12-01 ~ 2018-10-31 **한 시간 = 1줄**, 8,040줄. 대여 대수 + 그 시각의 날씨 | 1 · 2 · 3일차 |
| bikes_daily.csv | 같은 기간 **하루 = 1줄**, 335줄. 하루 합계 · 평균 기온 · 강수 합 · 요일 | 1 · 2일차 |
| hidden_2018-11_input.csv | 2018년 11월 720시간의 날씨 · 시각 · 요일만 (대여 대수 없음) | 4일차 대회 입력 |

## 열 사전 (bikes_hourly.csv)
| 열 | 뜻 | 단위 |
|---|---|---|
| date | 날짜 | YYYY-MM-DD |
| hour | 시각 | 0 ~ 23 |
| **rentals** | **그 시간에 대여된 자전거 수 — 예측 대상** | 대 |
| temp_c | 기온 | ℃ |
| humidity_pct | 습도 | % |
| wind_ms | 풍속 | m/s |
| visibility_10m | 가시거리 | 10 m 단위 |
| dew_point_c | 이슬점 온도 | ℃ |
| solar_mj | 일사량 | MJ/m² |
| rain_mm | 강수량 | mm |
| snow_cm | 적설 | cm |
| season | 계절 | winter · spring · summer · autumn |
| holiday | 공휴일이면 1 | 0 / 1 |
| functioning | 따릉이가 운영된 시간이면 1 (0이면 대여 0대) | 0 / 1 |
| weekday | 요일 번호 | 0 = 월 … 6 = 일 |
| day_name | 요일 | Mon … Sun |
| is_weekend | 토 · 일이면 1 | 0 / 1 |
| month | 월 | 1 ~ 12 |

bikes_daily.csv: date · rentals(하루 합계) · temp_mean · temp_max · rain_mm(합) · snow_cm · humidity_mean · holiday · functioning(그날 내내 운영이면 1) · weekday · day_name · is_weekend · month

## 알아 둘 특이점
- **운영 안 한 시간**(functioning = 0)이 223줄 있고 그때 대여는 0입니다. 평균을 낼 때는 `bikes[bikes.functioning == 1]`로 빼야 합니다.
- 평일은 **8시와 18시 두 봉우리**(출퇴근), 주말은 오후에 완만한 봉우리 하나입니다.
- 비가 오는 시간의 평균 대여는 168대, 안 오는 시간은 769대입니다(운영 시간 기준).
- 기온과 대여량의 상관은 0.57 — 더울수록 늘다가 30 ℃를 넘으면 조금 줄어듭니다.

## 수업 노트북 (Colab에서 바로 열기)
| 일차 | 수강생용 |
|---|---|
| 1일차 · 따릉이는 언제 많이 나갈까 | https://colab.research.google.com/github/aicec/seoul-bike-ml-data/blob/main/notebooks/day1_student.ipynb |

열리면 **파일 → Drive에 사본 저장**을 먼저 누르세요. 완성본은 수업 뒤에 올라옵니다.

## 출처
Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5F62R — 원자료: 서울열린데이터광장(따릉이 대여 이력) · 기상청. CC BY 4.0
