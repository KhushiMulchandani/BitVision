"""Unit tests for the pure ML helpers (no database, TensorFlow or network needed)."""
import unittest

import numpy as np
import pandas as pd

from ml.features import (
    SEQ_LEN, TAB_FEATURES, SEQ_FEATURES, build_frame, make_windows, split_indices,
    compute_metrics, baseline_metrics, interval_from_return, interval_coverage,
)


def _fake_frames(n=200, seed=0):
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    dates = pd.date_range("2020-01-01", periods=n).date
    ohlcv = pd.DataFrame({"date": dates, "open": close, "high": close * 1.01, "low": close * 0.99,
                          "close": close, "volume": rng.integers(1_000, 5_000, n)})
    s = pd.Series(close)
    feat = pd.DataFrame({
        "date": dates, "rsi_14": 50.0, "macd": 0.1, "macd_signal": 0.1,
        "ma_20": s.rolling(20).mean(), "ma_50": s.rolling(50).mean(),
        "bollinger_upper": s.rolling(20).mean() * 1.05, "bollinger_lower": s.rolling(20).mean() * 0.95,
        "fg_index": None, "lag_1": s.shift(1), "lag_7": s.shift(7),
    })
    return ohlcv, feat


class FeatureTests(unittest.TestCase):
    def test_frame_has_all_inputs_and_no_nans(self):
        df = build_frame(*_fake_frames())
        self.assertFalse(df[TAB_FEATURES + SEQ_FEATURES].isna().any().any())
        self.assertTrue(np.isnan(df["target_return"].iloc[-1]))          # today has no label
        self.assertFalse(df["target_return"].iloc[:-1].isna().any())

    def test_empty_fear_greed_becomes_neutral(self):
        df = build_frame(*_fake_frames())
        self.assertTrue((df["fg_norm"] == 0).all())

    def test_target_is_next_day_return(self):
        df = build_frame(*_fake_frames())
        i = 10
        self.assertAlmostEqual(df["target_return"].iloc[i], df["close"].iloc[i + 1] / df["close"].iloc[i] - 1)

    def test_window_ends_on_today_and_aligns_with_target(self):
        values = np.arange(100, dtype=float).reshape(-1, 1)
        windows, t = make_windows(values, 60)
        self.assertEqual(windows.shape, (41, 60, 1))
        self.assertEqual(t[0], 59)
        for k in (0, 17, 40):
            self.assertEqual(windows[k][-1, 0], values[t[k], 0])         # last step is day t, not t+1
            self.assertEqual(windows[k][0, 0], values[t[k] - 59, 0])

    def test_split_is_chronological(self):
        a, b = split_indices(1000)
        self.assertEqual((a, b), (700, 850))

    def test_baseline_has_zero_return_error_floor(self):
        y = np.array([101.0, 99.0, 100.0]); cur = np.array([100.0, 100.0, 100.0])
        m = baseline_metrics(y, cur)
        self.assertAlmostEqual(m["mae"], 2 / 3, places=2)
        self.assertAlmostEqual(m["directional_accuracy"], 33.33, places=1)  # share of up days

    def test_directional_accuracy(self):
        y = np.array([101.0, 99.0]); cur = np.array([100.0, 100.0])
        self.assertEqual(compute_metrics(y, np.array([102.0, 98.0]), cur)["directional_accuracy"], 100.0)
        self.assertEqual(compute_metrics(y, np.array([98.0, 102.0]), cur)["directional_accuracy"], 0.0)

    def test_interval(self):
        price, lo, hi = interval_from_return(100.0, 0.01, 0.02, z=1.0)
        self.assertAlmostEqual(price, 101.0); self.assertAlmostEqual(lo, 99.0); self.assertAlmostEqual(hi, 103.0)
        self.assertEqual(interval_coverage([0.0, 0.05], [0.0, 0.0], 0.02, z=1.0), 0.5)


if __name__ == "__main__":
    unittest.main()
