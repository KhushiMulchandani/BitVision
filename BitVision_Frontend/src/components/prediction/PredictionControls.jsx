import "./PredictionControls.css";

function PredictionControls() {
  return (
    <div className="prediction-controls">

      <div className="controls-header">

        <span className="controls-badge">
          AI Configuration
        </span>

        <h2>Prediction Setup</h2>

        <p>
          Configure your forecasting preferences before
          generating a prediction.
        </p>

      </div>

      <div className="control-group">

        <label>Forecast Horizon</label>

        <select>
          <option>1 Day</option>
          <option>7 Days</option>
          <option>30 Days</option>
        </select>

      </div>

      <div className="control-group">

        <label>AI Model</label>

        <select>
          <option>Ensemble Model</option>
          <option>Random Forest</option>
          <option>XGBoost</option>
          <option>LSTM</option>
        </select>

      </div>

      <div className="control-group">

        <label>Historical Data</label>

        <select>
          <option>30 Days</option>
          <option selected>90 Days</option>
          <option>180 Days</option>
          <option>365 Days</option>
        </select>

      </div>

      <div className="control-group">

        <label>Prediction Date</label>

        <input type="date" />

      </div>

      <button className="generate-btn">
        Generate Prediction
      </button>

    </div>
  );
}

export default PredictionControls;