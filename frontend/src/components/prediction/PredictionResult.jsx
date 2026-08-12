import React, { useState, useEffect } from "react";
import "./PredictionResult.css";
import {
  FiActivity,
  FiTrendingUp,
  FiShield,
  FiCpu,
  FiClock,
} from "react-icons/fi";

function PredictionResult() {
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/predict/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch live prediction data.");
        }
        return res.json();
      })
      .then((data) => {
        setPredictionData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <aside className="prediction-summary">
        <div className="summary-header">
          <h2>Prediction Summary</h2>
          <p>Loading live AI market prediction...</p>
        </div>
      </aside>
    );
  }

  if (error || !predictionData) {
    return (
      <aside className="prediction-summary">
        <div className="summary-header">
          <h2>Prediction Summary</h2>
          <p className="error-text">Unable to load prediction. Run evaluation command.</p>
        </div>
      </aside>
    );
  }

  const confidencePercent = Math.round((predictionData.confidence || 0.85) * 100);
  const isBullish = predictionData.predicted_price > 0; // Or adjust based on your comparison logic

  return (
    <aside className="prediction-summary">
      <div className="summary-header">
        <div>
          <h2>Prediction Summary</h2>
          <p>Live AI market prediction for {predictionData.date}</p>
        </div>
        <span className="live-badge">Live</span>
      </div>

      <div className="summary-table">
        <div className="summary-row">
          <div className="summary-label">
            <FiActivity />
            <span>Confidence</span>
          </div>
          <strong>{confidencePercent}%</strong>
        </div>

        <div className="summary-row">
          <div className="summary-label">
            <FiTrendingUp />
            <span>Trend</span>
          </div>
          <strong className={isBullish ? "positive" : "negative"}>
            {isBullish ? "Bullish" : "Bearish"}
          </strong>
        </div>

        <div className="summary-row">
          <div className="summary-label">
            <FiShield />
            <span>Risk</span>
          </div>
          <strong className="warning">Moderate</strong>
        </div>

        <div className="summary-row">
          <div className="summary-label">
            <FiCpu />
            <span>AI Model</span>
          </div>
          <strong>{predictionData.model_used.toUpperCase()}</strong>
        </div>
      </div>

      <div className="prediction-verdict">
        <div className="verdict-top">
          <span>Prediction Price</span>
          <span className="buy-pill">₹{predictionData.predicted_price.toLocaleString()}</span>
        </div>

        <div className="verdict-bottom">
          <div>
            <small>RSI (14)</small>
            <strong>{predictionData.indicators_used?.rsi_14 ?? "N/A"}</strong>
          </div>
          <div>
            <small>
              <FiClock /> Updated
            </small>
            <strong>{predictionData.date}</strong>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default PredictionResult;