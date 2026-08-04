import "./DashboardCard.css";

function DashboardCard() {
  return (
    <div className="dashboard-card">

      {/* Header */}
      <div className="dashboard-top">

        <div className="coin">

          <div className="coin-icon">
            ₿
          </div>

          <div>

            <span className="coin-title">
              Bitcoin Forecast
            </span>

            <h2>₹98,56,545</h2>

          </div>

        </div>

        <div className="profit">
          ▲ +2.56%
        </div>

      </div>

      {/* Chart */}
      <div className="dashboard-chart">

        <svg
          width="100%"
          height="180"
          viewBox="0 0 420 180"
          preserveAspectRatio="none"
        >

          {/* Grid */}

          <defs>

            <pattern
              id="grid"
              width="40"
              height="30"
              patternUnits="userSpaceOnUse"
            >

              <path
                d="M40 0H0V30"
                fill="none"
                stroke="#E9EFEB"
                strokeWidth="1"
              />

            </pattern>

          </defs>

          <rect
            width="100%"
            height="100%"
            fill="url(#grid)"
          />

          {/* Line */}

          <polyline
            fill="none"
            stroke="#5FA777"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
            points="
              20,145
              60,140
              100,112
              140,120
              180,82
              220,90
              260,65
              300,72
              340,35
              380,48
              410,18
            "
          />

        </svg>

      </div>

      {/* Bottom */}

      <div className="dashboard-middle">

        <div className="stat-block">

          <span>Confidence</span>

          <h3>94%</h3>

          <div className="progress">

            <div className="fill"></div>

          </div>

        </div>

        <div className="stat-block">

          <span>Trend</span>

          <h3 className="green">
            Bullish
          </h3>

        </div>

      </div>

      {/* Models */}

      <div className="models">

        <span className="section-title">
          AI Models
        </span>

        <div className="model-tags">

          <span>Random Forest</span>

          <span>XGBoost</span>

          <span>LSTM</span>

        </div>

      </div>

      {/* Footer */}

      <div className="updated">

        <span className="dot"></span>

        Updated 3 sec ago

      </div>

    </div>
  );
}

export default DashboardCard;