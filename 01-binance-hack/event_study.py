"""Event Window Nº01 - BNB around the Binance hack of 29 October 2026.

Market model event study (MacKinlay 1997), the same set-up as my M1 thesis:
  R_BNB,t = alpha + beta * R_BTC,t + e_t
estimated on trading days [-200, -20] before the event, then
  AR_t = R_BNB,t - (alpha + beta * R_BTC,t),  CAR = sum of AR over the window,
  t = CAR / (sigma_e * sqrt(L)).

Data: CoinGecko public API, daily prices (00:00 UTC). The return of day d is ln(P(d+1) / P(d)),
so "day 0" (29 Oct) covers 29 Oct 00:00 UTC to 30 Oct 00:00 UTC, which contains the hack (~20:05 UTC).

Run:  python event_study.py   (writes results/abnormal_returns.csv and prints the summary)
"""
import json, math, os, time, urllib.request
import numpy as np
import pandas as pd

EVENT = pd.Timestamp("2026-10-29")
EST_WINDOW = (-200, -20)
HERE = os.path.dirname(os.path.abspath(__file__))


def coingecko_daily(coin_id: str, days: int = 365) -> pd.DataFrame:
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.load(r)
    df = pd.DataFrame(d["prices"], columns=["t", "price"]).merge(
        pd.DataFrame(d["market_caps"], columns=["t", "mcap"]), on="t")
    df["date"] = pd.to_datetime(df.t, unit="ms").dt.normalize()
    return df.drop(columns="t").groupby("date").first()


def main():
    bnb = coingecko_daily("binancecoin"); time.sleep(2)
    btc = coingecko_daily("bitcoin")
    px = pd.DataFrame({"bnb": bnb.price, "btc": btc.price}).dropna()
    r = np.log(px).diff().shift(-1).dropna()          # return of day d = d -> d+1

    e = r.index.get_loc(EVENT)
    est = r.iloc[e + EST_WINDOW[0]: e + EST_WINDOW[1]]
    X = np.c_[np.ones(len(est)), est.btc]
    alpha, beta = np.linalg.lstsq(X, est.bnb, rcond=None)[0]
    resid = est.bnb - X @ [alpha, beta]
    sigma = resid.std(ddof=2)

    ar = r.bnb - (alpha + beta * r.btc)
    out = pd.DataFrame({"r_bnb": r.bnb, "r_btc": r.btc, "ar": ar, "t_ar": ar / sigma})
    out["day"] = np.arange(len(out)) - e
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    out.loc[out.day.between(-10, 10)].to_csv(os.path.join(HERE, "results", "abnormal_returns.csv"), float_format="%.6f")

    print(f"alpha={alpha:.5f}  beta={beta:.3f}  sigma={sigma:.4f}  (estimation {est.index[0].date()} to {est.index[-1].date()})")
    for a, b in [(0, 0), (0, 1), (-1, 1), (0, 5), (0, 7)]:
        if e + b < len(ar):
            car = ar.iloc[e + a: e + b + 1].sum()
            print(f"CAR[{a:+d},{b:+d}] = {car*100:+.2f}%   t = {car / (sigma * math.sqrt(b - a + 1)):+.2f}")
    mcap = bnb.mcap.loc[EVENT]
    print(f"Day-0 abnormal value change ~ {ar.iloc[e] * mcap / 1e9:+.1f} bn USD (market cap {mcap/1e9:.1f} bn)")


if __name__ == "__main__":
    main()
