import "./TrendAnalysis.css";

function TrendAnalysis() {

  return (

    <section className="trend-analysis">

      {/* ================= HEADER ================= */}

      <div className="trend-header">

        <div>

          <h2>Trend Analysis</h2>

          <p>Real-time market decision panel</p>

        </div>

        <span className="live-tag">
          Live
        </span>

      </div>

      {/* ================= MARKET STATUS ================= */}

      <div className="trend-table">

        <div className="trend-row">

          <span>Market Trend</span>

          <strong className="green">
            Bullish ▲
          </strong>

        </div>

        <div className="trend-row">

          <span>Momentum</span>

          <strong>
            Strong
          </strong>

        </div>

        <div className="trend-row">

          <span>Volume</span>

          <strong>
            Increasing
          </strong>

        </div>

        <div className="trend-row">

          <span>Support</span>

          <strong>
            ₹96.8L
          </strong>

        </div>

        <div className="trend-row">

          <span>Resistance</span>

          <strong>
            ₹99.2L
          </strong>

        </div>

        <div className="trend-row">

          <span>Breakout</span>

          <strong className="orange">
            Possible
          </strong>

        </div>

      </div>

      {/* ================= AI VERDICT ================= */}

      <div className="verdict-card">

        <div className="verdict-top">

          <h3>

            AI Verdict

          </h3>

          <span className="buy-pill">

            BUY

          </span>

        </div>

        <div className="verdict-table">

          <div className="verdict-row">

            <span>Confidence</span>

            <strong>
              94%
            </strong>

          </div>

          <div className="verdict-row">

            <span>Risk</span>

            <strong className="orange">
              Medium
            </strong>

          </div>

          <div className="verdict-row">

            <span>Time Horizon</span>

            <strong>
              24 Hours
            </strong>

          </div>

          <div className="verdict-row">

            <span>Success Rate</span>

            <strong className="green">
              87%
            </strong>

          </div>

        </div>

        <div className="powered-by">

          Powered by <span>BitVision AI</span>

        </div>

      </div>

    </section>

  );

}

export default TrendAnalysis;