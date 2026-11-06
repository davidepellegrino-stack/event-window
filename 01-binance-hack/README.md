# Nº01 · The Binance hack (29 October 2026)

About $6.3bn left Binance hot wallets on 29 October 2026. This folder measures how BNB, Binance's own token, reacted relative to Bitcoin.

## Results

| Window | CAR | t |
|---|---|---|
| Day 0 (29 Oct) | −5.34% | −3.75 |
| [0, +1] | −3.94% | −1.95 |
| [−1, +1] | −2.43% | −0.98 |
| [0, +5] | −5.15% | −1.48 |
| [0, +7] | −5.17% | −1.28 |

- On the day, BNB fell 8.2% while Bitcoin fell 4.2% (simple price changes). With β = 0.75, the abnormal log return is −5.3%, the most negative abnormal day in the previous 12 months.
- With a market cap of about $99.8bn, that is roughly $5.3bn of value lost beyond the market move.
- Only day 0 is statistically significant. A week later (day +7) the cumulative gap was about −5.2% (t ≈ −1.3).

## Caveats

- Bitcoin itself fell 4.2% that day, partly because of the hack. If the hack moved the benchmark too, the market model understates the full effect.
- Daily data at 00:00 UTC: day 0 covers 29 Oct 00:00 to 30 Oct 00:00 UTC, which includes the hack (about 20:05 UTC).

`results/abnormal_returns.csv` holds the daily returns and abnormal returns for days −10 to +10 (as far as data exists).
