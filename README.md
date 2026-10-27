# Nifty 200 breakout backtest (open code, honest numbers)

A small, reproducible test of one simple idea on Indian stocks: **buy the first close above the previous 50-day closing high, ride it with a 3 x ATR trailing exit.** Educational research, not investment advice.

## Result (5 years, today's Nifty 200 list, 0.2% costs)

| | trades | profit trades | average per trade | median trade |
|---|---|---|---|---|
| 50-day-high closing breakout | 1,991 | 43% | **+4.24%** | -2.03% |
| Random entry, same exit rule (control) | 1,740 | 34% | +2.47% | -2.35% |

What this says, in plain words:
- The breakout beat random entry by about 1.8 percentage points per trade, and it won more often (43% vs 34%).
- **The typical (median) trade still lost about 2%.** The money came from a minority of big winners that the trailing exit let run. If you cannot sit through many small losses, this style is not for you.
- Run it yourself: `pip install yfinance pandas numpy` then `python breakout_backtest.py` (3-6 minutes).

## Other things we tested (same data family, earlier runs)

| Question | Finding |
|---|---|
| Intraday entry rules on 5m / 15m bars (EMA20 / EMA50 pullback, VWAP reclaim, opening-range breakout, previous-day-high retest), 59 days, 90 stocks | **None beat random entry** after 0.1% costs; win rates 27-34%. No "perfect EMA" for intraday timing. |
| Swing entry timing after a 50-day-high breakout: next-day open vs waiting for a retest vs waiting for a 1-ATR pullback | Next-day open +4.02% per signal; waiting for a retest +2.45% per signal; waiting for a pullback +1.62%. The best breakouts often never come back, so waiting cost return. |
| Weekly trend filter (weekly EMA20 > EMA50) | Breakouts with weekly uptrend +4.96% vs weekly downtrend +2.57%. Longer EMA pairs separated better than 9/21 or 10/30. |
| Midcap index above its 50 EMA | Breakouts +4.38% (43% profit trades) vs +2.40% (38%) when the Nifty Midcap 50 was below. Nifty itself above/below its 50 EMA made no difference. |

## Limits you should know

- **Survivorship bias:** today's Nifty 200 list, not the list from five years ago.
- **One regime:** mostly a rising market; a long bear market could look very different.
- No slippage model; daily bars only; costs fixed at 0.2%.
- Past results are not a promise. Small samples (the intraday test is only 59 days) are suggestions, not proof.

## More

- Free weekly lessons (we show our own real numbers, including the losses): https://ai360trading.in/tutorial-videos/
- Free calculators (SIP, EMI, tax, PPF, NPS and more): https://ai360trading.in/tools/
- Telegram: https://t.me/ai360trading

Built by AI360Trading. Not a SEBI-registered adviser. Educational use only.
