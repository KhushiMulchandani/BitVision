import "./Roadmap.css";

import {
  FiWifi,
  FiBell,
  FiPieChart,
  FiSmartphone,
  FiGlobe,
  FiShield,
} from "react-icons/fi";

const roadmap = [

  {
    icon: <FiWifi />,
    title: "Live Exchange APIs",
    desc: "Real-time cryptocurrency market data.",
  },

  {
    icon: <FiBell />,
    title: "Smart Alerts",
    desc: "Instant price & prediction notifications.",
  },

  {
    icon: <FiPieChart />,
    title: "Portfolio Tracking",
    desc: "Monitor assets with AI insights.",
  },

  {
    icon: <FiSmartphone />,
    title: "Mobile Application",
    desc: "Native Android & iOS experience.",
  },

  {
    icon: <FiGlobe />,
    title: "Multi-Crypto Support",
    desc: "Expand beyond Bitcoin prediction.",
  },

  {
    icon: <FiShield />,
    title: "Cloud Deployment",
    desc: "Secure & scalable production hosting.",
  },

];

function Roadmap() {

  return (

    <section className="roadmap-card">

      <div className="roadmap-header">

        <div>

          <h2>Product Roadmap</h2>

          <p>

            Future enhancements planned for BitVision.

          </p>

        </div>

        <span>

          Coming Soon

        </span>

      </div>

      <div className="roadmap-grid">

        {

          roadmap.map((item)=>(

            <div
              className="roadmap-item"
              key={item.title}
            >

              <div className="roadmap-icon">

                {item.icon}

              </div>

              <h4>

                {item.title}

              </h4>

              <p>

                {item.desc}

              </p>

            </div>

          ))

        }

      </div>

    </section>

  );

}

export default Roadmap;