import React from 'react';
import type { FinancialSummary as FinancialSummaryType } from '../types';

interface FinancialSummaryProps {
  summary: FinancialSummaryType;
}

const FinancialSummary: React.FC<FinancialSummaryProps> = ({ summary }) => {
  const formatNumber = (num: number | undefined) => {
    if (num === undefined || num === null) return 'N/A';
    return num.toLocaleString('en-US', { maximumFractionDigits: 2 });
  };

  const formatPercent = (num: number | undefined) => {
    if (num === undefined || num === null) return 'N/A';
    return `${(num * 100).toFixed(2)}%`;
  };

  const formatMarketCap = (num: number | undefined) => {
    if (num === undefined || num === null) return 'N/A';
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    return `$${num.toFixed(0)}`;
  };

  const metrics = [
    { label: 'Market Cap', value: formatMarketCap(summary.marketCap) },
    { label: 'P/E Ratio (TTM)', value: formatNumber(summary.trailingPE) },
    { label: 'Forward P/E', value: formatNumber(summary.forwardPE) },
    { label: 'Price/Book', value: formatNumber(summary.priceToBook) },
    { label: 'Debt/Equity', value: formatNumber(summary.debtToEquity) },
    { label: 'ROE', value: formatPercent(summary.returnOnEquity) },
    { label: 'Revenue Growth', value: formatPercent(summary.revenueGrowth) }
  ];

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1.5rem' }}>Financial Summary</h3>
      <div className="grid grid-cols-2" style={{ gap: '1rem' }}>
        {metrics.map((metric, index) => (
          <div
            key={index}
            style={{
              padding: '1rem',
              background: 'var(--surface-light)',
              borderRadius: '8px'
            }}
          >
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
              {metric.label}
            </p>
            <p style={{ fontSize: '1.25rem', fontWeight: 600 }}>
              {metric.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FinancialSummary;
