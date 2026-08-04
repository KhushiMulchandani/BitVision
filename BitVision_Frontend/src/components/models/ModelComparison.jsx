import "./ModelComparison.css";
import {
  FiCpu,
  FiCheckCircle,
  FiStar,
} from "react-icons/fi";

const models = [
  {
    name: "Random Forest",
    score: "95.4%",
    status: "Active",
  },
  {
    name: "XGBoost",
    score: "94.8%",
    status: "Active",
  },
  {
    name: "LSTM",
    score: "93.7%",
    status: "Ready",
  },
  {
    name: "GRU",
    score: "92.6%",
    status: "Ready",
  },
  {
    name: "Ensemble",
    score: "96.1%",
    status: "Best",
  },
];

function ModelComparison() {
  return (
    <section className="model-comparison">

      <div className="comparison-header">

        <div>

          <h2>Model Comparison</h2>

          <p>
            Compare available machine learning models.
          </p>

        </div>

        <span className="comparison-badge">
          Live
        </span>

      </div>

      <div className="comparison-table">

        <div className="comparison-head">

          <span>Model</span>

          <span>Score</span>

          <span>Status</span>

        </div>

        {models.map((model) => (

          <div
            className={`comparison-row ${
              model.status === "Best" ? "active-model" : ""
            }`}
            key={model.name}
          >

            <div className="model-name">

              <FiCpu />

              {model.name}

            </div>

            <strong>{model.score}</strong>

            <div className="model-status">

              {model.status === "Best" ? (

                <span className="best">

                  <FiStar />

                  Best

                </span>

              ) : (

                <span>

                  <FiCheckCircle />

                  {model.status}

                </span>

              )}

            </div>

          </div>

        ))}

      </div>

    </section>
  );
}

export default ModelComparison;