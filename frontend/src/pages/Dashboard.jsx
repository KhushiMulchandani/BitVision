import React, { useEffect, useState } from 'react';
import API, { getSentiment } from '../services/api';

function Dashboard() {
  const [latestPrice, setLatestPrice] = useState(null);
  const [indicators, setIndicators] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    try {
      const [priceRes, featureRes, predictRes, sentimentRes] = await Promise.allSettled([
        API.get('price/'),
        API.get('features/'),
        API.get('predict/'),
        API.get('sentiment/') // <--- Direct Axios request
      ]);

      // 1. Process Price Data
      if (priceRes.status === 'fulfilled') {
        const data = priceRes.value.data.results ? priceRes.value.data.results : priceRes.value.data;
        if (Array.isArray(data) && data.length > 0) {
          const sortedData = [...data].sort((a, b) => new Date(b.date) - new Date(a.date));
          setLatestPrice(sortedData[0]);
        } else if (data && typeof data === 'object') {
          setLatestPrice(data);
        }
      } else {
        console.error("Price fetch failed:", priceRes.reason);
      }

      // 2. Process Feature Indicators Data
      if (featureRes.status === 'fulfilled') {
        const data = featureRes.value.data.results ? featureRes.value.data.results : featureRes.value.data;
        if (Array.isArray(data) && data.length > 0) {
          const sortedFeatures = [...data].sort((a, b) => new Date(b.date) - new Date(a.date));
          setIndicators(sortedFeatures);
        } else {
          setIndicators([]);
        }
      } else {
        console.error("Features fetch failed:", featureRes.reason);
      }

      // 3. Process Prediction Data
      if (predictRes.status === 'fulfilled') {
        setPrediction(predictRes.value.data);
      } else {
        console.error("Predict fetch failed:", predictRes.reason);
      }

      // 4. Process Sentiment Data
      if (sentimentRes.status === 'fulfilled') {
        setSentiment(sentimentRes.value.data); // <--- Access .data from response
      } else {
        console.error("Sentiment fetch failed:", sentimentRes.reason);
      }
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Error fetching dashboard feed.');
    } finally {
      setLoading(false);
    }
  };

  // Helper function to color code Fear & Greed status
  const getSentimentColor = (classification) => {
    if (!classification) return '#333';
    const lower = classification.toLowerCase();
    if (lower.includes('extreme fear')) return '#dc3545';
    if (lower.includes('fear')) return '#fd7e14';
    if (lower.includes('neutral')) return '#ffc107';
    if (lower.includes('greed')) return '#28a745';
    return '#20c997';
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
                <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '10px 0', color: '#111827' }}>
                  ${Number(latestPrice.close ?? 0).toLocaleString()}
                </p>
                <small style={{ color: '#666' }}>Date: {latestPrice.date ? latestPrice.date : 'Live'}</small>
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
                <p style={{ color: '#333' }}>Model: <strong>{prediction.model_used || 'Ensemble'}</strong></p>
              </div>
            ) : (
              <p>No active prediction generated yet.</p>
            )}
          </div>

          {/* Card 3: Fear & Greed Index Widget */}
          <div style={{ border: '1px solid #e0e0e0', padding: '20px', borderRadius: '8px', backgroundColor: '#fafafa' }}>
            <h3>Market Sentiment</h3>
            {sentiment ? (
              <div>
                <p style={{ fontSize: '28px', fontWeight: 'bold', color: getSentimentColor(sentiment.value_classification), margin: '10px 0' }}>
                  {sentiment.value} <span style={{ fontSize: '18px', fontWeight: 'normal' }}>/ 100</span>
                </p>
                <p style={{ fontWeight: 'bold', color: getSentimentColor(sentiment.value_classification) }}>
                  {sentiment.value_classification}
                </p>
              </div>
            ) : (
              <p>No sentiment data available.</p>
            )}
          </div>

          {/* Card 4: Technical Indicators */}
          <div style={{ border: '1px solid #e0e0e0', padding: '20px', borderRadius: '8px', backgroundColor: '#fafafa', gridColumn: '1 / -1' }}>
            <h3>Technical Indicators</h3>
            {indicators && indicators.length > 0 ? (
              <ul>
                {indicators.slice(0, 5).map((ind, i) => (
                  <li key={i} style={{ marginBottom: '8px', color: '#333' }}>
                    <strong>Date:</strong> {ind.date || 'N/A'} | <strong>RSI:</strong> {ind.rsi_14 ? Number(ind.rsi_14).toFixed(2) : (ind.rsi ? Number(ind.rsi).toFixed(2) : 'N/A')} | <strong>MACD:</strong> {ind.macd ? Number(ind.macd).toFixed(2) : 'N/A'} | <strong>SMA 20:</strong> {ind.sma_20 ? Number(ind.sma_20).toFixed(2) : (ind.ma_20 ? Number(ind.ma_20).toFixed(2) : 'N/A')}
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