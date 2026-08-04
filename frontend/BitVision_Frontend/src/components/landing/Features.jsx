
import "./Features.css";
import {
  FaChartLine,
  FaBrain,
  FaShieldAlt
} from "react-icons/fa";

function Features() {
  return (
    <section className="features">

      <div className="section-title">

        <span>FEATURES</span>

        <h2>
          Everything you need for smarter Bitcoin forecasting.
        </h2>

      </div>

      <div className="feature-grid">

        <div className="feature-card">

          <div className="feature-icon">
            <FaBrain />
          </div>

          <h3>AI Prediction</h3>

          <p>
            Advanced ML models for highly accurate Bitcoin price forecasting.
          </p>

        </div>

        <div className="feature-card">

          <div className="feature-icon">
            <FaChartLine />
          </div>

          <h3>Live Analytics</h3>

          <p>
            Real-time market indicators and technical analysis in one place.
          </p>

        </div>

        <div className="feature-card">

          <div className="feature-icon">
            <FaShieldAlt />
          </div>

          <h3>Reliable Models</h3>

          <p>
            Ensemble AI combining Random Forest, XGBoost and LSTM.
          </p>

        </div>

      </div>

    </section>
  );
}

export default Features;