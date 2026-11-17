"""Event Window No.02 - Nvidia: what is one CEO worth to the market?
Market-model event study (MacKinlay, 1997) on daily log returns.
Data: Yahoo Finance adjusted daily closes, data/prices.csv. Run: python event_study.py"""
import os
import numpy as np
import pandas as pd

PEERS = ["AMD", "AVGO", "TSM", "QCOM", "MU"]
SHARES = 24.3e9  # approx. NVDA shares outstanding, only for the $ approximation
EVENTS = {  # day 0 = first US session after each report; window [0, +1]
    "E1 intelligence-effort report": "2026-10-29",
    "E2 affair acknowledged + board probe": "2026-11-09",
    "E3 second report + resignation": "2026-11-12",
}

px = pd.read_csv("data/prices.csv", parse_dates=["date"], index_col="date").dropna()
lr = np.log(px).diff().dropna()
bench = {
    "Chip peers ex-NVDA (equal weight)": lr[PEERS].mean(axis=1),
    "SMH (contains NVDA)": lr["SMH"],
    "Nasdaq-100 (QQQ)": lr["QQQ"],
}
t0 = lr.index.get_loc(pd.Timestamp(EVENTS["E1 intelligence-effort report"]))
est = slice(t0 - 200, t0 - 20)  # estimation window [-200, -20]

rows, daily = [], {}
for bname, rm in bench.items():
    beta, alpha = np.polyfit(rm.iloc[est], lr["NVDA"].iloc[est], 1)
    resid = lr["NVDA"].iloc[est] - (alpha + beta * rm.iloc[est])
    sigma = resid.std(ddof=2)
    ar = lr["NVDA"] - (alpha + beta * rm)
    daily[bname] = ar

    def add(label, d0, d1):
        a = ar.loc[d0:d1]
        car = a.sum()
        p0 = px["NVDA"].shift(1).loc[d0]
        rows.append(dict(benchmark=bname, window=label, start=d0.date(), end=d1.date(), days=len(a),
                         alpha=alpha, beta=beta, sigma=sigma, CAR=car, t=car / (sigma * np.sqrt(len(a))),
                         usd_bn=(np.exp(car) - 1) * p0 * SHARES / 1e9))

    for name, d in EVENTS.items():
        i = lr.index.get_loc(pd.Timestamp(d))
        add(f"{name} [0,+1]", lr.index[i], lr.index[i + 1])
        add(f"{name} [0]", lr.index[i], lr.index[i])
    add("Full period 29 Oct - 16 Nov", pd.Timestamp("2026-10-29"), pd.Timestamp("2026-11-16"))

res = pd.DataFrame(rows)
os.makedirs("results", exist_ok=True)
res.to_csv("results/abnormal_returns.csv", index=False, float_format="%.6f")
pd.DataFrame(daily).loc["2026-10-20":"2026-11-16"].to_csv("results/daily_abnormal_returns.csv", float_format="%.6f")
pd.set_option("display.width", 200)
print(res[["benchmark", "window", "beta", "CAR", "t", "usd_bn"]].round(4).to_string(index=False))
