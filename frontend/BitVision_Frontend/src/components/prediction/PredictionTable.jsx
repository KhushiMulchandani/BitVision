import "./PredictionTable.css";

import {
  FaArrowTrendUp,
  FaArrowTrendDown,
} from "react-icons/fa6";

function PredictionTable() {
  return (
    <section className="prediction-table-section">

      <div className="table-header">

        <div>

          <span className="table-badge">
            Prediction History
          </span>

          <h2>Recent Forecasts</h2>

          <p>
            Compare previous AI predictions with actual market
            performance.
          </p>

        </div>

      </div>

      <div className="table-card">

        <table>

          <thead>

            <tr>

              <th>Date</th>

              <th>Predicted</th>

              <th>Actual</th>

              <th>Difference</th>

              <th>Status</th>

              <th>Confidence</th>

            </tr>

          </thead>

          <tbody>

            <tr>

              <td>04 Aug</td>

              <td>₹98,56,450</td>

              <td>₹98,22,900</td>

              <td className="positive">

                <FaArrowTrendUp />

                +2.56%

              </td>

              <td>

                <span className="status success">

                  Bullish

                </span>

              </td>

              <td>94%</td>

            </tr>

            <tr>

              <td>03 Aug</td>

              <td>₹97,84,120</td>

              <td>₹97,10,520</td>

              <td className="negative">

                <FaArrowTrendDown />

                -1.28%

              </td>

              <td>

                <span className="status danger">

                  Bearish

                </span>

              </td>

              <td>92%</td>

            </tr>

            <tr>

              <td>02 Aug</td>

              <td>₹98,02,640</td>

              <td>₹97,88,700</td>

              <td className="positive">

                <FaArrowTrendUp />

                +0.84%

              </td>

              <td>

                <span className="status success">

                  Bullish

                </span>

              </td>

              <td>91%</td>

            </tr>

            <tr>

              <td>01 Aug</td>

              <td>₹96,95,300</td>

              <td>₹97,42,810</td>

              <td className="negative">

                <FaArrowTrendDown />

                -0.62%

              </td>

              <td>

                <span className="status danger">

                  Bearish

                </span>

              </td>

              <td>90%</td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>
  );
}

export default PredictionTable;