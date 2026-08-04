import Navbar from "../components/landing/Navbar";
import LiveTicker from "../components/landing/LiveTicker";
import Hero from "../components/landing/Hero";
import Features from "../components/landing/Features";
import Footer from "../components/landing/Footer";
import Background from "../components/common/Background";
import Stats from "../components/landing/Stats";

function LandingPage() {
  return (
    <>
      <Background/>

<Navbar/>

<LiveTicker/>

<Hero/>

<Stats />

<Features/>

<Footer/>
    </>
  );
}

export default LandingPage;