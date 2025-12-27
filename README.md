# Stock Price Prediction & Investment Recommendation Platform

A full-stack web application for stock price prediction and investment recommendations using machine learning. The platform supports both US and Indonesian (IDX) stocks and provides comprehensive technical and fundamental analysis.

## Features

- **Stock Data Fetching**: Real-time and historical stock price data for US and IDX markets
- **Technical Analysis**: RSI, MACD, Moving Averages (SMA 20/50/200, EMA 12/26)
- **ML Price Prediction**: LSTM and XGBoost models for 7-30 day price forecasting
- **Investment Recommendations**: AI-generated Buy/Hold/Sell recommendations with confidence scores
- **Financial Analysis**: Balance sheet, income statement, and cash flow data
- **Interactive Charts**: Historical vs predicted prices with Recharts
- **Risk Assessment**: Low/Medium/High risk levels for each recommendation
- **AI Explanations**: Detailed reasoning for every recommendation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.10+** - Core language
- **TensorFlow/Keras** - LSTM neural networks
- **XGBoost** - Gradient boosting for predictions
- **yfinance** - Stock data fetching
- **ta** - Technical analysis indicators
- **Pandas/NumPy** - Data processing
- **Supabase** - Database and authentication

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Recharts** - Interactive charts
- **Axios** - HTTP client
- **Lucide React** - Icons

### Database
- **PostgreSQL** (via Supabase) - Relational database
- **Row Level Security** - Data protection

## Architecture

```
project/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database connection
│   ├── models.py                  # Pydantic data models
│   ├── stock_service.py           # Stock data fetching
│   ├── technical_indicators.py    # Technical analysis
│   ├── ml_models.py               # ML prediction models
│   ├── recommendation_engine.py   # Recommendation logic
│   └── requirements.txt           # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StockSearch.tsx
│   │   │   ├── StockHeader.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   ├── RecommendationCard.tsx
│   │   │   ├── TechnicalIndicators.tsx
│   │   │   └── FinancialSummary.tsx
│   │   ├── lib/
│   │   │   ├── supabase.ts
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── index.css
│   └── package.json
│
└── supabase/
    └── migrations/
        └── create_stock_prediction_schema.sql
```

## Database Schema

### Tables

1. **stocks** - Basic stock information
2. **stock_prices** - Historical price data
3. **technical_indicators** - RSI, MACD, Moving Averages
4. **financial_statements** - Income statement, balance sheet, cash flow
5. **predictions** - ML model predictions
6. **recommendations** - Buy/Hold/Sell recommendations
7. **user_watchlist** - User's watched stocks

All tables include Row Level Security policies for data protection.

## API Endpoints

### Main Endpoints

- `POST /api/analyze` - Analyze stock and generate predictions
  - Request: `{ ticker: string, prediction_days: number, model_type: 'lstm' | 'xgboost' }`
  - Returns: Complete analysis with predictions and recommendations

- `GET /api/stock/{ticker}` - Get stock information
- `GET /api/predictions/{stock_id}` - Get predictions for a stock
- `GET /api/recommendations/{stock_id}` - Get recommendations for a stock
- `GET /api/stocks/search?query={query}` - Search for stocks

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- pip and npm

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# The .env file is already configured with Supabase credentials

# Run the backend server
python main.py
# Server will start on http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# The .env file is already configured

# Run the development server
npm run dev
# Server will start on http://localhost:5173
```

### Build for Production

```bash
cd frontend
npm run build
```

## Usage

1. **Enter a Stock Ticker**: Type a stock symbol (e.g., AAPL, MSFT, BBCA.JK)
2. **Select Prediction Period**: Choose 7, 14, or 30 days
3. **Choose ML Model**: Select LSTM or XGBoost
4. **Click Analyze**: The system will:
   - Fetch historical price data
   - Calculate technical indicators
   - Run ML predictions
   - Generate investment recommendations
   - Display interactive charts and analysis

## ML Models

### XGBoost (Recommended)
- **Type**: Gradient Boosting
- **Features**: 60-day lookback window
- **Speed**: Fast training and prediction
- **Accuracy**: Good for short-term predictions
- **Use Case**: Quick analysis, day trading

### LSTM
- **Type**: Deep Learning (Recurrent Neural Network)
- **Features**: Sequential pattern learning
- **Speed**: Slower training
- **Accuracy**: Better for complex patterns
- **Use Case**: Long-term trends, detailed analysis

## Recommendation Logic

The system generates Buy/Hold/Sell recommendations based on:

1. **Technical Score (40%)**: RSI, MACD, Moving Averages
2. **Fundamental Score (30%)**: P/E ratio, ROE, Debt/Equity, Revenue Growth
3. **ML Prediction (30%)**: Predicted price change

### Action Criteria
- **Buy**: Predicted increase > 5% AND combined score > 0.6
- **Sell**: Predicted decrease > 5% AND combined score < 0.4
- **Hold**: All other cases

## Technical Indicators

- **RSI (14)**: Identifies overbought (>70) and oversold (<30) conditions
- **MACD**: Trend-following momentum indicator
- **SMA 20/50/200**: Short, medium, and long-term trends
- **EMA 12/26**: Fast and slow exponential moving averages

## Sample Stocks

### US Markets
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Alphabet)
- TSLA (Tesla)
- AMZN (Amazon)

### Indonesian IDX
- BBCA.JK (Bank Central Asia)
- BBRI.JK (Bank Rakyat Indonesia)
- TLKM.JK (Telkom Indonesia)
- ASII.JK (Astra International)

## Important Disclaimer

⚠️ **IMPORTANT**: This platform is for educational and informational purposes only.

- NOT financial advice
- Past performance does NOT guarantee future results
- AI predictions can be inaccurate
- Always conduct your own research
- Consult a licensed financial advisor before investing
- Invest only what you can afford to lose
- The creators assume NO responsibility for investment decisions

## Future Enhancements

Potential features for scaling:

1. **User Authentication**: Personal portfolios and watchlists
2. **Real-time Updates**: WebSocket connections for live data
3. **Alerts**: Price and prediction notifications
4. **Backtesting**: Historical accuracy metrics
5. **News Sentiment**: NLP analysis of financial news
6. **Options Analysis**: Call/Put recommendations
7. **Portfolio Optimization**: Modern Portfolio Theory
8. **Social Features**: Community insights and discussions
9. **Mobile App**: React Native application
10. **Advanced Models**: Transformer-based predictions

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review API endpoint documentation at `/docs` (FastAPI automatic docs)

---

Built with Python, FastAPI, React, and Machine Learning
