# Event Window

One market event, measured. Each issue takes a news event and runs a short event study on it: what did the market actually price, beyond the normal market move?

The method is the one from my M1 thesis (market model, estimation window [-200, -20], abnormal returns and t-statistics). Every issue has its own folder with the code and the results, so anyone can re-run it.

| Nº | Date | Event | Main result |
|---|---|---|---|
| 01 | 10 Nov 2026 | [Binance hack, 29 Oct 2026](01-binance-hack) | BNB abnormal return −5.3% on the day (t = −3.75), about $5.3bn of market value |
| 02 | 17 Nov 2026 | [Nvidia CEO news, Oct–Nov 2026](02-nvidia-key-person) | NVDA abnormal return −13.7% vs chip peers on 9–10 Nov (t = −4.7), about $580bn of market value |
| 03 | 24 Nov 2026 | [Anthropic IPO: the first-trade buyers](03-anthropic-ipo) | First trade ($111.50) to day-3 close −21.4% (−18.4% net of the Nasdaq-100), 2nd worst of 12 large US IPOs since 2008 |

## Method in one paragraph

Expected return comes from a market model, `R_asset = α + β · R_market`, estimated on the 180 trading days that end 20 days before the event. The abnormal return is the actual return minus the expected one. Cumulative abnormal returns (CAR) add these up over a window, and the t-statistic divides the CAR by the estimation-window residual volatility times the square root of the window length. For crypto assets the market benchmark is Bitcoin. New listings (Nº03) have no estimation window, so they use market-adjusted returns (β = 1), the standard choice in IPO studies.

## Run it

```bash
pip install -r requirements.txt
python 01-binance-hack/event_study.py
cd 02-nvidia-key-person && python event_study.py
cd ../03-anthropic-ipo && python ipo_first_trade.py
```

Nº01 downloads its prices from the CoinGecko public API at run time. Nº02 ships its Yahoo Finance prices in `02-nvidia-key-person/data/`. Nº03 downloads Yahoo Finance prices at run time and ships a copy in `03-anthropic-ipo/data/`.

## Author

Davide Pellegrino · M2 Financial Economics, Université Paris 1 Panthéon-Sorbonne · [LinkedIn](https://www.linkedin.com/in/pellegrino-davide/)

Related: [Sanctions and privacy coins (M1 thesis)](https://github.com/davidepellegrino-stack/sanctions-privacy-coins)
