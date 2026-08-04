import "./SelectedModel.css";

import {
  FiCpu,
  FiActivity,
  FiTarget,
  FiTrendingUp,
  FiClock,
} from "react-icons/fi";

function SelectedModel() {
  return (
    <section className="selected-model-card">

      <div className="selected-header">

        <div>

          <h2>Model Performance</h2>

          <p>
            Performance of the currently deployed AI model.
          </p>

        </div>

        <span className="selected-badge">
          Best Model
        </span>

      </div>

      <div className="selected-model">

        <FiCpu className="selected-icon" />

        <div>

          <h3>Ensemble Learning</h3>

          <span>Production Model</span>

        </div>

      </div>

      <div className="performance-table">

        <div className="performance-row">

          <div className="performance-title">

            <FiActivity />

            <span>Accuracy</span>

          </div>

          <strong>96.1%</strong>

        </div>

        <div className="performance-row">

          <div className="performance-title">

            <FiTarget />

            <span>Precision</span>

          </div>

          <strong>95.6%</strong>

        </div>

        <div className="performance-row">

          <div className="performance-title">

            <FiTrendingUp />

            <span>Recall</span>

          </div>

          <strong>95.2%</strong>

        </div>

        <div className="performance-row">

          <div className="performance-title">

            <FiClock />

            <span>Prediction Time</span>

          </div>

          <strong>0.18 sec</strong>

        </div>

      </div>

      <div className="model-footer">

        <span>Deployment</span>

        <strong>Final Bitcoin Prediction</strong>

      </div>

    </section>
  );
}

export default SelectedModel;