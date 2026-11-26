"""Event Window Nº04: where do the largest US IPOs of 2025-26 trade relative to their first-day close?

Sample (objective, from Renaissance Capital, which excludes SPACs):
  - the 10 largest US IPOs of 2025 (Renaissance Capital 2025 Annual Review, "Largest US IPOs");
  - the 4 largest US IPOs of 2026 to date (Renaissance Capital "All Time Largest U.S. IPOs" page:
    Anthropic $81.3bn, SpaceX $75.0bn, SK hynix $26.5bn, Cerebras $5.55bn).
Measure: r_d1 = close on the valuation date / close on the first trading day - 1
  (the return to an investor who bought at the first close and still holds).
Also reported: return vs the Nasdaq Composite over the same window (market-adjusted, beta = 1).
Data: Yahoo Finance daily bars, split-adjusted. Valuation date: last common close on or before VAL_DATE.
Run: python3 ipo_class.py  -> data/prices.csv, results/ipo_class.csv
"""
import csv, json, os, statistics, time, urllib.request
from datetime import datetime, timezone

VAL_DATE = "2026-11-25"   # last US session before Thanksgiving (26 Nov 2026)
IPOS = [  # ticker, name, year, deal size $m (Renaissance)
    ("MDLN", "Medline", 2025, 6265), ("VG", "Venture Global", 2025, 1750),
    ("CRWV", "CoreWeave", 2025, 1500), ("SAIL", "SailPoint", 2025, 1380),
    ("KLAR", "Klarna", 2025, 1373), ("FIG", "Figma", 2025, 1219),
    ("BLSH", "Bullish", 2025, 1110), ("CRCL", "Circle", 2025, 1054),
    ("NIQ", "NIQ", 2025, 1050), ("BETA", "BETA Technologies", 2025, 1015),
    ("ANT", "Anthropic", 2026, 81340), ("SPCX", "SpaceX", 2026, 75000),
    ("SKHY", "SK hynix (ADR)", 2026, 26507), ("CBRS", "Cerebras", 2026, 5550),
]
INDEX = "^IXIC"

def yahoo(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5y&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req))["chart"]["result"][0]
    q, off = r["indicators"]["quote"][0], r["meta"]["gmtoffset"]
    return {datetime.fromtimestamp(t + off, timezone.utc).date().isoformat(): q["close"][i]
            for i, t in enumerate(r["timestamp"]) if q["close"][i] is not None}

def main():
    os.makedirs("data", exist_ok=True); os.makedirs("results", exist_ok=True)
    idx = yahoo(INDEX)
    rows, prices = [], []
    for tk, name, year, size in IPOS:
        p = yahoo(tk); time.sleep(0.4)
        days = sorted(d for d in p if d <= VAL_DATE)
        first, last = days[0], days[-1]
        r = p[last] / p[first] - 1
        i0 = max(d for d in idx if d <= first); i1 = max(d for d in idx if d <= last)
        rm = idx[i1] / idx[i0] - 1
        rows.append({"ticker": tk, "name": name, "ipo_year": year, "deal_size_musd": size,
                     "first_day": first, "close_day1": round(p[first], 2), "val_date": last,
                     "close_val": round(p[last], 2), "r_from_day1_close_pct": round(r * 100, 1),
                     "nasdaq_same_window_pct": round(rm * 100, 1),
                     "market_adjusted_pct": round((r - rm) * 100, 1)})
        prices += [[tk, first, round(p[first], 4)], [tk, last, round(p[last], 4)]]
    rows.sort(key=lambda r: r["r_from_day1_close_pct"])
    with open("results/ipo_class.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open("data/prices.csv", "w", newline="") as f:
        csv.writer(f).writerows([["ticker", "date", "close"]] + prices)
    below = sum(r["r_from_day1_close_pct"] < 0 for r in rows)
    below_adj = sum(r["market_adjusted_pct"] < 0 for r in rows)
    w_ret = sum(r["r_from_day1_close_pct"] * r["deal_size_musd"] for r in rows) / sum(r["deal_size_musd"] for r in rows)
    for r in rows:
        print(f"{r['name']:<18}{r['ipo_year']}  {r['first_day']}  {r['r_from_day1_close_pct']:>7.1f}%  Nasdaq {r['nasdaq_same_window_pct']:>6.1f}%  adj {r['market_adjusted_pct']:>7.1f}%")
    print(f"below day-1 close: {below}/{len(rows)}; market-adjusted below: {below_adj}/{len(rows)}")
    print(f"median: {statistics.median(r['r_from_day1_close_pct'] for r in rows):.1f}%; "
          f"median adj: {statistics.median(r['market_adjusted_pct'] for r in rows):.1f}%; deal-size weighted: {w_ret:.1f}%")

if __name__ == "__main__":
    main()
