import React, { useEffect, useState } from 'react';
import API from '../services/api';

function ModelComparison() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchModelMetrics();
  }, []);

  const fetchModelMetrics = async () => {
    setLoading(true);
    setError('');
    try {
      // Endpoint: GET /api/compare/
      const response = await API.get('compare/');
      const data = response.data.results ? response.data.results : response.data;
      setMetrics(data);
    } catch (err) {
      console.error('Failed to fetch model metrics:', err);
      setError('Failed to load comparison metrics. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '30px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>Model Performance Comparison</h1>
      <p>Evaluation metrics calculated across trained ML models</p>

      {loading && <p>Loading model metrics...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && metrics.length === 0 && (
        <p>No model comparison data available yet.</p>
      )}

      {!loading && !error && metrics.length > 0 && (
        <div style={{ overflowX: 'auto', marginTop: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ccc', backgroundColor: '#f4f4f4' }}>
                <th style={{ padding: '10px' }}>Model Name</th>
                <th style={{ padding: '10px' }}>MAE ($)</th>
                <th style={{ padding: '10px' }}>RMSE ($)</th>
                <th style={{ padding: '10px' }}>MAPE (%)</th>
                <th style={{ padding: '10px' }}>Directional Acc (%)</th>
                <th style={{ padding: '10px' }}>Evaluated At</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((item, index) => (
                <tr key={item.id || index} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '10px', fontWeight: 'bold' }}>{item.model_name || 'N/A'}</td>
                  <td style={{ padding: '10px' }}>{item.mae !== undefined ? Number(item.mae).toFixed(2) : 'N/A'}</td>
                  <td style={{ padding: '10px' }}>{item.rmse !== undefined ? Number(item.rmse).toFixed(2) : 'N/A'}</td>
                  <td style={{ padding: '10px' }}>{item.mape !== undefined ? `${Number(item.mape).toFixed(2)}%` : 'N/A'}</td>
                  <td style={{ padding: '10px', color: '#16a34a', fontWeight: 'bold' }}>
                    {item.directional_accuracy !== undefined ? `${Number(item.directional_accuracy).toFixed(2)}%` : 'N/A'}
                  </td>
                  <td style={{ padding: '10px' }}>
                    {item.evaluated_at ? new Date(item.evaluated_at).toLocaleString() : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ModelComparison;