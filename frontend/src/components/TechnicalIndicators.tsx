import React from 'react';
import type { TechnicalIndicator } from '../types';

interface TechnicalIndicatorsProps {
  indicators: TechnicalIndicator[];
  latestPrice: number;
}

const TechnicalIndicators: React.FC<TechnicalIndicatorsProps> = ({ indicators, latestPrice }) => {
  if (!indicators || indicators.length === 0) {
    return (
      <div className="card">
        <h3>Technical Indicators</h3>
        <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>No technical indicators available</p>
      </div>
    );
  }

  const latest = indicators[0];

  const getRSISignal = (rsi: number | null | undefined) => {
    if (!rsi) return { text: 'N/A', color: 'var(--text-muted)' };
    if (rsi < 30) return { text: 'Oversold', color: 'var(--success)' };
    if (rsi > 70) return { text: 'Overbought', color: 'var(--danger)' };
    return { text: 'Neutral', color: 'var(--warning)' };
  };

  const getMACDSignal = (macd: number | null | undefined, signal: number | null | undefined) => {
    if (!macd || !signal) return { text: 'N/A', color: 'var(--text-muted)' };
    if (macd > signal) return { text: 'Bullish', color: 'var(--success)' };
    return { text: 'Bearish', color: 'var(--danger)' };
  };

  const getMASignal = (ma: number | null | undefined, price: number) => {
    if (!ma) return { text: 'N/A', color: 'var(--text-muted)' };
    if (price > ma) return { text: 'Above', color: 'var(--success)' };
    return { text: 'Below', color: 'var(--danger)' };
  };

  const rsiSignal = getRSISignal(latest.rsi_14);
  const macdSignal = getMACDSignal(latest.macd, latest.macd_signal);
  const sma20Signal = getMASignal(latest.sma_20, latestPrice);
  const sma50Signal = getMASignal(latest.sma_50, latestPrice);
  const sma200Signal = getMASignal(latest.sma_200, latestPrice);

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1.5rem' }}>Technical Indicators</h3>

      <div style={{ display: 'grid', gap: '1rem' }}>
        <div style={{ padding: '1rem', background: 'var(--surface-light)', borderRadius: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontWeight: 600 }}>RSI (14)</span>
            <span style={{ color: rsiSignal.color, fontWeight: 600 }}>{rsiSignal.text}</span>
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            {latest.rsi_14 ? latest.rsi_14.toFixed(2) : 'N/A'}
          </div>
          <div style={{ width: '100%', height: '6px', background: 'var(--background)', borderRadius: '3px', marginTop: '0.5rem', overflow: 'hidden' }}>
            {latest.rsi_14 && (
              <div
                style={{
                  width: `${latest.rsi_14}%`,
                  height: '100%',
                  background: latest.rsi_14 < 30 ? 'var(--success)' : latest.rsi_14 > 70 ? 'var(--danger)' : 'var(--warning)',
                  transition: 'width 0.3s ease'
                }}
              />
            )}
          </div>
        </div>

        <div style={{ padding: '1rem', background: 'var(--surface-light)', borderRadius: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontWeight: 600 }}>MACD</span>
            <span style={{ color: macdSignal.color, fontWeight: 600 }}>{macdSignal.text}</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem', fontSize: '0.875rem' }}>
            <div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>MACD</div>
              <div style={{ fontWeight: 600 }}>{latest.macd ? latest.macd.toFixed(2) : 'N/A'}</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Signal</div>
              <div style={{ fontWeight: 600 }}>{latest.macd_signal ? latest.macd_signal.toFixed(2) : 'N/A'}</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>Histogram</div>
              <div style={{ fontWeight: 600 }}>{latest.macd_histogram ? latest.macd_histogram.toFixed(2) : 'N/A'}</div>
            </div>
          </div>
        </div>

        <div style={{ padding: '1rem', background: 'var(--surface-light)', borderRadius: '8px' }}>
          <div style={{ fontWeight: 600, marginBottom: '0.75rem' }}>Moving Averages</div>
          <div style={{ display: 'grid', gap: '0.5rem', fontSize: '0.875rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>SMA 20:</span>
              <span>
                <strong>{latest.sma_20 ? latest.sma_20.toFixed(2) : 'N/A'}</strong>
                <span style={{ marginLeft: '0.5rem', color: sma20Signal.color, fontWeight: 600 }}>
                  ({sma20Signal.text})
                </span>
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>SMA 50:</span>
              <span>
                <strong>{latest.sma_50 ? latest.sma_50.toFixed(2) : 'N/A'}</strong>
                <span style={{ marginLeft: '0.5rem', color: sma50Signal.color, fontWeight: 600 }}>
                  ({sma50Signal.text})
                </span>
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>SMA 200:</span>
              <span>
                <strong>{latest.sma_200 ? latest.sma_200.toFixed(2) : 'N/A'}</strong>
                <span style={{ marginLeft: '0.5rem', color: sma200Signal.color, fontWeight: 600 }}>
                  ({sma200Signal.text})
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechnicalIndicators;
