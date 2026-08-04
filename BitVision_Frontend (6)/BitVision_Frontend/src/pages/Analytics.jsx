import Navbar from "../components/landing/Navbar";

import AnalyticsHeader from "../components/analytics/AnalyticsHeader";
import MarketWorkspace from "../components/analytics/MarketWorkspace";

import MarketIntelligence from "../components/analytics/MarketIntelligence";
import TechnicalIndicators from "../components/analytics/TechnicalIndicators";
import TrendAnalysis from "../components/analytics/TrendAnalysis";
import HistoricalPerformance from "../components/analytics/HistoricalPerformance";

import "../components/analytics/Analytics.css";

function Analytics() {
  return (
    <>
      <Navbar />

      <main className="analytics-page">

        <AnalyticsHeader />

        <MarketWorkspace />

        <section className="analytics-dashboard">

          {/* ROW 1 */}

          <div className="analytics-row analytics-row-top">

            <MarketIntelligence />

            <TechnicalIndicators />

          </div>

          {/* ROW 2 */}

          <div className="analytics-row">

            <TrendAnalysis />

            <HistoricalPerformance />

          </div>


        </section>

      </main>

    </>
  );
}

export default Analytics;