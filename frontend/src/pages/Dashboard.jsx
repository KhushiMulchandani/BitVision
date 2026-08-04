import React, { useEffect, useState } from 'react';
import API from '../services/api';

function Dashboard() {
  const [latestPrice, setLatestPrice] = useState(null);
  const [indicators, setIndicators] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    try {
      const [priceRes, featureRes, predictRes] = await Promise.allSettled([
        API.get('price/'),
        API.get('features/'),
        API.get('predict/')
      ]);

      // 1. Process Price Data (Sort descending by date to grab the newest)
      if (priceRes.status === 'fulfilled') {
        const data = priceRes.value.data.results ? priceRes.value.data.results : priceRes.value.data;
        if (Array.isArray(data) && data.length > 0) {
          // Sort array so newest date is first
          const sortedData = [...data].sort((a, b) => new Date(b.date) - new Date(a.date));
          setLatestPrice(sortedData[0]);
        } else if (data && typeof data === 'object') {
          setLatestPrice(data);
        }
      }

      // 2. Process Feature Indicators Data (Sort descending by date)
      if (featureRes.status === 'fulfilled') {
        const data = featureRes.value.data.results ? featureRes.value.data.results : featureRes.value.data;
        if (Array.isArray(data) && data.length > 0) {
          const sortedFeatures = [...data].sort((a, b) => new Date(b.date) - new Date(a.date));
          setIndicators(sortedFeatures);
        } else {
          setIndicators([]);
        }
      }

      // 3. Process Prediction Data
      if (predictRes.status === 'fulfilled') {
        setPrediction(predictRes.value.data);
      }
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Error fetching dashboard feed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '30px', maxWidth: '1100px', margin: '0 auto' }}>
      <h1>BitVision Overview</h1>

      {loading && <p>Loading market data & AI predictions...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginTop: '20px' }}>
          
          {/* Card 1: Latest Price */}
          <div style={{ border: '1px solid #e0e0e0', padding: '20px', borderRadius: '8px', backgroundColor: '#fafafa' }}>
            <h3>Bitcoin Live Price</h3>
            {latestPrice ? (
              <div>
                <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '10px 0' }}>
                  ${Number(latestPrice.close ?? 0).toLocaleString()}
                </p>
                <small>Date: {latestPrice.date ? latestPrice.date : 'Live'}</small>
              </div>
            ) : (
              <p>No live price data available.</p>
            )}
          </div>

          {/* Card 2: AI Prediction */}
          <div style={{ border: '1px solid #e0e0e0', padding: '20px', borderRadius: '8px', backgroundColor: '#fafafa' }}>
            <h3>Next Signal / Prediction</h3>
            {prediction ? (
              <div>
                <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#28a745', margin: '10px 0' }}>
                  ${Number(prediction.predicted_price || 0).toLocaleString()}
                </p>
                <p>Model: <strong>{prediction.model_used || 'Ensemble'}</strong></p>
              </div>
            ) : (
              <p>No active prediction generated yet.</p>
            )}
          </div>

          {/* Card 3: Technical Indicators */}
          <div style={{ border: '1px solid #e0e0e0', padding: '20px', borderRadius: '8px', backgroundColor: '#fafafa', gridColumn: '1 / -1' }}>
            <h3>Technical Indicators</h3>
            {indicators && indicators.length > 0 ? (
              <ul>
                {indicators.slice(0, 5).map((ind, i) => (
                  <li key={i} style={{ marginBottom: '8px' }}>
                    <strong>Date:</strong> {ind.date || 'N/A'} | <strong>RSI:</strong> {ind.rsi_14 ?? ind.rsi ?? 'N/A'} | <strong>MACD:</strong> {ind.macd ?? 'N/A'} | <strong>SMA 20:</strong> {ind.sma_20 ?? ind.ma_20 ?? 'N/A'}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No indicator calculated data returned.</p>
            )}
          </div>

        </div>
      )}
    </div>
  );
}

export default Dashboard;