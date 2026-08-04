import "./Stats.css";

import {
  Target,
  BrainCircuit,
  TrendingUp,
  Rocket,
} from "lucide-react";

const stats = [
  {
    icon: <Target size={24} />,
    title: "Accuracy",
    value: "95%",
    description: "AI Prediction Success",
  },
  {
    icon: <BrainCircuit size={24} />,
    title: "AI Models",
    value: "5+",
    description: "Ensemble Learning",
  },
  {
    icon: <TrendingUp size={24} />,
    title: "Market Analysis",
    value: "24/7",
    description: "Real-time Monitoring",
  },
  {
    icon: <Rocket size={24} />,
    title: "Forecasts",
    value: "10K+",
    description: "Predictions Generated",
  },
];

function Stats() {
  return (
    <section className="stats">

      <div className="stats-grid">

        {stats.map((item) => (

          <div
            className="stats-card"
            key={item.title}
          >

            <div className="stats-icon">
              {item.icon}
            </div>

            <span className="stats-title">
              {item.title}
            </span>

            <h2>
              {item.value}
            </h2>

            <p>
              {item.description}
            </p>

          </div>

        ))}

      </div>

    </section>
  );
}

export default Stats;