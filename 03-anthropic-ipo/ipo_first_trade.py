"""Event Window Nº03: what happened to the buyers of the FIRST TRADE in 12 large US IPOs?

For each IPO we compare three prices: the offer price (what allocated investors paid),
the first-day open (the first trade on the exchange) and the close on trading day 3.
  r_offer_d1   = close_day1 / offer - 1        (classic first-day "pop", Ritter)
  r_open_d3    = close_day3 / open_day1 - 1    (return to someone who bought the first trade)
  r_ndx_d3     = NDX close_day3 / NDX open_day1 - 1
  ar_open_d3   = r_open_d3 - r_ndx_d3          (market-adjusted return, beta = 1)
A market model cannot be estimated for a new listing (no pre-event price history), so the
market-adjusted return (beta = 1) is the standard choice in the IPO literature.
Data: Yahoo Finance daily bars (split-adjusted). Offer prices are divided by later split
factors so they are on the same basis as the adjusted prices.
Run: python3 ipo_first_trade.py   -> data/prices.csv, results/ipo_first_trade.csv
"""
import csv, json, os, statistics, time, urllib.request
from datetime import datetime, timedelta, timezone

IPOS = [  # ticker, name, offer price (USD, at IPO), first trading day
    ("V",    "Visa",      44.00, "2008-03-19"),
    ("GM",   "GM",        33.00, "2010-11-18"),
    ("META", "Facebook",  38.00, "2012-05-18"),
    ("BABA", "Alibaba",   68.00, "2014-09-19"),
    ("UBER", "Uber",      45.00, "2019-05-10"),
    ("SNOW", "Snowflake", 120.00, "2020-09-16"),
    ("ABNB", "Airbnb",    68.00, "2020-12-10"),
    ("RIVN", "Rivian",    78.00, "2021-11-10"),
    ("ARM",  "Arm",       51.00, "2023-09-14"),
    ("CBRS", "Cerebras",  185.00, "2026-05-14"),
    ("SPCX", "SpaceX",    135.00, "2026-06-12"),
    ("ANT",  "Anthropic", 83.00, "2026-11-19"),
]
INDEX = "^NDX"

def yahoo(ticker, start, end):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?period1={start}&period2={end}&interval=1d&events=split")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req))["chart"]["result"][0]
    q, off = r["indicators"]["quote"][0], r["meta"]["gmtoffset"]
    bars = [(datetime.fromtimestamp(t + off, timezone.utc).date().isoformat(), q["open"][i], q["close"][i])
            for i, t in enumerate(r["timestamp"]) if q["close"][i] is not None]
    splits = [(datetime.fromtimestamp(s["date"], timezone.utc).date().isoformat(), s["numerator"] / s["denominator"])
              for s in (r.get("events", {}).get("splits", {}) or {}).values()]
    return bars, splits

def main():
    os.makedirs("data", exist_ok=True); os.makedirs("results", exist_ok=True)
    prices, rows = [], []
    for tk, name, offer, first in IPOS:
        d0 = datetime.fromisoformat(first).replace(tzinfo=timezone.utc)
        start, end = int((d0 - timedelta(days=7)).timestamp()), int((d0 + timedelta(days=12)).timestamp())
        bars, splits = yahoo(tk, start, int(time.time()))      # full history: catches every later split
        factor = 1.0
        for d, f in splits:
            if d > first: factor *= f
        adj_offer = offer / factor
        s = [b for b in bars if b[0] >= first][:3]
        idx = [b for b in yahoo(INDEX, start, end)[0] if b[0] >= first][:3]
        assert s[0][0] == first and idx[2][0] == s[2][0], (tk, s, idx)
        for d, o, c in s: prices.append([tk, d, round(o, 4), round(c, 4)])
        r_open_d3 = s[2][2] / s[0][1] - 1
        r_ndx = idx[2][2] / idx[0][1] - 1
        rows.append({"ticker": tk, "name": name, "first_day": first, "offer": offer,
                     "split_factor": factor, "open_day1": round(s[0][1] * factor, 2),
                     "close_day1": round(s[0][2] * factor, 2), "close_day3": round(s[2][2] * factor, 2),
                     "r_offer_open_pct": round((s[0][1] / adj_offer - 1) * 100, 1),
                     "r_offer_d1_pct": round((s[0][2] / adj_offer - 1) * 100, 1),
                     "r_offer_d3_pct": round((s[2][2] / adj_offer - 1) * 100, 1),
                     "r_open_d3_pct": round(r_open_d3 * 100, 1),
                     "r_ndx_d3_pct": round(r_ndx * 100, 1),
                     "ar_open_d3_pct": round((r_open_d3 - r_ndx) * 100, 1)})
        time.sleep(0.5)
    rows.sort(key=lambda r: r["r_open_d3_pct"])
    for i, r in enumerate(rows, 1): r["rank_worst_first"] = i
    with open("results/ipo_first_trade.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open("data/prices.csv", "w", newline="") as f:
        csv.writer(f).writerows([["ticker", "date", "open_adj", "close_adj"]] + prices)
    med = statistics.median(r["r_open_d3_pct"] for r in rows)
    med_ar = statistics.median(r["ar_open_d3_pct"] for r in rows)
    print(f"{'IPO':<10}{'offer->open':>12}{'offer->d1':>11}{'open->d3':>10}{'NDX':>7}{'adj.':>7}")
    for r in rows:
        print(f"{r['name']:<10}{r['r_offer_open_pct']:>11.1f}%{r['r_offer_d1_pct']:>10.1f}%"
              f"{r['r_open_d3_pct']:>9.1f}%{r['r_ndx_d3_pct']:>6.1f}%{r['ar_open_d3_pct']:>6.1f}%")
    print(f"median open->day-3: {med:.1f}%   median market-adjusted: {med_ar:.1f}%")

if __name__ == "__main__":
    main()
