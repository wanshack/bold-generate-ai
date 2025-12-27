/*
  # Stock Prediction Platform Schema

  ## Overview
  This migration creates the complete database schema for a stock price prediction
  and investment recommendation platform supporting US and Indonesian (IDX) stocks.

  ## New Tables
  
  ### 1. `stocks`
  Stores basic stock information
  - `id` (uuid, primary key) - Unique identifier
  - `ticker` (text, unique) - Stock ticker symbol (e.g., AAPL, BBCA.JK)
  - `name` (text) - Company name
  - `exchange` (text) - Stock exchange (NYSE, NASDAQ, IDX)
  - `sector` (text) - Business sector
  - `country` (text) - Country code (US, ID)
  - `currency` (text) - Trading currency
  - `last_updated` (timestamptz) - Last data fetch timestamp
  - `created_at` (timestamptz) - Record creation timestamp

  ### 2. `stock_prices`
  Historical and real-time price data
  - `id` (uuid, primary key)
  - `stock_id` (uuid, foreign key) - References stocks table
  - `date` (date) - Price date
  - `open` (decimal) - Opening price
  - `high` (decimal) - Highest price
  - `low` (decimal) - Lowest price
  - `close` (decimal) - Closing price
  - `volume` (bigint) - Trading volume
  - `adjusted_close` (decimal) - Adjusted closing price
  - `created_at` (timestamptz)

  ### 3. `technical_indicators`
  Technical analysis indicators
  - `id` (uuid, primary key)
  - `stock_id` (uuid, foreign key)
  - `date` (date) - Indicator date
  - `rsi_14` (decimal) - 14-day RSI
  - `macd` (decimal) - MACD line
  - `macd_signal` (decimal) - MACD signal line
  - `macd_histogram` (decimal) - MACD histogram
  - `sma_20` (decimal) - 20-day Simple Moving Average
  - `sma_50` (decimal) - 50-day Simple Moving Average
  - `sma_200` (decimal) - 200-day Simple Moving Average
  - `ema_12` (decimal) - 12-day Exponential Moving Average
  - `ema_26` (decimal) - 26-day Exponential Moving Average
  - `created_at` (timestamptz)

  ### 4. `financial_statements`
  Company financial data
  - `id` (uuid, primary key)
  - `stock_id` (uuid, foreign key)
  - `period_end` (date) - Financial period end date
  - `statement_type` (text) - Type: income_statement, balance_sheet, cash_flow
  - `data` (jsonb) - Complete financial data in JSON format
  - `created_at` (timestamptz)

  ### 5. `predictions`
  ML model predictions
  - `id` (uuid, primary key)
  - `stock_id` (uuid, foreign key)
  - `prediction_date` (date) - When prediction was made
  - `target_date` (date) - Future date being predicted
  - `predicted_price` (decimal) - Predicted price
  - `actual_price` (decimal) - Actual price (filled later)
  - `model_type` (text) - Model used: lstm, xgboost
  - `confidence_score` (decimal) - Prediction confidence (0-1)
  - `prediction_horizon` (integer) - Days ahead (7, 14, 30)
  - `features_used` (jsonb) - Features used in prediction
  - `created_at` (timestamptz)

  ### 6. `recommendations`
  Investment recommendations
  - `id` (uuid, primary key)
  - `stock_id` (uuid, foreign key)
  - `recommendation_date` (date)
  - `action` (text) - Action: buy, hold, sell
  - `confidence_score` (decimal) - Confidence (0-1)
  - `target_price` (decimal) - Target price
  - `current_price` (decimal) - Current price at recommendation
  - `technical_score` (decimal) - Technical analysis score
  - `fundamental_score` (decimal) - Fundamental analysis score
  - `reasoning` (text) - AI explanation
  - `risk_level` (text) - Risk: low, medium, high
  - `time_horizon` (text) - Short, medium, long term
  - `created_at` (timestamptz)

  ### 7. `user_watchlist`
  User's watched stocks
  - `id` (uuid, primary key)
  - `user_id` (uuid) - User identifier
  - `stock_id` (uuid, foreign key)
  - `created_at` (timestamptz)

  ## Security
  - Row Level Security (RLS) enabled on all tables
  - Public read access for stock data
  - Authenticated users can manage their watchlist

  ## Indexes
  - Performance indexes on frequently queried columns
  - Composite indexes for date range queries
*/

-- Create stocks table
CREATE TABLE IF NOT EXISTS stocks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ticker text UNIQUE NOT NULL,
  name text NOT NULL,
  exchange text NOT NULL,
  sector text,
  country text NOT NULL DEFAULT 'US',
  currency text NOT NULL DEFAULT 'USD',
  last_updated timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now()
);

-- Create stock_prices table
CREATE TABLE IF NOT EXISTS stock_prices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  date date NOT NULL,
  open decimal(20, 4) NOT NULL,
  high decimal(20, 4) NOT NULL,
  low decimal(20, 4) NOT NULL,
  close decimal(20, 4) NOT NULL,
  volume bigint NOT NULL,
  adjusted_close decimal(20, 4),
  created_at timestamptz DEFAULT now(),
  UNIQUE(stock_id, date)
);

-- Create technical_indicators table
CREATE TABLE IF NOT EXISTS technical_indicators (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  date date NOT NULL,
  rsi_14 decimal(10, 4),
  macd decimal(20, 4),
  macd_signal decimal(20, 4),
  macd_histogram decimal(20, 4),
  sma_20 decimal(20, 4),
  sma_50 decimal(20, 4),
  sma_200 decimal(20, 4),
  ema_12 decimal(20, 4),
  ema_26 decimal(20, 4),
  created_at timestamptz DEFAULT now(),
  UNIQUE(stock_id, date)
);

-- Create financial_statements table
CREATE TABLE IF NOT EXISTS financial_statements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  period_end date NOT NULL,
  statement_type text NOT NULL CHECK (statement_type IN ('income_statement', 'balance_sheet', 'cash_flow')),
  data jsonb NOT NULL,
  created_at timestamptz DEFAULT now(),
  UNIQUE(stock_id, period_end, statement_type)
);

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  prediction_date date NOT NULL DEFAULT CURRENT_DATE,
  target_date date NOT NULL,
  predicted_price decimal(20, 4) NOT NULL,
  actual_price decimal(20, 4),
  model_type text NOT NULL CHECK (model_type IN ('lstm', 'xgboost')),
  confidence_score decimal(5, 4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
  prediction_horizon integer NOT NULL,
  features_used jsonb,
  created_at timestamptz DEFAULT now()
);

-- Create recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  recommendation_date date NOT NULL DEFAULT CURRENT_DATE,
  action text NOT NULL CHECK (action IN ('buy', 'hold', 'sell')),
  confidence_score decimal(5, 4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
  target_price decimal(20, 4),
  current_price decimal(20, 4) NOT NULL,
  technical_score decimal(5, 4),
  fundamental_score decimal(5, 4),
  reasoning text NOT NULL,
  risk_level text CHECK (risk_level IN ('low', 'medium', 'high')),
  time_horizon text CHECK (time_horizon IN ('short', 'medium', 'long')),
  created_at timestamptz DEFAULT now()
);

-- Create user_watchlist table
CREATE TABLE IF NOT EXISTS user_watchlist (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  stock_id uuid NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  UNIQUE(user_id, stock_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_stock_prices_stock_date ON stock_prices(stock_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_stock_prices_date ON stock_prices(date DESC);
CREATE INDEX IF NOT EXISTS idx_technical_indicators_stock_date ON technical_indicators(stock_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_stock_date ON predictions(stock_id, prediction_date DESC);
CREATE INDEX IF NOT EXISTS idx_recommendations_stock_date ON recommendations(stock_id, recommendation_date DESC);
CREATE INDEX IF NOT EXISTS idx_financial_statements_stock_period ON financial_statements(stock_id, period_end DESC);
CREATE INDEX IF NOT EXISTS idx_stocks_ticker ON stocks(ticker);
CREATE INDEX IF NOT EXISTS idx_user_watchlist_user ON user_watchlist(user_id);

-- Enable Row Level Security
ALTER TABLE stocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE stock_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE technical_indicators ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_statements ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_watchlist ENABLE ROW LEVEL SECURITY;

-- RLS Policies for public read access to stock data
CREATE POLICY "Anyone can view stocks"
  ON stocks FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can view stock prices"
  ON stock_prices FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can view technical indicators"
  ON technical_indicators FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can view financial statements"
  ON financial_statements FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can view predictions"
  ON predictions FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can view recommendations"
  ON recommendations FOR SELECT
  TO public
  USING (true);

-- RLS Policies for user_watchlist (authenticated users only)
CREATE POLICY "Users can view own watchlist"
  ON user_watchlist FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can add to own watchlist"
  ON user_watchlist FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove from own watchlist"
  ON user_watchlist FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);
