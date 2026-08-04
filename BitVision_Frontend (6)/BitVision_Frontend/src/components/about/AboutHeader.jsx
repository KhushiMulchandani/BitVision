import "./AboutHeader.css";

import {
  FiCpu,
  FiTrendingUp,
  FiShield,
} from "react-icons/fi";

function AboutHeader() {
  return (
    <section className="about-header">

      <div className="about-left">

        <span className="about-badge">
          AI Powered Platform
        </span>

        <h1>About BitVision</h1>

        <p>
          BitVision is an AI-powered Bitcoin intelligence platform that
          combines machine learning, technical analysis, and real-time
          market insights to deliver explainable cryptocurrency predictions.
        </p>

      </div>

      <div className="about-right">

        <div className="about-stat">

          <FiCpu />

          <div>

            <h3>5+</h3>

            <span>AI Models</span>

          </div>

        </div>

        <div className="about-stat">

          <FiTrendingUp />

          <div>

            <h3>95%</h3>

            <span>Prediction Accuracy</span>

          </div>

        </div>

        <div className="about-stat">

          <FiShield />

          <div>

            <h3>Real-Time</h3>

            <span>Market Analytics</span>

          </div>

        </div>

      </div>

    </section>
  );
}

export default AboutHeader;