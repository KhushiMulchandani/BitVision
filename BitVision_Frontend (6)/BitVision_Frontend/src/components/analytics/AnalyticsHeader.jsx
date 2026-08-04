import "./AnalyticsHeader.css";

import { FaChartSimple } from "react-icons/fa6";

function AnalyticsHeader() {

  return (

    <section className="analytics-header">

      <span className="analytics-badge">

        <FaChartSimple />

        Market Analytics

      </span>

      <h1>

        Advanced Bitcoin

        <span> Analytics</span>

      </h1>

      <p>

        Explore real-time Bitcoin trends, technical indicators,
        historical performance and AI-powered market intelligence.

      </p>

    </section>

  );

}

export default AnalyticsHeader;