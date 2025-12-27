import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface StockSearchProps {
  onSearch: (ticker: string, days: number, model: 'lstm' | 'xgboost') => void;
  loading: boolean;
}

const StockSearch: React.FC<StockSearchProps> = ({ onSearch, loading }) => {
  const [ticker, setTicker] = useState('');
  const [days, setDays] = useState(30);
  const [model, setModel] = useState<'lstm' | 'xgboost'>('xgboost');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase(), days, model);
    }
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: '1.5rem' }}>Stock Analysis</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Stock Ticker (e.g., AAPL, BBCA.JK)
          </label>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter stock ticker"
            style={{
              width: '100%',
              padding: '0.75rem',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              background: 'var(--surface-light)',
              color: 'var(--text-primary)',
              fontSize: '1rem'
            }}
            disabled={loading}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Prediction Period
            </label>
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border)',
                background: 'var(--surface-light)',
                color: 'var(--text-primary)',
                fontSize: '1rem'
              }}
              disabled={loading}
            >
              <option value={7}>7 days</option>
              <option value={14}>14 days</option>
              <option value={30}>30 days</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              ML Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value as 'lstm' | 'xgboost')}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border)',
                background: 'var(--surface-light)',
                color: 'var(--text-primary)',
                fontSize: '1rem'
              }}
              disabled={loading}
            >
              <option value="xgboost">XGBoost</option>
              <option value="lstm">LSTM</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !ticker.trim()}
          style={{ marginTop: '0.5rem' }}
        >
          <Search size={20} />
          {loading ? 'Analyzing...' : 'Analyze Stock'}
        </button>
      </form>
    </div>
  );
};

export default StockSearch;
