"""Event Window Nº05: the OAT-Bund spread and French bank shares.

Question: the 10-year OAT-Bund spread averaged 147 bp in October 2026, the widest monthly
average since November 2011. Have French bank shares priced a sovereign-bank "doom loop",
i.e. have they underperformed euro area banks as the spread widened?

Data:
  - 10-year government bond yields, France and Germany: ECB long-term interest rate statistics
    (dataset IRS, series M.FR.L.L40.CI.0000.EUR.N.Z and M.DE.L.L40.CI.0000.EUR.N.Z), monthly averages.
  - Share prices: Yahoo Finance adjusted closes (dividends reinvested) for BNP Paribas (BNP.PA),
    Societe Generale (GLE.PA), Credit Agricole SA (ACA.PA), the iShares EURO STOXX Banks 30-15 ETF
    (EXX1.DE, proxy for euro area banks) and seven large euro area banks.
Tests:
  1. Window return from 31 Aug 2026 (before the spread jumped: 82 bp in Aug, 97 bp in Sep,
     147 bp in Oct) to the valuation date.
  2. Monthly regression since START_REG: relative return of an equal-weight basket of the three
     French banks vs EXX1 on the monthly change in the spread (bp). OLS with t-statistic.
Run: python3 french_banks_spread.py  -> data/*.csv, results/*.csv
"""
import csv, io, json, os, time, urllib.request
from datetime import datetime, timezone
import numpy as np

VAL_DATE, WIN_START, START_REG = "2026-11-25", "2026-08-31", "2012-01"
FRENCH = {"BNP.PA": "BNP Paribas", "GLE.PA": "Societe Generale", "ACA.PA": "Credit Agricole"}
BENCH = {"EXX1.DE": "Euro area banks (EXX1 ETF)"}
PEERS = {"SAN.MC": "Santander", "BBVA.MC": "BBVA", "ISP.MI": "Intesa Sanpaolo", "UCG.MI": "UniCredit",
         "DBK.DE": "Deutsche Bank", "CBK.DE": "Commerzbank", "INGA.AS": "ING"}
UA = {"User-Agent": "Mozilla/5.0"}

def ecb_yield(country):
    url = (f"https://data-api.ecb.europa.eu/service/data/IRS/M.{country}.L.L40.CI.0000.EUR.N.Z"
           "?startPeriod=2010-01&format=csvdata")
    text = urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode()
    return {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in csv.DictReader(io.StringIO(text))}

def yahoo_daily(ticker):
    """Daily adjusted closes over 20 years (range=max returns monthly bars, so it is not used)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=20y&interval=1d"
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))["chart"]["result"][0]
    px = r["indicators"]["adjclose"][0]["adjclose"]; off = r["meta"]["gmtoffset"]
    return {datetime.fromtimestamp(t + off, timezone.utc).date().isoformat(): p
            for t, p in zip(r["timestamp"], px) if p is not None}

def month_end(daily, last_date):
    """Last available adjusted close of each calendar month, up to last_date."""
    out = {}
    for d in sorted(daily):
        if d <= last_date: out[d[:7]] = daily[d]
    return out

def main():
    os.makedirs("data", exist_ok=True); os.makedirs("results", exist_ok=True)
    fr, de = ecb_yield("FR"), ecb_yield("DE")
    spread = {m: round((fr[m] - de[m]) * 100, 1) for m in sorted(fr) if m in de}
    with open("data/oat_bund_spread_monthly.csv", "w", newline="") as f:
        csv.writer(f).writerows([["month", "fr_10y", "de_10y", "spread_bp"]] +
                                [[m, fr[m], de[m], spread[m]] for m in spread])
    last_m = max(spread)
    wider_since = max(m for m, v in spread.items() if m < last_m and v >= spread[last_m])

    # 1) window returns
    rows, daily = [], {}
    for tk, name in {**FRENCH, **BENCH, **PEERS}.items():
        p = daily[tk] = yahoo_daily(tk); time.sleep(0.3)
        a = max(d for d in p if d <= WIN_START); b = max(d for d in p if d <= VAL_DATE)
        rows.append({"ticker": tk, "name": name, "group": "France" if tk in FRENCH else
                     ("benchmark" if tk in BENCH else "euro area peer"),
                     "start": a, "end": b, "total_return_pct": round((p[b] / p[a] - 1) * 100, 1)})
    rows.sort(key=lambda r: r["total_return_pct"])
    with open("results/window_returns.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    # 2) monthly regression
    mp = {tk: month_end(daily[tk], VAL_DATE) for tk in [*FRENCH, *BENCH]}
    months = [m for m in sorted(spread) if m >= START_REG and all(m in mp[t] for t in mp)]
    months = [m for m in months if m <= last_m]   # spread data end month
    reg = []
    for a, b in zip(months, months[1:]):
        fra = np.mean([mp[t][b] / mp[t][a] - 1 for t in FRENCH])
        eu = mp["EXX1.DE"][b] / mp["EXX1.DE"][a] - 1
        reg.append((b, (fra - eu) * 100, spread[b] - spread[a]))
    x = np.array([r[2] for r in reg]); y = np.array([r[1] for r in reg])
    beta, alpha = np.polyfit(x, y, 1); res = y - (alpha + beta * x)
    se = np.sqrt(res.var(ddof=2) / ((x - x.mean()) ** 2).sum()); r2 = 1 - res.var() / y.var()
    with open("results/monthly_regression.csv", "w", newline="") as f:
        csv.writer(f).writerows([["month", "french_minus_euro_banks_pp", "d_spread_bp"]] +
                                [[m, round(a, 2), round(b, 1)] for m, a, b in reg])
    last = reg[-1]; pred = alpha + beta * last[2]
    summary = {"oct_2026_d_spread_bp": round(last[2], 1), "oct_2026_relative_pp": round(last[1], 2),
               "oct_2026_predicted_pp": round(pred, 2),"last_month": last_m, "last_spread_bp": spread[last_m],
               "previous_month_at_least_as_wide": wider_since, "spread_jun_2026_bp": spread["2026-06"],
               "n_months": len(reg), "beta_pp_per_bp": round(beta, 3), "t_stat": round(beta / se, 2),
               "r2": round(r2, 3), "reg_window": f"{reg[0][0]}..{reg[-1][0]}"}
    with open("results/summary.json", "w") as f: json.dump(summary, f, indent=1)
    for r in rows: print(f"{r['name']:<28}{r['total_return_pct']:>7.1f}%")
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()
