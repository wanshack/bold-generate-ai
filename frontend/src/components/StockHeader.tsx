import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import type { Stock } from '../types';

interface StockHeaderProps {
  stock: Stock;
  latestPrice: number;
  priceChange: number;
  priceChangePercent: number;
  currency: string;
}

const StockHeader: React.FC<StockHeaderProps> = ({
  stock,
  latestPrice,
  priceChange,
  priceChangePercent,
  currency
}) => {
  const isPositive = priceChange >= 0;

  return (
    <div className="card" style={{ background: 'linear-gradient(135deg, var(--surface) 0%, var(--surface-light) 100%)' }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <h1 style={{ fontSize: '2rem', marginBottom: 0 }}>{stock.ticker}</h1>
            <span className="badge badge-info">{stock.exchange}</span>
          </div>
          <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>
            {stock.name}
          </p>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
            {stock.sector} • {stock.country}
          </p>
        </div>

        <div style={{ textAlign: 'right' }}>
          <p style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.25rem' }}>
            {currency} {latestPrice.toFixed(2)}
          </p>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              justifyContent: 'flex-end',
              color: isPositive ? 'var(--success)' : 'var(--danger)'
            }}
          >
            {isPositive ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
            <span style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              {isPositive ? '+' : ''}{priceChange.toFixed(2)} ({isPositive ? '+' : ''}{priceChangePercent.toFixed(2)}%)
            </span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            vs. previous close
          </p>
        </div>
      </div>
    </div>
  );
};

export default StockHeader;
