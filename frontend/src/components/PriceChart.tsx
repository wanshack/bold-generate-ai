import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { StockPrice, Prediction } from '../types';

interface PriceChartProps {
  historicalPrices: StockPrice[];
  predictions: Prediction[];
  currency: string;
}

const PriceChart: React.FC<PriceChartProps> = ({ historicalPrices, predictions, currency }) => {
  const chartData = [
    ...historicalPrices.slice(-60).map((price) => ({
      date: new Date(price.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      historical: price.close,
      predicted: null
    })),
    ...predictions.map((pred) => ({
      date: new Date(pred.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      historical: null,
      predicted: pred.price
    }))
  ];

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1.5rem' }}>Price Chart - Historical vs Predicted</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis
            dataKey="date"
            stroke="var(--text-secondary)"
            tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke="var(--text-secondary)"
            tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
            domain={['auto', 'auto']}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              color: 'var(--text-primary)'
            }}
            formatter={(value: any) => [`${currency} ${Number(value).toFixed(2)}`, '']}
          />
          <Legend wrapperStyle={{ color: 'var(--text-primary)' }} />
          <Line
            type="monotone"
            dataKey="historical"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
            name="Historical Price"
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#10b981', r: 3 }}
            name="Predicted Price"
            connectNulls={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
