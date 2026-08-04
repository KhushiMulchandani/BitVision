import React, { useEffect, useState } from 'react';
import API from '../services/api';

function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);
  const [amount, setAmount] = useState('');
  const [action, setAction] = useState('buy');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    setLoading(true);
    try {
      // GET /api/portfolio/
      const response = await API.get('portfolio/');
      setPortfolio(response.data);
    } catch (err) {
      console.error('Error loading portfolio:', err);
      setMessage({
        text: err.response?.status === 401 
          ? 'Please log in to access paper trading.' 
          : 'Failed to load portfolio details.',
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTrade = async (e) => {
    e.preventDefault();
    if (!amount || Number(amount) <= 0) {
      setMessage({ text: 'Please enter a valid positive amount.', type: 'error' });
      return;
    }

    setSubmitting(true);
    setMessage({ text: '', type: '' });

    try {
      // POST /api/portfolio/ { action: 'buy'|'sell', amount_inr: <number> }
      const response = await API.post('portfolio/', {
        action: action,
        amount_inr: Number(amount),
      });
      setPortfolio(response.data);
      setAmount('');
      setMessage({
        text: `Successfully executed ${action.toUpperCase()} order!`,
        type: 'success'
      });
    } catch (err) {
      const errDetail = err.response?.data?.error || 'Trade execution failed.';
      setMessage({ text: errDetail, type: 'error' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ padding: '30px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Paper Trading Portfolio</h1>
      <p>Simulate Bitcoin buy and sell orders in real-time.</p>

      {loading && <p>Loading portfolio data...</p>}

      {!loading && portfolio && (
        <div>
          {/* Balance Cards */}
          <div style={{ display: 'flex', gap: '20px', margin: '20px 0' }}>
            <div style={{ flex: 1, padding: '20px', border: '1px solid #e0e0e0', borderRadius: '8px', backgroundColor: '#fafafa' }}>
              <h3>Cash Balance</h3>
              <p style={{ fontSize: '26px', fontWeight: 'bold', color: '#1a73e8', margin: '10px 0' }}>
                ₹{Number(portfolio.cash_balance ?? 0).toLocaleString()}
              </p>
            </div>
            <div style={{ flex: 1, padding: '20px', border: '1px solid #e0e0e0', borderRadius: '8px', backgroundColor: '#fafafa' }}>
              <h3>BTC Holdings</h3>
              <p style={{ fontSize: '26px', fontWeight: 'bold', color: '#f2a900', margin: '10px 0' }}>
                {Number(portfolio.btc_holdings ?? 0).toFixed(6)} BTC
              </p>
            </div>
          </div>

          {/* Trade Form */}
          <div style={{ border: '1px solid #e0e0e0', padding: '25px', borderRadius: '8px', marginTop: '20px' }}>
            <h3>Place Order</h3>

            {message.text && (
              <div style={{ 
                padding: '10px 15px', 
                borderRadius: '4px', 
                marginBottom: '15px', 
                backgroundColor: message.type === 'error' ? '#f8d7da' : '#d4edda',
                color: message.type === 'error' ? '#721c24' : '#155724'
              }}>
                {message.text}
              </div>
            )}

            <form onSubmit={handleTrade} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Action</label>
                <select 
                  value={action} 
                  onChange={(e) => setAction(e.target.value)}
                  style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
                >
                  <option value="buy">BUY BTC</option>
                  <option value="sell">SELL BTC</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Amount (INR)</label>
                <input
                  type="number"
                  placeholder="e.g. 5000"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                style={{
                  padding: '12px',
                  backgroundColor: action === 'buy' ? '#28a745' : '#dc3545',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  fontWeight: 'bold',
                  fontSize: '16px',
                  cursor: submitting ? 'not-allowed' : 'pointer',
                  opacity: submitting ? 0.7 : 1
                }}
              >
                {submitting ? 'Executing Trade...' : `EXECUTE ${action.toUpperCase()} ORDER`}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Portfolio;