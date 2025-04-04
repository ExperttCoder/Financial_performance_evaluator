# Momentum Strategy Backtesting Framework

A comprehensive backtesting framework for evaluating investment strategies based on momentum factors.

## Overview

This framework is designed to evaluate the effectiveness of an investment strategy based on key market factors, particularly momentum. The strategy focuses on buying stocks that exhibit momentum (using 6 identified momentum factors) and selling them when they are out of momentum.

## Project Structure

```
├── backtesting/          # Main package
│   ├── data/             # Data collection and processing
│   ├── engine/           # Backtesting engine
│   ├── analysis/         # Performance analysis
│   ├── visualization/    # Visualization tools
│   ├── utils/            # Utility functions
│   ├── config/           # Configuration files
│   └── tests/            # Unit tests
├── docs/                 # Documentation
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Example code for running a backtest:

```python
from backtesting.engine.backtest import Backtest
from backtesting.data.loader import DataLoader
from backtesting.config.strategy import MomentumStrategy

# Load data
data_loader = DataLoader()
data = data_loader.load_from_source('yfinance', symbols=['AAPL', 'MSFT', 'GOOG'], 
                                    start_date='2010-01-01', end_date='2023-12-31')

# Define strategy with momentum factors
strategy = MomentumStrategy(momentum_factors=6)

# Create and run backtest
backtest = Backtest(data=data, strategy=strategy, initial_capital=100000)
results = backtest.run()

# Analyze results
performance = results.analyze()
performance.plot_equity_curve()
performance.print_statistics()
```

## Features

- Data collection from various sources (Yahoo Finance, CSV, etc.)
- Momentum factor calculation and analysis
- Flexible backtesting engine
- Comprehensive performance metrics
- Visualization tools for analysis
- Parameter optimization

## License

MIT 