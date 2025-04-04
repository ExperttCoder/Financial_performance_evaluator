# Financial Performance Evaluator

A comprehensive backtesting framework for evaluating investment strategies based on momentum factors and market signals.

## 🎯 Overview

This framework is designed to evaluate the effectiveness of investment strategies based on key market factors, particularly momentum. The strategy focuses on buying stocks that exhibit momentum (using 6 identified momentum factors) and selling them when they are out of momentum.

### Key Features
- 📊 Multi-source data handling (Yahoo Finance, CSV, Excel)
- 🔄 Six momentum factor implementation
- 📈 Comprehensive performance analytics
- 📉 Advanced visualization tools
- 🛠️ Modular and scalable architecture
- 📝 Detailed documentation and type hints

## 🏗️ Project Structure

```
├── backtesting/          # Main package
│   ├── data/            # Data collection and processing
│   │   ├── __init__.py
│   │   └── loader.py    # Data loading utilities
│   ├── engine/          # Backtesting engine
│   ├── analysis/        # Performance analysis
│   ├── visualization/   # Visualization tools
│   ├── utils/          # Utility functions
│   ├── config/         # Configuration files
│   └── tests/          # Unit tests
├── docs/               # Documentation
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🚀 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ExperttCoder/Financial_performance_evaluator.git
   cd Financial_performance_evaluator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Usage Example

```python
from backtesting.engine.backtest import Backtest
from backtesting.data.loader import DataLoader
from backtesting.config.strategy import MomentumStrategy

# Load data
data_loader = DataLoader()
data = data_loader.load_from_source('yfinance', 
                                  symbols=['AAPL', 'MSFT', 'GOOG'],
                                  start_date='2010-01-01',
                                  end_date='2023-12-31')

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

## 🔍 Features in Detail

### Data Collection & Processing
- Multiple data source support
- Automated data cleaning
- Missing data handling
- Time series alignment

### Momentum Factors
1. Price Momentum
2. Volume Momentum
3. Relative Strength Index (RSI)
4. Moving Average Convergence Divergence (MACD)
5. Rate of Change (ROC)
6. Bollinger Band Position

### Analysis Capabilities
- Return metrics calculation
- Risk metrics evaluation
- Performance attribution
- Statistical significance testing

### Visualization Tools
- Equity curves
- Drawdown analysis
- Factor contribution charts
- Performance heat maps

## 📈 Performance Metrics

The framework calculates and reports:
- Sharpe Ratio
- Maximum Drawdown
- Alpha & Beta
- Information Ratio
- Win/Loss Ratio
- Factor Attribution

## 🛠️ Development

### Running Tests
```bash
pytest backtesting/tests/
```

### Adding New Features
1. Create a new branch
2. Implement feature
3. Add tests
4. Submit pull request

## 📝 Documentation

Detailed documentation is available in the `docs/` directory:
- Strategy Implementation Guide
- Factor Analysis Documentation
- API Reference
- Performance Metrics Guide

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions and feedback, please open an issue on GitHub.