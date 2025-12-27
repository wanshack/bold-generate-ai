# Quick Start Guide

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed

## Installation

### 1. Backend Setup (Terminal 1)

```bash
cd backend

# Install Python dependencies
pip3 install -r requirements.txt --break-system-packages

# Start the backend server
python3 main.py
```

Backend will start on: http://localhost:8000

### 2. Frontend Setup (Terminal 2)

```bash
cd frontend

# Dependencies are already installed
# Start the development server
npm run dev
```

Frontend will start on: http://localhost:5173

## Quick Launch (Alternative)

Use the provided start script:

```bash
chmod +x start.sh
./start.sh
```

This will start both backend and frontend servers simultaneously.

## Testing the Application

1. Open your browser to http://localhost:5173
2. Enter a stock ticker:
   - US stocks: AAPL, MSFT, GOOGL, TSLA, AMZN
   - Indonesian (IDX): BBCA.JK, BBRI.JK, TLKM.JK
3. Select prediction period (7, 14, or 30 days)
4. Choose ML model (XGBoost recommended for speed)
5. Click "Analyze Stock"

The system will:
- Fetch historical price data
- Calculate technical indicators
- Generate ML predictions
- Provide investment recommendations

## API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example API Request

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "prediction_days": 30,
    "model_type": "xgboost"
  }'
```

## Troubleshooting

### Backend Issues

**Problem**: Python package installation fails
```bash
# Try installing with system packages override
pip3 install -r requirements.txt --break-system-packages
```

**Problem**: Port 8000 already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Problem**: Port 5173 already in use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

**Problem**: Module not found errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Issues

The Supabase database is pre-configured. If you encounter issues:
- Check the .env files in both frontend and backend directories
- Verify the Supabase credentials are correct
- Check your internet connection

## Features to Try

1. **Compare Models**: Run the same stock with both LSTM and XGBoost
2. **Different Timeframes**: Compare 7-day vs 30-day predictions
3. **Multiple Stocks**: Analyze different stocks to see varied recommendations
4. **Technical Indicators**: Pay attention to RSI and MACD signals
5. **Risk Assessment**: Notice how confidence scores affect recommendations

## Support

For detailed documentation, see README.md in the project root.
