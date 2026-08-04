import { FaBrain } from "react-icons/fa";
import "./PredictionHeader.css";
function PredictionHeader() {
  return (
    <section className="prediction-header">

      <div className="prediction-badge">
        <FaBrain />
        <span>AI Prediction Workspace</span>
      </div>

      <h1>
        Bitcoin Price
        <span> Prediction</span>
      </h1>

      <p>
        Forecast Bitcoin prices using an Ensemble AI model powered by
        Random Forest, XGBoost and LSTM. Analyze predictions,
        confidence scores and market trends in one place.
      </p>

    </section>
  );
}

export default PredictionHeader;