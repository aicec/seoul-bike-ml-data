"""UCI Seoul Bike Sharing Demand → 수업용 CSV
  python convert_bike.py <SeoulBikeData.csv> <출력 폴더>
  public/bikes_hourly.csv        2017-12-01 ~ 2018-10-31 시간별 8,040줄 (정답 rentals 포함)
  public/bikes_daily.csv         같은 기간 일별 335줄 (하루 합계 · 평균 기온 · 강수 합 · 요일)
  public/hidden_2018-11_input.csv 2018-11 시간별 720줄, rentals 열 없음 (4일차 대회 입력)
  private/hidden_2018-11_answer.csv 2018-11 정답 — 공개 저장소에 올리지 않음
원본: Seoul Bike Sharing Demand, UCI Machine Learning Repository (서울시 공공데이터 · 기상청) · CC BY 4.0
"""
import sys
from pathlib import Path
import pandas as pd

src, out = Path(sys.argv[1]), Path(sys.argv[2])
d = pd.read_csv(src, encoding="latin1")
d.columns = ["date", "rentals", "hour", "temp_c", "humidity_pct", "wind_ms", "visibility_10m", "dew_point_c",
             "solar_mj", "rain_mm", "snow_cm", "season", "holiday", "functioning"]
d["date"] = pd.to_datetime(d["date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
d["holiday"] = (d["holiday"] == "Holiday").astype(int)
d["functioning"] = (d["functioning"] == "Yes").astype(int)
d["season"] = d["season"].str.lower()
dt = pd.to_datetime(d["date"])
d["weekday"] = dt.dt.day_of_week                    # 0 = 월 … 6 = 일
d["day_name"] = dt.dt.day_name().str[:3]           # Mon … Sun
d["is_weekend"] = (d["weekday"] >= 5).astype(int)
d["month"] = dt.dt.month
cols = ["date", "hour", "rentals", "temp_c", "humidity_pct", "wind_ms", "visibility_10m", "dew_point_c", "solar_mj",
        "rain_mm", "snow_cm", "season", "holiday", "functioning", "weekday", "day_name", "is_weekend", "month"]
d = d[cols]
pub = d[d["date"] < "2018-11-01"]
hid = d[d["date"] >= "2018-11-01"]
(out / "public").mkdir(parents=True, exist_ok=True); (out / "private").mkdir(parents=True, exist_ok=True)
pub.to_csv(out / "public/bikes_hourly.csv", index=False)
daily = pub.groupby("date").agg(rentals=("rentals", "sum"), temp_mean=("temp_c", "mean"), temp_max=("temp_c", "max"),
                                rain_mm=("rain_mm", "sum"), snow_cm=("snow_cm", "sum"), humidity_mean=("humidity_pct", "mean"),
                                holiday=("holiday", "max"), functioning=("functioning", "min"), weekday=("weekday", "first"),
                                day_name=("day_name", "first"), is_weekend=("is_weekend", "first"), month=("month", "first")).reset_index()
daily["temp_mean"] = daily["temp_mean"].round(1); daily["humidity_mean"] = daily["humidity_mean"].round(1)
daily.to_csv(out / "public/bikes_daily.csv", index=False)
hid.drop(columns=["rentals"]).to_csv(out / "public/hidden_2018-11_input.csv", index=False)
hid[["date", "hour", "rentals"]].to_csv(out / "private/hidden_2018-11_answer.csv", index=False)
print("hourly", len(pub), "daily", len(daily), "hidden", len(hid))
