import { useState } from 'react';
import { Activity } from 'lucide-react';
import StockSearch from './components/StockSearch';
import StockHeader from './components/StockHeader';
import PriceChart from './components/PriceChart';
import RecommendationCard from './components/RecommendationCard';
import TechnicalIndicators from './components/TechnicalIndicators';
import FinancialSummary from './components/FinancialSummary';
import { analyzeStock } from './lib/api';
import type { StockAnalysis } from './types';

function App() {
  const [analysis, setAnalysis] = useState<StockAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (ticker: string, days: number, model: 'lstm' | 'xgboost') => {
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const result = await analyzeStock({
        ticker,
        prediction_days: days,
        model_type: model
      });
      setAnalysis(result as StockAnalysis);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to analyze stock. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--background)' }}>
      <header style={{
        background: 'linear-gradient(135deg, var(--surface) 0%, var(--primary) 100%)',
        padding: '2rem',
        borderBottom: '1px solid var(--border)'
      }}>
        <div className="container">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <Activity size={40} style={{ color: 'white' }} />
            <div>
              <h1 style={{ marginBottom: '0.25rem', color: 'white' }}>Stock Prediction Platform</h1>
              <p style={{ color: 'rgba(255, 255, 255, 0.9)', fontSize: '1rem' }}>
                AI-Powered Investment Analysis & Recommendations
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container" style={{ paddingTop: '2rem', paddingBottom: '3rem' }}>
        <div style={{ marginBottom: '2rem' }}>
          <StockSearch onSearch={handleSearch} loading={loading} />
        </div>

        {loading && (
          <div className="loading">
            <div>
              <div className="spinner" style={{ margin: '0 auto' }} />
              <p style={{ marginTop: '1rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
                Analyzing stock data and generating predictions...
              </p>
            </div>
          </div>
        )}

        {error && (
          <div className="card" style={{ borderLeft: '4px solid var(--danger)', marginBottom: '2rem' }}>
            <h3 style={{ color: 'var(--danger)', marginBottom: '0.5rem' }}>Error</h3>
            <p style={{ color: 'var(--text-secondary)' }}>{error}</p>
          </div>
        )}

        {analysis && !loading && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <StockHeader
              stock={analysis.stock}
              latestPrice={analysis.latest_price}
              priceChange={analysis.price_change}
              priceChangePercent={analysis.price_change_percent}
              currency={analysis.stock.currency}
            />

            <RecommendationCard
              recommendation={analysis.recommendation}
              currency={analysis.stock.currency}
            />

            <PriceChart
              historicalPrices={analysis.historical_prices}
              predictions={analysis.predictions}
              currency={analysis.stock.currency}
            />

            <div className="grid grid-cols-2" style={{ gap: '2rem' }}>
              <TechnicalIndicators
                indicators={analysis.technical_indicators}
                latestPrice={analysis.latest_price}
              />
              <FinancialSummary summary={analysis.financial_summary} />
            </div>
          </div>
        )}

        {!analysis && !loading && !error && (
          <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
            <Activity size={64} style={{ color: 'var(--text-muted)', margin: '0 auto 1.5rem' }} />
            <h2 style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>
              Get Started
            </h2>
            <p style={{ color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>
              Enter a stock ticker above to get AI-powered price predictions, technical analysis,
              and investment recommendations powered by machine learning models.
            </p>
          </div>
        )}
      </main>

      <footer style={{
        borderTop: '1px solid var(--border)',
        padding: '2rem',
        textAlign: 'center',
        color: 'var(--text-muted)',
        fontSize: '0.875rem'
      }}>
        <p style={{ marginBottom: '0.5rem' }}>
          <strong>Disclaimer:</strong> This platform provides AI-generated stock predictions and recommendations
          for educational and informational purposes only.
        </p>
        <p>
          This is not financial advice. Always conduct your own research and consult with a licensed
          financial advisor before making investment decisions. Past performance does not guarantee future results.
        </p>
      </footer>
    </div>
  );
}

export default App;
