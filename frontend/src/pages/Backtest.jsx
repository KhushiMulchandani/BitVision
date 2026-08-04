import React, { useEffect, useState } from 'react';
import API from '../services/api';

function Backtest() {
  const [backtestData, setBacktestData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [days, setDays] = useState(30);

  useEffect(() => {
    fetchBacktestData(days);
  }, [days]);

  const fetchBacktestData = async (selectedDays) => {
    setLoading(true);
    setError('');
    try {
      // Endpoint: GET /api/backtest/?days=30
      const response = await API.get(`backtest/?days=${selectedDays}`);
      const data = response.data.results ? response.data.results : response.data;
      setBacktestData(data);
    } catch (err) {
      console.error('Failed to fetch backtest data:', err);
      setError('Failed to load backtest data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '30px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Model Backtesting</h1>
      <p>Historical Predictions vs. Actual Closing Prices</p>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Time Range:</label>
        <select 
          value={days} 
          onChange={(e) => setDays(Number(e.target.value))}
          style={{ padding: '6px 12px', borderRadius: '4px' }}
        >
          <option value={7}>Last 7 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={90}>Last 90 Days</option>
        </select>
      </div>

      {loading && <p>Loading backtest data...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && backtestData.length === 0 && (
        <p>No backtest records found for the selected period.</p>
      )}

      {!loading && !error && backtestData.length > 0 && (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ccc', backgroundColor: '#f4f4f4' }}>
                <th style={{ padding: '10px' }}>Date</th>
                <th style={{ padding: '10px' }}>Model</th>
                <th style={{ padding: '10px' }}>Predicted Price</th>
                <th style={{ padding: '10px' }}>Actual Price</th>
                <th style={{ padding: '10px' }}>Variance ($)</th>
              </tr>
            </thead>
            <tbody>
              {backtestData.map((row, index) => {
                const pred = Number(row.predicted_price || 0);
                const actual = row.actual_price ? Number(row.actual_price) : null;
                const diff = actual !== null ? (pred - actual).toFixed(2) : null;

                return (
                  <tr key={row.id || index} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '10px' }}>{row.date}</td>
                    <td style={{ padding: '10px', textTransform: 'uppercase', fontWeight: 'bold' }}>
                      {row.model_used || 'N/A'}
                    </td>
                    <td style={{ padding: '10px' }}>${pred.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                    <td style={{ padding: '10px' }}>
                      {actual !== null ? `$${actual.toLocaleString(undefined, { minimumFractionDigits: 2 })}` : 'N/A'}
                    </td>
                    <td 
                      style={{ 
                        padding: '10px', 
                        fontWeight: 'bold',
                        color: diff === null ? '#666' : diff >= 0 ? '#16a34a' : '#dc2626' 
                      }}
                    >
                      {diff !== null ? (diff >= 0 ? `+${diff}` : diff) : 'N/A'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Backtest;