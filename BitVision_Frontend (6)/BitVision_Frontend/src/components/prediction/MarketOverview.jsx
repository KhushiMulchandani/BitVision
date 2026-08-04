import "./MarketOverview.css";

import {
  FaArrowTrendUp,
  FaArrowTrendDown,
  FaChartLine,
  FaRobot,
  FaChartSimple,
} from "react-icons/fa6";

function MarketOverview() {
  return (
    <section className="market-overview">

      <div className="market-header">

        <div>

          <span className="market-badge">
            Live Market
          </span>

          <h2>Market Overview</h2>

          <p>
            Monitor Bitcoin trends with AI-powered market insights.
          </p>

        </div>

      </div>

      <div className="market-grid">

        {/* LEFT */}

        <div className="chart-card">

          <div className="chart-top">

            <div>

              <h3>Bitcoin (BTC)</h3>

              <span>Last 30 Days</span>

            </div>

            <div className="chart-price">

              ₹98,56,450

              <small className="trend-up">
                ▲ +2.56%
              </small>

            </div>

          </div>

          <div className="chart-area">

            <svg
              viewBox="0 0 900 300"
              className="market-chart"
            >

              <polyline
                className="chart-green"
                points="
                0,210
                90,180
                180,190
                260,130
                340,145
                430,100
                "
              />

              <polyline
                className="chart-red"
                points="
                430,100
                520,145
                600,120
                "
              />

              <polyline
                className="chart-green"
                points="
                600,120
                700,90
                800,70
                900,40
                "
              />

            </svg>

          </div>

          <div className="chart-bottom">

            <div>

              <h4>Volume</h4>

              <span>₹1.84T</span>

            </div>

            <div>

              <h4>High</h4>

              <span className="positive">
                ₹99.2L
              </span>

            </div>

            <div>

              <h4>Low</h4>

              <span className="negative">
                ₹96.8L
              </span>

            </div>

          </div>

        </div>

        {/* RIGHT */}

        <div className="market-side">

          <div className="overview-card">

            <FaChartLine />

            <h4>Confidence</h4>

            <h2>94%</h2>

          </div>

          <div className="overview-card">

            <FaArrowTrendUp />

            <h4>Trend</h4>

            <h2 className="positive">
              Bullish
            </h2>

          </div>

          <div className="overview-card">

            <FaArrowTrendDown />

            <h4>Risk</h4>

            <h2 className="negative">
              Moderate
            </h2>

          </div>

          <div className="overview-card">

            <FaRobot />

            <h4>AI Model</h4>

            <h2>Ensemble</h2>

          </div>

        </div>

      </div>

    </section>
  );
}

export default MarketOverview;