import Navbar from "../components/landing/Navbar";

import PredictionHeader from "../components/prediction/PredictionHeader";
import PredictionWorkspace from "../components/prediction/PredictionWorkspace";
import MarketOverview from "../components/prediction/MarketOverview";
import PredictionTable from "../components/prediction/PredictionTable";
import PredictionInsights from "../components/prediction/PredictionInsights";

import "../components/prediction/Prediction.css";

function Prediction() {
  return (
    <>
      <Navbar />

      <main className="prediction-page">

        <PredictionHeader />

        <PredictionWorkspace />

        <MarketOverview />

        <PredictionTable />

        <PredictionInsights />

      </main>
    </>
  );
}

export default Prediction;