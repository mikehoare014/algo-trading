# Algorithmic Trading Project

This repository contains a Python-based algorithmic trading system that focuses on trading major US stocks, including top 50 companies by market capitalization.

## Project Structure

```
├── alpacha.py         # Main algorithm implementation
├── main.py           # Entry point of the application
├── plotting.py       # Visualization utilities
├── requirements.txt  # Project dependencies
└── legacy/          # Legacy code and notebooks
    ├── alpacha.ipynb
    ├── test.ipynb
    └── trading_strategy.py
```

## Covered Stocks

The project tracks 50 major US stocks including:
- Technology (AAPL, MSFT, GOOGL, META)
- Finance (JPM, BAC, GS)
- Healthcare (JNJ, PFE, UNH)
- Consumer (AMZN, WMT, DIS)
- And many more blue-chip companies

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/mikehoare014/algo-trading.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the main script:
```bash
python main.py
```

## Features

- Real-time market data processing
- Technical analysis tools
- Automated trading strategies
- Data visualization and plotting utilities
- Backtesting capabilities

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational and research purposes only. Do not use this system for actual trading without proper understanding of the risks involved in algorithmic trading. Always consult with a financial advisor before making investment decisions.