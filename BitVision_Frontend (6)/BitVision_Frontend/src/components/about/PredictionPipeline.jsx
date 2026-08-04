import "./PredictionPipeline.css";

import {
  FiDatabase,
  FiFilter,
  FiLayers,
  FiCpu,
  FiTrendingUp,
  FiMonitor,
} from "react-icons/fi";

const pipeline = [
  {
    icon: <FiDatabase />,
    title: "Market Data",
    desc: "Bitcoin prices & market history",
  },
  {
    icon: <FiFilter />,
    title: "Data Processing",
    desc: "Cleaning & preprocessing",
  },
  {
    icon: <FiLayers />,
    title: "Feature Engineering",
    desc: "Technical indicators",
  },
  {
    icon: <FiCpu />,
    title: "AI Models",
    desc: "ML prediction engine",
  },
  {
    icon: <FiTrendingUp />,
    title: "Prediction",
    desc: "Forecast generation",
  },
  {
    icon: <FiMonitor />,
    title: "Dashboard",
    desc: "Visual insights",
  },
];

function PredictionPipeline() {
  return (
    <section className="pipeline-card">

      <div className="pipeline-header">

        <div>

          <h2>Prediction Pipeline</h2>

          <p>
            The workflow followed by BitVision to generate Bitcoin predictions.
          </p>

        </div>

        <span className="pipeline-badge">
          Workflow
        </span>

      </div>

      <div className="pipeline-flow">

        {pipeline.map((step, index) => (

          <div
            className="pipeline-step"
            key={step.title}
          >

            <div className="step-icon">
              {step.icon}
            </div>

            <h4>{step.title}</h4>

            <span>{step.desc}</span>

            {index !== pipeline.length - 1 && (
              <div className="pipeline-arrow">
                →
              </div>
            )}

          </div>

        ))}

      </div>

    </section>
  );
}

export default PredictionPipeline;