import "./PredictionWorkspace.css";

import PredictionControls from "./PredictionControls";
import PredictionResult from "./PredictionResult";

function PredictionWorkspace() {
  return (
    <section className="prediction-workspace">

      {/* Left Side */}

      <div className="workspace-left">

        <PredictionControls />

      </div>

      {/* Right Side */}

      <div className="workspace-right">

        <PredictionResult />

      </div>

    </section>
  );
}

export default PredictionWorkspace;