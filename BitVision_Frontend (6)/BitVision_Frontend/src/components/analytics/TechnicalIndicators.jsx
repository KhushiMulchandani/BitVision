import "./TechnicalIndicators.css";

function TechnicalIndicators() {

  const indicators = [

    {
      name: "RSI (14)",
      value: "64.2",
      signal: "Bullish",
      type: "positive",
    },

    {
      name: "MACD",
      value: "Positive",
      signal: "Buy",
      type: "positive",
    },

    {
      name: "EMA 20",
      value: "₹97.8L",
      signal: "Above Price",
      type: "positive",
    },

    {
      name: "EMA 50",
      value: "₹96.2L",
      signal: "Strong",
      type: "positive",
    },

    {
      name: "ATR",
      value: "Medium",
      signal: "Stable",
      type: "warning",
    },

    {
      name: "Bollinger",
      value: "Upper Band",
      signal: "Breakout",
      type: "positive",
    },

    {
      name: "Fear Index",
      value: "74",
      signal: "Greed",
      type: "warning",
    }

  ];

  return (

    <section className="technical-indicators">

      <div className="technical-header">

        <div>

          <h2>Technical Indicators</h2>

          <p>
            Live technical health of Bitcoin.
          </p>

        </div>

        <span>
          Updated Now
        </span>

      </div>

      <div className="indicator-table">

        <div className="table-head">

          <span>Indicator</span>

          <span>Value</span>

          <span>Signal</span>

        </div>

        {indicators.map((item) => (

          <div
            className="table-row"
            key={item.name}
          >

            <span>
              {item.name}
            </span>

            <strong>
              {item.value}
            </strong>

            <small className={item.type}>
              {item.signal}
            </small>

          </div>

        ))}

      </div>

    </section>

  );

}

export default TechnicalIndicators;