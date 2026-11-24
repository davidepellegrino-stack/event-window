# Event Window Nº03: Anthropic's first-trade buyers, measured

**Question.** Anthropic (ANT) priced its IPO at $83 and its first trade on Nasdaq printed at $111.50 (19 Nov 2026). What happened over three trading days to the people who bought that first trade, and how does it compare with other large US IPOs?

**Sample.** 12 large US IPOs since 2008 with daily data on Yahoo Finance: Visa, GM, Facebook, Alibaba, Uber, Snowflake, Airbnb, Rivian, Arm, Cerebras, SpaceX, Anthropic. This is a hand-picked set of big, widely followed listings, not a complete list of the largest IPOs (non-US listings and direct listings are excluded).

**Data.** Yahoo Finance daily bars (open, close; split-adjusted), Nasdaq-100 index (^NDX). Offer prices from the issuers' pricing announcements; each is divided by later split factors (Visa 4:1 in 2015, as reported by Yahoo) to match the adjusted prices. Check: the computed day-1 returns vs offer (e.g. Facebook +0.6%, Alibaba +38.1%, Snowflake +111.6%, Airbnb +112.8%, Rivian +29.1%) match the widely reported first-day moves.

**Method.**
- `r_offer_d1` = close day 1 / offer − 1: the classic first-day return ("underpricing", Ritter).
- `r_open_d3` = close day 3 / open day 1 − 1: the return to a buyer of the first trade.
- `ar_open_d3` = `r_open_d3` − Nasdaq-100 return from its day-1 open to the day-3 close: a market-adjusted return (β = 1). A market model cannot be estimated for a stock with no price history, so β = 1 is the standard choice for new listings.

**Results** (`results/ipo_first_trade.csv`)

| IPO | Offer → first trade | Offer → day-1 close | First trade → day-3 close | Nasdaq-100 | Market-adjusted |
|---|---|---|---|---|---|
| Facebook (2012) | +10.7% | +0.6% | **−26.3%** | +1.2% | −27.4% |
| Anthropic (2026) | +34.3% | +17.1% | **−21.4%** | −3.0% | −18.4% |
| Cerebras (2026) | +89.2% | +68.1% | −15.2% | −1.3% | −14.0% |
| Airbnb (2020) | +114.7% | +112.8% | −11.0% | +1.6% | −12.5% |
| Alibaba (2014) | +36.3% | +38.1% | −6.0% | −1.5% | −4.5% |
| Uber (2019) | −6.7% | −7.6% | −4.9% | −2.0% | −2.8% |
| GM (2010) | +6.1% | +3.6% | −2.6% | +1.2% | −3.9% |
| Snowflake (2020) | +104.2% | +111.6% | −2.0% | −4.6% | +2.6% |
| Visa (2008) | +35.2% | +28.4% | +0.4% | +2.8% | −2.4% |
| Arm (2023) | +10.0% | +24.7% | +3.4% | −1.3% | +4.7% |
| Rivian (2021) | +36.9% | +29.1% | +21.7% | +0.7% | +21.0% |
| SpaceX (2026) | +11.1% | +19.2% | +40.9% | +2.0% | +38.9% |

Median first trade → day-3 close: −3.8% (market-adjusted: −3.3%). Anthropic ranks 2nd worst of 12 on both measures. Investors allocated at the $83 offer were still +5.6% on day 3 ($87.64).

**Caveats.**
- 12 IPOs is a small, hand-picked sample: read the ranking as context, not as a statistical test.
- "Open" is the first-day opening print reported by Yahoo; large IPOs often open hours after 9:30, while the index open is at 9:30, so the market adjustment is approximate.
- Three trading days only. Lock-ups, index inclusion and options listing can move prices later.

Re-run: `python3 ipo_first_trade.py` (downloads prices at run time; Yahoo may revise historical data slightly).
