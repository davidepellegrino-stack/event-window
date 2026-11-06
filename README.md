# Event Window

One market event, measured. Each issue takes a news event and runs a short event study on it: what did the market actually price, beyond the normal market move?

The method is the one from my M1 thesis (market model, estimation window [-200, -20], abnormal returns and t-statistics). Every issue has its own folder with the code and the results, so anyone can re-run it.

| Nº | Date | Event | Main result |
|---|---|---|---|
| 01 | 10 Nov 2026 | [Binance hack, 29 Oct 2026](01-binance-hack) | BNB abnormal return −5.3% on the day (t = −3.75), about $5.3bn of market value |

## Method in one paragraph

Expected return comes from a market model, `R_asset = α + β · R_market`, estimated on the 180 trading days that end 20 days before the event. The abnormal return is the actual return minus the expected one. Cumulative abnormal returns (CAR) add these up over a window, and the t-statistic divides the CAR by the estimation-window residual volatility times the square root of the window length. For crypto assets the market benchmark is Bitcoin.

## Run it

```bash
pip install -r requirements.txt
python 01-binance-hack/event_study.py
```

Data comes from the CoinGecko public API at run time, so the raw prices are not stored in this repository.

## Author

Davide Pellegrino · M2 Financial Economics, Université Paris 1 Panthéon-Sorbonne · [LinkedIn](https://www.linkedin.com/in/pellegrino-davide/)

Related: [Sanctions and privacy coins (M1 thesis)](https://github.com/davidepellegrino-stack/sanctions-privacy-coins)
