# Event Window Nº04: the largest US IPOs of 2025-26, measured from the first-day close

**Question.** Anthropic closed below its $83 offer price on 24 Nov 2026, its fourth session. Is that unusual? How have the largest recent US IPOs performed for an investor who bought at the first-day close?

**Sample (14 deals, selected by deal size, not by outcome).**
- The 10 largest US IPOs of 2025 (Renaissance Capital, 2025 US IPO Market Annual Review, "Largest US IPOs"): Medline, Venture Global, CoreWeave, SailPoint, Klarna, Figma, Bullish, Circle, NIQ, BETA Technologies.
- The 4 largest US IPOs of 2026 to date (Renaissance Capital, "All Time Largest U.S. IPOs"): Anthropic ($81.3bn), SpaceX ($75.0bn), SK hynix ADR ($26.5bn), Cerebras ($5.55bn).
Renaissance excludes SPACs.

**Data.** Yahoo Finance daily closes; Nasdaq Composite (^IXIC). Valuation date 25 Nov 2026 (US markets closed on 26 Nov for Thanksgiving).

**Method.**
- `r_from_day1_close` = close on 25 Nov 2026 / close on the first trading day − 1.
- `market_adjusted` = `r_from_day1_close` − Nasdaq Composite return over the same window (β = 1). A market model cannot be estimated without pre-IPO price history, so β = 1 is the standard choice for new listings.

**Results** (`results/ipo_class.csv`)

| IPO | First day | From first-day close | Nasdaq, same window | Market-adjusted (pp) |
|---|---|---|---|---|
| Figma (2025) | 31 Jul 2025 | −85.2% | +11.7% | −96.8 |
| Cerebras (2026) | 14 May 2026 | −71.2% | −11.4% | −59.7 |
| Bullish (2025) | 13 Aug 2025 | −71.1% | +8.6% | −79.7 |
| Klarna (2025) | 11 Sep 2025 | −68.8% | +7.0% | −75.8 |
| BETA Technologies (2025) | 4 Nov 2025 | −54.4% | +1.0% | −55.5 |
| Venture Global (2025) | 24 Jan 2025 | −51.1% | +18.2% | −69.3 |
| Circle (2025) | 5 Jun 2025 | −42.0% | +22.2% | −64.2 |
| SK hynix ADR (2026) | 10 Jul 2026 | −33.8% | −10.3% | −23.6 |
| SpaceX (2026) | 12 Jun 2026 | −20.8% | −8.9% | −11.9 |
| Anthropic (2026) | 19 Nov 2026 | −14.8% | −1.2% | −13.6 |
| NIQ (2025) | 23 Jul 2025 | −10.9% | +12.2% | −23.1 |
| Medline (2025) | 17 Dec 2025 | −1.0% | +3.9% | −5.0 |
| SailPoint (2025) | 13 Feb 2025 | +4.0% | +18.3% | −14.3 |
| CoreWeave (2025) | 28 Mar 2025 | +6.4% | +36.2% | −29.7 |

12 of 14 trade below their first-day close (median −37.9%; deal-size-weighted −21.9%). 14 of 14 underperform the Nasdaq Composite over the same window (median −42.6 percentage points).

**Caveats.**
- Small sample; windows range from 4 sessions (Anthropic) to about 22 months (Venture Global), so the numbers are not directly comparable across deals.
- β = 1 understates or overstates the benchmark for stocks whose true beta differs from 1; the Nasdaq Composite is a price index (dividends excluded).
- Closing prices only; no transaction costs.

Re-run: `python3 ipo_class.py` (downloads prices at run time; Yahoo may revise data slightly).
