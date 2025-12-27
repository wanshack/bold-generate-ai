import React from 'react';
import { TrendingUp, TrendingDown, Minus, AlertCircle } from 'lucide-react';
import type { Recommendation } from '../types';

interface RecommendationCardProps {
  recommendation: Recommendation;
  currency: string;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation, currency }) => {
  const getActionIcon = () => {
    switch (recommendation.action) {
      case 'buy':
        return <TrendingUp size={32} />;
      case 'sell':
        return <TrendingDown size={32} />;
      default:
        return <Minus size={32} />;
    }
  };

  const getActionColor = () => {
    switch (recommendation.action) {
      case 'buy':
        return 'var(--success)';
      case 'sell':
        return 'var(--danger)';
      default:
        return 'var(--warning)';
    }
  };

  const getRiskBadgeClass = () => {
    switch (recommendation.risk_level) {
      case 'low':
        return 'badge-success';
      case 'high':
        return 'badge-danger';
      default:
        return 'badge-warning';
    }
  };

  return (
    <div className="card" style={{ borderLeft: `4px solid ${getActionColor()}` }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ color: getActionColor() }}>
            {getActionIcon()}
          </div>
          <div>
            <h3 style={{ textTransform: 'uppercase', color: getActionColor(), marginBottom: '0.25rem' }}>
              {recommendation.action}
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Confidence: {(recommendation.confidence_score * 100).toFixed(1)}%
            </p>
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span className={`badge ${getRiskBadgeClass()}`}>
            {recommendation.risk_level?.toUpperCase()} RISK
          </span>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '0.5rem' }}>
            {recommendation.time_horizon} term
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ marginBottom: '1.5rem' }}>
        <div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>Current Price</p>
          <p style={{ fontSize: '1.25rem', fontWeight: 600 }}>
            {currency} {recommendation.current_price.toFixed(2)}
          </p>
        </div>
        <div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>Target Price</p>
          <p style={{ fontSize: '1.25rem', fontWeight: 600 }}>
            {currency} {recommendation.target_price?.toFixed(2) || 'N/A'}
          </p>
        </div>
        <div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>Potential</p>
          <p style={{ fontSize: '1.25rem', fontWeight: 600, color: getActionColor() }}>
            {recommendation.target_price
              ? `${(((recommendation.target_price - recommendation.current_price) / recommendation.current_price) * 100).toFixed(2)}%`
              : 'N/A'}
          </p>
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <h4 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>Analysis Scores</h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Technical</span>
              <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>
                {((recommendation.technical_score || 0) * 100).toFixed(0)}%
              </span>
            </div>
            <div style={{ width: '100%', height: '6px', background: 'var(--surface-light)', borderRadius: '3px', overflow: 'hidden' }}>
              <div
                style={{
                  width: `${(recommendation.technical_score || 0) * 100}%`,
                  height: '100%',
                  background: 'var(--primary)',
                  transition: 'width 0.3s ease'
                }}
              />
            </div>
          </div>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Fundamental</span>
              <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>
                {((recommendation.fundamental_score || 0) * 100).toFixed(0)}%
              </span>
            </div>
            <div style={{ width: '100%', height: '6px', background: 'var(--surface-light)', borderRadius: '3px', overflow: 'hidden' }}>
              <div
                style={{
                  width: `${(recommendation.fundamental_score || 0) * 100}%`,
                  height: '100%',
                  background: 'var(--secondary)',
                  transition: 'width 0.3s ease'
                }}
              />
            </div>
          </div>
        </div>
      </div>

      <div style={{ padding: '1rem', background: 'var(--surface-light)', borderRadius: '8px' }}>
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem' }}>
          <AlertCircle size={20} style={{ color: 'var(--primary)', flexShrink: 0 }} />
          <h4 style={{ fontSize: '0.875rem', fontWeight: 600 }}>AI Analysis</h4>
        </div>
        <div
          style={{
            fontSize: '0.875rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.6,
            whiteSpace: 'pre-line'
          }}
        >
          {recommendation.reasoning}
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;
