"""
50-day closing-high breakout on Nifty 200 stocks: a small, honest backtest (educational, not advice).

Rule tested
  Signal : a stock's close is above the highest close of the previous 50 sessions (first such close).
  Entry  : next session's open.
  Exit   : close below max(stop, highest close since entry - 3 x ATR14) -> exit at the next open.
           Initial stop = lower of the 20-day low, but never more than 12% below the entry. Max hold 120 sessions.
  Costs  : 0.2% round trip.
  Control: the SAME exit rule applied to random entry days (same stocks, same period).

Run:  pip install yfinance pandas numpy
      python breakout_backtest.py            (about 3-6 minutes, downloads 5 years of daily data)

Limits (read them): survivorship bias (today's Nifty 200 list, not the list of 5 years ago), one market regime
(mostly a rising market), no slippage model, daily bars only. Results are history, not a promise.
"""
import warnings
import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
SYMS = [s.strip() for s in open("nifty200_symbols.txt") if s.strip()]
TK = [s + ".NS" for s in SYMS]
COST = 0.2
rng = np.random.RandomState(7)


def atr14(h, l, c):
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / 14, adjust=False).mean()


def trade(o, l, c, a, i, n):
    """Enter at the open of bar i+1, return % return after costs and the exit index."""
    entry = o.iloc[i + 1]
    stop = max(l.iloc[max(0, i - 19):i + 1].min(), entry * 0.88)
    hh, j, exit_px = c.iloc[i], i + 1, None
    while j < n and j - i <= 120:
        hh = max(hh, c.iloc[j])
        if c.iloc[j] < max(stop, hh - 3 * a.iloc[j]) and j + 1 < n:
            exit_px = o.iloc[j + 1]
            return (exit_px / entry - 1) * 100 - COST, j + 1
        j += 1
    jl = min(j, n - 1)
    return (c.iloc[jl] / entry - 1) * 100 - COST, jl


def main():
    data = yf.download(TK, period="5y", interval="1d", group_by="ticker", auto_adjust=False, progress=False, threads=True)
    brk, ctl = [], []
    for s in TK:
        try:
            d = data[s].dropna()
        except Exception:
            continue
        if len(d) < 300:
            continue
        o, h, l, c = d.Open, d.High, d.Low, d.Close
        a = atr14(h, l, c)
        n = len(d)
        hi50 = c.shift(1).rolling(50).max()
        sig = ((c > hi50) & (c.shift(1) <= hi50.shift(1))).values
        busy = -1
        for i in np.where(sig)[0]:
            if i < 200 or i <= busy or i + 1 >= n:
                continue
            r, busy = trade(o, l, c, a, i, n)
            brk.append(r)
        # control: random entry days, same exit rule, no overlap
        days = sorted(rng.choice(np.arange(200, n - 2), size=min(12, n - 202), replace=False))
        busy = -1
        for i in days:
            if i <= busy:
                continue
            r, busy = trade(o, l, c, a, i, n)
            ctl.append(r)

    def rep(name, x):
        x = np.array(x)
        print(f"{name:26s} trades={len(x):5d}  profit trades={(x > 0).mean() * 100:4.0f}%  avg={x.mean():+.2f}%  median={np.median(x):+.2f}%")

    print("5 years, Nifty 200 (today's list), costs 0.2%, exit = 3xATR trail")
    rep("50-day-high breakout", brk)
    rep("random entry (control)", ctl)


if __name__ == "__main__":
    main()
