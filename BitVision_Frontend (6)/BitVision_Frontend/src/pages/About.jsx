import Navbar from "../components/landing/Navbar";
import "../components/about/About.css";

import AboutHeader from "../components/about/AboutHeader";
import Mission from "../components/about/Mission";
import PredictionPipeline from "../components/about/PredictionPipeline";
import Roadmap from "../components/about/Roadmap";

function About() {

  return (

    <>

      <Navbar />

      <main className="about-page">

        <AboutHeader />

        <section className="about-dashboard">

          <Mission />

          <PredictionPipeline />

          <Roadmap />

        </section>

      </main>

    </>

  );

}

export default About;