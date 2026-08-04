import "./MarketIntelligence.css";

import {
  FaArrowTrendUp,
  FaChartPie,
  FaCoins,
  FaWallet,
  FaGlobe,
  FaSignal,
} from "react-icons/fa6";

function MarketIntelligence() {

  return (

    <section className="market-intelligence">

      <div className="intelligence-card">

        <div className="intelligence-header">

          <h2>Market Intelligence</h2>

          <span>Live Overview</span>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaCoins />

            <span>Market Cap</span>

          </div>

          <strong>₹2.35T</strong>

          <small className="green">Growing</small>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaChartPie />

            <span>BTC Dominance</span>

          </div>

          <strong>58.2%</strong>

          <small className="green">Strong</small>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaArrowTrendUp />

            <span>24H Change</span>

          </div>

          <strong>+2.56%</strong>

          <small className="green">Bullish</small>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaWallet />

            <span>Volume</span>

          </div>

          <strong>₹1.84T</strong>

          <small>High</small>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaGlobe />

            <span>Liquidity</span>

          </div>

          <strong>High</strong>

          <small className="green">Healthy</small>

        </div>

        <div className="intel-row">

          <div className="intel-left">

            <FaSignal />

            <span>Sentiment</span>

          </div>

          <strong>Greed</strong>

          <small className="orange">Positive</small>

        </div>

      </div>

    </section>

  );

}

export default MarketIntelligence;