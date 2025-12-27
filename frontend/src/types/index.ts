export interface Stock {
  id: string;
  ticker: string;
  name: string;
  exchange: string;
  sector: string;
  country: string;
  currency: string;
}

export interface StockPrice {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TechnicalIndicator {
  date: string;
  rsi_14: number;
  macd: number;
  macd_signal: number;
  macd_histogram: number;
  sma_20: number;
  sma_50: number;
  sma_200: number;
}

export interface Prediction {
  date: string;
  price: number;
}

export interface Recommendation {
  action: 'buy' | 'hold' | 'sell';
  confidence_score: number;
  target_price: number;
  current_price: number;
  technical_score: number;
  fundamental_score: number;
  reasoning: string;
  risk_level: 'low' | 'medium' | 'high';
  time_horizon: 'short' | 'medium' | 'long';
}

export interface FinancialSummary {
  marketCap?: number;
  trailingPE?: number;
  forwardPE?: number;
  priceToBook?: number;
  debtToEquity?: number;
  returnOnEquity?: number;
  revenueGrowth?: number;
}

export interface StockAnalysis {
  stock: Stock;
  latest_price: number;
  price_change: number;
  price_change_percent: number;
  historical_prices: StockPrice[];
  technical_indicators: TechnicalIndicator[];
  predictions: Prediction[];
  recommendation: Recommendation;
  financial_summary: FinancialSummary;
}
