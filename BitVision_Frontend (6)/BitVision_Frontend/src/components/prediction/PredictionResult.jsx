import "./PredictionResult.css";
import {
  FiActivity,
  FiTrendingUp,
  FiShield,
  FiCpu,
  FiClock,
} from "react-icons/fi";

function PredictionResult() {
  return (
    <aside className="prediction-summary">

      <div className="summary-header">

        <div>

          <h2>Prediction Summary</h2>

          <p>Live AI market prediction</p>

        </div>

        <span className="live-badge">
          Live
        </span>

      </div>

      <div className="summary-table">

        <div className="summary-row">

          <div className="summary-label">

            <FiActivity />

            <span>Confidence</span>

          </div>

          <strong>94%</strong>

        </div>

        <div className="summary-row">

          <div className="summary-label">

            <FiTrendingUp />

            <span>Trend</span>

          </div>

          <strong className="positive">
            Bullish
          </strong>

        </div>

        <div className="summary-row">

          <div className="summary-label">

            <FiShield />

            <span>Risk</span>

          </div>

          <strong className="warning">
            Moderate
          </strong>

        </div>

        <div className="summary-row">

          <div className="summary-label">

            <FiCpu />

            <span>AI Model</span>

          </div>

          <strong>
            Ensemble
          </strong>

        </div>

      </div>

      <div className="prediction-verdict">

        <div className="verdict-top">

          <span>Prediction</span>

          <span className="buy-pill">
            BUY
          </span>

        </div>

        <div className="verdict-bottom">

          <div>

            <small>Expected Move</small>

            <strong>+2.56%</strong>

          </div>

          <div>

            <small>

              <FiClock />

              Updated

            </small>

            <strong>Live</strong>

          </div>

        </div>

      </div>

    </aside>
  );
}

export default PredictionResult;