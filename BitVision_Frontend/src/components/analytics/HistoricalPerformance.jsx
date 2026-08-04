import "./HistoricalPerformance.css";

function HistoricalPerformance() {

  return (

    <section className="historical-performance">

      {/* ================= HEADER ================= */}

      <div className="history-header">

        <div>

          <h2>Historical Performance</h2>

          <p>Bitcoin performance across multiple timeframes</p>

        </div>

        <div className="history-filter">

          <button className="active">24H</button>

          <button>7D</button>

          <button>30D</button>

          <button>90D</button>

          <button>1Y</button>

        </div>

      </div>

      {/* ================= CHART ================= */}

      <div className="history-chart">

        <svg
          viewBox="0 0 900 260"
          className="chart-svg"
        >

          <defs>

            <linearGradient
              id="chartFill"
              x1="0%"
              y1="0%"
              x2="0%"
              y2="100%"
            >

              <stop
                offset="0%"
                stopColor="#5FA777"
                stopOpacity=".35"
              />

              <stop
                offset="100%"
                stopColor="#5FA777"
                stopOpacity="0"
              />

            </linearGradient>

          </defs>

          {/* Area */}

          <path

            d="
            M0 205
            C70 185 150 175 220 182
            C310 190 390 120 470 126
            C560 132 650 88 730 96
            C810 103 860 55 900 25
            L900 260
            L0 260
            Z"

            fill="url(#chartFill)"

          />

          {/* Line */}

          <path

            d="
            M0 205
            C70 185 150 175 220 182
            C310 190 390 120 470 126
            C560 132 650 88 730 96
            C810 103 860 55 900 25"

            fill="none"

            stroke="#5FA777"

            strokeWidth="4"

            strokeLinecap="round"

          />

        </svg>

      </div>

      {/* ================= PERFORMANCE ================= */}

      <div className="performance-table">

        <div className="performance-row">

          <span>24H Return</span>

          <strong className="positive">

            +2.56%

          </strong>

        </div>

        <div className="performance-row">

          <span>30D Return</span>

          <strong className="positive">

            +12.84%

          </strong>

        </div>

        <div className="performance-row">

          <span>1Y Return</span>

          <strong className="positive">

            +64.20%

          </strong>

        </div>

        <div className="performance-row">

          <span>All-Time High</span>

          <strong>

            ₹99.2L

          </strong>

        </div>

      </div>

    </section>

  );

}

export default HistoricalPerformance;