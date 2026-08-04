import { Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import Prediction from "./pages/Prediction";
import Analytics from "./pages/Analytics";
import About from "./pages/About";
import Dashboard from "./pages/Dashboard";
import Portfolio from "./pages/Portfolio";
import News from "./pages/News";
import Settings from "./pages/Settings";
import Models from "./pages/Models";

function App() {
  return (
    <Routes>

      <Route path="/" element={<LandingPage />} />

      <Route path="/prediction" element={<Prediction />} />

      <Route path="/analytics" element={<Analytics />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/portfolio" element={<Portfolio />} />

      <Route path="/news" element={<News />} />

      <Route path="/settings" element={<Settings />} />

      <Route path="/models" element={<Models />} />

      <Route path="/about" element={<About />} />

    </Routes>
  );
}

export default App;