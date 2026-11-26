# Event Window Nº05: the OAT–Bund spread at a 2011 high, and French bank shares

**Question.** The 10-year OAT–Bund spread averaged 147 bp in October 2026, the widest monthly average since November 2011 (154 bp). Have French bank shares priced a sovereign-bank loop, i.e. have they lagged euro area banks as the spread widened?

**Data.**
- 10-year government bond yields for France and Germany: ECB long-term interest rate statistics (dataset IRS, series `M.FR.L.L40.CI.0000.EUR.N.Z` and `M.DE.L.L40.CI.0000.EUR.N.Z`), monthly averages, Jan 2010–Oct 2026 (`data/oat_bund_spread_monthly.csv`).
- Share prices: Yahoo Finance daily adjusted closes (dividends reinvested) for BNP Paribas, Société Générale, Crédit Agricole SA, the iShares EURO STOXX Banks 30-15 ETF (EXX1, proxy for euro area banks) and seven large euro area banks.

**Method.**
1. Window returns from 31 Aug 2026 (before the spread jumped: 82 bp in August, 97 bp in September, 147 bp in October) to 25 Nov 2026.
2. Monthly OLS, Feb 2012–Oct 2026 (177 months): relative return of an equal-weight basket of the three French banks minus EXX1 (pp) on the monthly change in the spread (bp). Month-end prices vs monthly-average yields is a timing mismatch; this likely biases the slope towards zero.

**Results** (`results/`)

| | |
|---|---|
| Spread, Oct 2026 (monthly average) | 147.4 bp (Jun 2026: 71.6 bp; Nov 2011: 154 bp) |
| Slope, French banks vs euro area banks on Δspread | −0.076 pp per bp (t = −2.46, R² = 0.03, 177 months) |
| October 2026: Δspread | +50.7 bp |
| October 2026: predicted relative return | −3.5 pp |
| October 2026: actual relative return | +0.6 pp |

Window returns, 31 Aug–25 Nov 2026 (`results/window_returns.csv`): Santander −19.9%, Deutsche Bank −16.1%, Intesa Sanpaolo −15.9%, Commerzbank −15.0%, Crédit Agricole −14.9%, Société Générale −14.6%, euro area banks (EXX1) −14.0%, BBVA −13.6%, ING −13.5%, BNP Paribas −11.3%, UniCredit −9.5%.

**Reading.** Historically, a wider OAT–Bund spread has coincided with French banks underperforming their euro area peers (small but statistically significant slope). In October 2026, the largest monthly widening in the sample, they did not: the sell-off has been European, not French-specific. September (+15 bp, French banks −3.1 pp) was closer to the historical pattern.

**Caveats.** Monthly data, low R²; one month is one observation; yields are monthly averages while prices are month-end; the spread may keep moving in November (not yet published by the ECB at the time of writing). Equity prices are only one channel: funding spreads and CDS are not covered here.

Re-run: `python3 french_banks_spread.py` (downloads data at run time).
