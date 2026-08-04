import "./FeatureImportance.css";

const features = [
  { name: "Price History", value: 92 },
  { name: "Trading Volume", value: 84 },
  { name: "RSI Indicator", value: 78 },
  { name: "Market Sentiment", value: 71 },
  { name: "MACD", value: 66 },
  { name: "News Trend", value: 54 },
];

function FeatureImportance() {
  return (
    <section className="feature-card">

      <div className="feature-header">

        <div>

          <h2>Feature Analysis</h2>

          <p>
            Relative contribution of each feature to the prediction model.
          </p>

        </div>

        <span className="feature-badge">
          Top Factors
        </span>

      </div>

      <div className="feature-list">

        {features.map((feature) => (

          <div
            className="feature-row"
            key={feature.name}
          >

            <div className="feature-top">

              <span>{feature.name}</span>

              <strong>{feature.value}%</strong>

            </div>

            <div className="feature-track">

              <div
                className="feature-fill"
                style={{
                  width: `${feature.value}%`,
                }}
              />

            </div>

          </div>

        ))}

      </div>

    </section>
  );
}

export default FeatureImportance;