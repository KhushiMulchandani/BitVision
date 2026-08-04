import "./Hero.css";
import { ArrowRight } from "lucide-react";

function Hero() {
  return (
    <section className="hero">

      {/* LEFT SIDE */}

      <div className="hero-content">

        <span className="hero-badge">
          AI Powered Bitcoin Forecasting
        </span>

        <h1 className="hero-title">
          Predict the Future of
          <br />
          <span className="bitcoin-gradient">
            Bitcoin
          </span>{" "}
          with
          <br />
          Artificial Intelligence.
        </h1>

        <p className="hero-description">
          Harness machine learning, technical indicators and
          real-time market intelligence to forecast Bitcoin
          prices with confidence.
        </p>

        <div className="hero-buttons">

          <button className="btn-primary">
            Get Started
          </button>

          <button className="btn-secondary">
            Explore
            <ArrowRight size={18}/>
          </button>

        </div>

        <div className="hero-stats">

          <div className="hero-stat">
            <h3>95%</h3>
            <span>Prediction Accuracy</span>
          </div>

          <div className="hero-stat">
            <h3>5+</h3>
            <span>AI Models</span>
          </div>

          <div className="hero-stat">
            <h3>24/7</h3>
            <span>Market Monitoring</span>
          </div>

        </div>

      </div>

      {/* RIGHT SIDE */}

      <div className="hero-visual">

        <div className="forecast-card">

          <div className="forecast-header">

            <div className="forecast-left">

              <div className="live-badge">

                <span className="live-dot"></span>

                LIVE AI FORECAST

              </div>

              <p className="forecast-label">
                Bitcoin Price
              </p>

              <h2 className="forecast-price">
                ₹98,56,450
              </h2>

            </div>

            <div className="forecast-growth">

              ▲ +2.56%

            </div>

          </div>

          {/* GRAPH */}

          <div className="graph-area">

            <svg
              className="graph-svg"
              viewBox="0 0 600 260"
              preserveAspectRatio="none"
            >

              <defs>

                <linearGradient
                  id="graphGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >

                  <stop
                    offset="0%"
                    stopColor="#5FA777"
                  />

                  <stop
                    offset="100%"
                    stopColor="#18C964"
                  />

                </linearGradient>

              </defs>

              <path
                d="
                M20 220
                L80 205
                L140 165
                L200 178
                L260 135
                L320 148
                L380 96
                L440 112
                L500 70
                L580 35
                "
                fill="none"
                stroke="url(#graphGradient)"
                strokeWidth="6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />

              <circle
                cx="580"
                cy="35"
                r="8"
                fill="#18C964"
              />

            </svg>

          </div>

          {/* FOOTER */}

          <div className="forecast-footer">

            <div className="confidence-box">

              <div className="confidence-top">

                <span>AI Confidence</span>

                <strong>95%</strong>

              </div>

              <div className="progress-bar">

                <div className="progress-fill"></div>

              </div>

            </div>

            <div className="forecast-row">

              <span>Market Trend</span>

              <strong className="bullish">

                🟢 Bullish

              </strong>

            </div>

            <div className="forecast-row">

              <span>Best Model</span>

              <strong>

                Ensemble AI

              </strong>

            </div>

            <div className="forecast-row">

              <span>Updated</span>

              <strong>

                Just now

              </strong>

            </div>

          </div>

        </div>

      </div>

    </section>
  );
}

export default Hero;