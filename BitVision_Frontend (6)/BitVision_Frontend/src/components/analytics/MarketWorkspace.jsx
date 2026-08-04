import "./MarketWorkspace.css";

import {
  FaBitcoin,
  FaBrain,
  FaArrowTrendUp,
} from "react-icons/fa6";

function MarketWorkspace() {
  return (
    <section className="market-workspace">

      {/* ================= LEFT ================= */}

      <div className="featured-card">

        <div className="featured-top">

          <div className="coin-info">

            <div className="coin-icon">
              <FaBitcoin />
            </div>

            <div>

              <h3>Bitcoin (BTC)</h3>

              <span>Live Market</span>

            </div>

          </div>

          <div className="change-box">

            <span className="positive">
              ▲ +2.56%
            </span>

            <small>Today</small>

          </div>

        </div>

        {/* Price */}

        <div className="price-row">

          <h1>₹98,56,450</h1>

        </div>

        {/* Compact Stats */}

        <div className="price-stats">

          <div>

            <span>High</span>

            <strong className="green">
              ₹99.2L
            </strong>

          </div>

          <div>

            <span>Low</span>

            <strong className="red">
              ₹96.8L
            </strong>

          </div>

          <div>

            <span>Volume</span>

            <strong>
              ₹1.84T
            </strong>

          </div>

        </div>

        {/* Sparkline */}

        <div className="sparkline">

          <svg
            viewBox="0 0 900 90"
            className="market-line"
          >

            <defs>

              <linearGradient
                id="marketGradient"
                x1="0%"
                x2="100%"
              >

                <stop
                  offset="0%"
                  stopColor="#5FA777"
                />

                <stop
                  offset="100%"
                  stopColor="#16C784"
                />

              </linearGradient>

            </defs>

            <polyline

              fill="none"

              stroke="url(#marketGradient)"

              strokeWidth="4"

              strokeLinecap="round"

              strokeLinejoin="round"

              points="
              0,70
              90,60
              180,64
              270,40
              360,45
              450,22
              540,34
              630,18
              720,25
              810,10
              900,3
              "

            />

          </svg>

        </div>

      </div>

      {/* ================= RIGHT ================= */}

      <div className="metrics-panel">

        <div className="metrics-header">

          <FaBrain />

          <h3>Market Metrics</h3>

        </div>

        <div className="metric-row">

          <span>AI Accuracy</span>

          <strong className="green">
            94%
          </strong>

        </div>

        <div className="metric-row">

          <span>24H Volume</span>

          <strong>
            ₹1.84T
          </strong>

        </div>

        <div className="metric-row">

          <span>Volatility</span>

          <strong className="orange">
            Medium
          </strong>

        </div>

        <div className="metric-row">

          <span>Fear Index</span>

          <strong>
            74
          </strong>

        </div>

        <div className="metric-row">

          <span>Market Trend</span>

          <strong className="green">

            <FaArrowTrendUp />

            Bullish

          </strong>

        </div>

        <div className="metric-row">

          <span>Confidence</span>

          <strong className="green">
            High
          </strong>

        </div>

        <div className="metrics-footer">

          Updated 2 mins ago

        </div>

      </div>

    </section>
  );
}

export default MarketWorkspace;