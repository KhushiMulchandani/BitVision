import "./LiveTicker.css";

function LiveTicker() {
  return (
    <section className="live-ticker">

      <div className="ticker-track">

        <div className="ticker-item">
          <span className="coin">BTC</span>
          <span className="price">₹98,56,545</span>
          <span className="up">▲ +4.91%</span>
        </div>

        <div className="ticker-item">
          <span className="coin">ETH</span>
          <span className="price">₹2,64,500</span>
          <span className="up">▲ +1.82%</span>
        </div>

        <div className="ticker-item">
          <span className="coin">SOL</span>
          <span className="price">₹14,890</span>
          <span className="down">▼ -0.95%</span>
        </div>

        <div className="ticker-item">
          <span className="coin">XRP</span>
          <span className="price">₹53</span>
          <span className="up">▲ +0.66%</span>
        </div>

      </div>

    </section>
  );
}

export default LiveTicker;