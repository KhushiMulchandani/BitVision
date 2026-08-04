import "./Mission.css";

import {
  FiTarget,
  FiMonitor,
  FiCpu,
  FiCheckCircle,
  FiCode,
  FiDatabase,
  FiLayers,
  FiBarChart2,
} from "react-icons/fi";

function Mission() {
  return (
    <section className="mission-grid">

      {/* Mission */}

      <div className="mission-card">

        <div className="card-header">

          <h2>Our Mission</h2>

          <span>Vision</span>

        </div>

        <div className="mission-list">

          <div>

            <FiTarget />

            <span>Deliver accurate Bitcoin predictions.</span>

          </div>

          <div>

            <FiMonitor />

            <span>Provide real-time market analytics.</span>

          </div>

          <div>

            <FiCpu />

            <span>Build transparent AI-driven insights.</span>

          </div>

          <div>

            <FiCheckCircle />

            <span>Help users make informed decisions.</span>

          </div>

        </div>

      </div>

      {/* Technology */}

      <div className="mission-card">

        <div className="card-header">

          <h2>Technology Stack</h2>

          <span>Platform</span>

        </div>

        <div className="tech-list">

          <div>

            <FiCode />

            <span>React.js</span>

          </div>

          <div>

            <FiLayers />

            <span>Django</span>

          </div>

          <div>

            <FiCpu />

            <span>Python</span>

          </div>

          <div>

            <FiDatabase />

            <span>SQLite</span>

          </div>

          <div>

            <FiBarChart2 />

            <span>Recharts</span>

          </div>

        </div>

      </div>

    </section>
  );
}

export default Mission;