import Navbar from "../components/landing/Navbar";
import "../components/models/Models.css";

import ModelsHeader from "../components/models/ModelsHeader";
import ModelComparison from "../components/models/ModelComparison";
import SelectedModel from "../components/models/SelectedModel";
import FeatureImportance from "../components/models/FeatureImportance";

function Models() {
  return (
    <>
      <Navbar />

      <main className="models-page">

        <ModelsHeader />

        <section className="models-dashboard">

          <div className="models-row">

            <ModelComparison />

            <SelectedModel />

          </div>

          <FeatureImportance />

        </section>

      </main>
    </>
  );
}

export default Models;