# Event Window Nº02 · Nvidia: what is one CEO worth to the market?

**Question.** How much of Nvidia's fall between 28 Oct and 16 Nov 2026 (−27.5%, ≈$1.44tn) is the Jensen Huang news, and how much is the chip-sector sell-off?

## Data
Daily adjusted closes from Yahoo Finance in one file, `data/prices.csv` (6 Jan to 16 Nov 2026): NVDA; peers AMD, AVGO, TSM, QCOM, MU; SMH; QQQ.

## Method
Market model on daily log returns (MacKinlay, 1997), as in my M1 thesis.
- Benchmark: equal-weight basket of chip peers **excluding Nvidia** (AMD, AVGO, TSM, QCOM, MU). Robustness: SMH (contains NVDA) and Nasdaq-100 (QQQ).
- Estimation window: trading days [−200, −20] before 29 Oct 2026.
- Event windows [0, +1], day 0 = first US session after each report:
  - E1 29 Oct: report that US officials see Huang as the target of a foreign intelligence effort.
  - E2 9 Nov: Huang acknowledges being unfaithful (Sun 8 Nov); board opens an independent investigation. Day +1 (10 Nov) also carries a report (The Information) that the relationship may have helped move ≥$7.5bn of chips to Chinese firms; Reuters could not verify it.
  - E3 12 Nov: second relationship reported (11 Nov); Huang resigns (8-K, 11 Nov), CFO Colette Kress interim CEO.
- t = CAR / (σ·√L). $ effect ≈ (e^CAR − 1) × market cap before the window (≈24.3bn shares).

## Results (vs chip peers ex-NVDA, β = 0.45)
| Window | CAR | t | ≈ $ |
|---|---|---|---|
| E1 29–30 Oct | −0.6% | −0.2 | −$32bn |
| E2 9–10 Nov | −13.7% | −4.7 | −$579bn |
| E3 12–13 Nov | −5.3% | −1.8 | −$217bn |
| E3 day 0 (12 Nov) | −5.1% | −2.5 | −$211bn |
| Sum of the three windows (6 sessions) | −19.5% | −3.9 | ≈ −$0.83tn |
| Full period 29 Oct–16 Nov (13 sessions) | −25.3% | −3.5 | — |

Robustness: E2 is −12.5% vs SMH and −13.5% vs QQQ; E3 is −3.9% / −4.6%. Full table: `results/abnormal_returns.csv`; daily ARs: `results/daily_abnormal_returns.csv`.

## Caveats
- The estimated beta to the peer basket is low (0.45), so on sector crash days (e.g. 5 Nov, SMH −11.2%) part of the sector move shows up as "abnormal". This is why the headline uses only the event windows, not the full-period CAR. With a market-adjusted model (β = 1), E2 is larger (≈ −18%) and E3 smaller (≈ −4%).
- Event windows bundle several pieces of news (E2: acknowledgement, board probe, unverified chips report), so they measure the combined reaction, not each item.
- Dollar figures are approximations (market cap × abnormal return).
- Nothing here is an opinion on the allegations; "reported" items are reports, not findings.
