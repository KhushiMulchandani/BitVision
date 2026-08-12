import React, { useState } from "react";
import "./PredictionControls.css";

function PredictionControls({ onRefresh }) {
  const [horizon, setHorizon] = useState("1 Day");
  const [model, setModel] = useState("lstm");
  const [history, setHistory] = useState("90 Days");

  const handleGenerate = (e) => {
    e.preventDefault();
    // Trigger callback or fetch fresh evaluation parameters if desired
    if (onRefresh) {
      onRefresh({ horizon, model, history });
    }
  };

  return (
    <div className="prediction-controls">
      <div className="controls-header">
        <span className="controls-badge">AI Configuration</span>
        <h2>Prediction Setup</h2>
        <p>Configure your forecasting preferences before generating a prediction.</p>
      </div>

      <form onSubmit={handleGenerate}>
        <div className="control-group">
          <label>Forecast Horizon</label>
          <select value={horizon} onChange={(e) => setHorizon(e.target.value)}>
            <option>1 Day</option>
            <option>7 Days</option>
            <option>30 Days</option>
          </select>
        </div>

        <div className="control-group">
          <label>AI Model</label>
          <select value={model} onChange={(e) => setModel(e.target.value)}>
            <option value="stacked">Ensemble Model</option>
            <option value="xgb">XGBoost</option>
            <option value="lstm">LSTM</option>
          </select>
        </div>

        <div className="control-group">
          <label>Historical Data</label>
          <select value={history} onChange={(e) => setHistory(e.target.value)}>
            <option>30 Days</option>
            <option>90 Days</option>
            <option>180 Days</option>
            <option>365 Days</option>
          </select>
        </div>

        <button type="submit" className="generate-btn">
          Generate Prediction
        </button>
      </form>
    </div>
  );
}

export default PredictionControls;