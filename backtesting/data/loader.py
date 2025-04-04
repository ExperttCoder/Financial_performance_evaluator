"""
Data loading module for the backtesting framework.
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Union, Optional, Tuple


class DataLoader:
    """
    Class for loading financial data from various sources.
    """
    
    def __init__(self):
        """Initialize the DataLoader."""
        self.data = {}
        
    def load_from_source(self, 
                         source: str, 
                         symbols: List[str],
                         start_date: str,
                         end_date: str,
                         interval: str = '1d',
                         **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Load data from the specified source.
        
        Parameters
        ----------
        source : str
            Data source ('yfinance', 'csv', 'excel')
        symbols : List[str]
            List of ticker symbols to load
        start_date : str
            Start date for data in format 'YYYY-MM-DD'
        end_date : str
            End date for data in format 'YYYY-MM-DD'
        interval : str, optional
            Data interval, by default '1d'
        **kwargs : dict
            Additional keyword arguments for specific data sources
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of DataFrames with symbols as keys
        """
        if source.lower() == 'yfinance':
            return self._load_from_yfinance(symbols, start_date, end_date, interval, **kwargs)
        elif source.lower() == 'csv':
            return self._load_from_csv(symbols, **kwargs)
        elif source.lower() == 'excel':
            return self._load_from_excel(symbols, **kwargs)
        else:
            raise ValueError(f"Unsupported data source: {source}")
    
    def _load_from_yfinance(self, 
                           symbols: List[str],
                           start_date: str,
                           end_date: str,
                           interval: str = '1d',
                           **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Load data from Yahoo Finance.
        
        Parameters
        ----------
        symbols : List[str]
            List of ticker symbols to load
        start_date : str
            Start date for data in format 'YYYY-MM-DD'
        end_date : str
            End date for data in format 'YYYY-MM-DD'
        interval : str, optional
            Data interval, by default '1d'
        **kwargs : dict
            Additional keyword arguments for yfinance
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of DataFrames with symbols as keys
        """
        result = {}
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date, interval=interval)
            
            # Ensure the DataFrame has the required columns
            if 'Open' not in df.columns or 'Close' not in df.columns:
                print(f"Warning: Missing required columns for symbol {symbol}")
                continue
                
            # Rename columns to standardized format
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            result[symbol] = df
            
        self.data.update(result)
        return result
    
    def _load_from_csv(self, 
                      symbols: List[str],
                      directory: str = './data',
                      **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Load data from CSV files.
        
        Parameters
        ----------
        symbols : List[str]
            List of ticker symbols to load
        directory : str, optional
            Directory containing CSV files, by default './data'
        **kwargs : dict
            Additional keyword arguments for pd.read_csv
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of DataFrames with symbols as keys
        """
        result = {}
        for symbol in symbols:
            file_path = os.path.join(directory, f"{symbol}.csv")
            if not os.path.exists(file_path):
                print(f"Warning: File not found for symbol {symbol} at {file_path}")
                continue
                
            df = pd.read_csv(file_path, **kwargs)
            
            # Convert date column to datetime if it exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            
            # Ensure DataFrame has required columns
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col not in df.columns:
                    print(f"Warning: Missing required column '{col}' for symbol {symbol}")
                
            result[symbol] = df
            
        self.data.update(result)
        return result
    
    def _load_from_excel(self, 
                        symbols: List[str],
                        file_path: str,
                        **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Load data from Excel file with multiple sheets.
        
        Parameters
        ----------
        symbols : List[str]
            List of ticker symbols to load (should match sheet names)
        file_path : str
            Path to Excel file
        **kwargs : dict
            Additional keyword arguments for pd.read_excel
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of DataFrames with symbols as keys
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
            
        result = {}
        for symbol in symbols:
            try:
                df = pd.read_excel(file_path, sheet_name=symbol, **kwargs)
                
                # Convert date column to datetime if it exists
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                    df.set_index('date', inplace=True)
                
                result[symbol] = df
            except Exception as e:
                print(f"Error loading sheet for symbol {symbol}: {e}")
                
        self.data.update(result)
        return result
    
    def calculate_returns(self, 
                         symbols: List[str] = None, 
                         period: int = 1,
                         method: str = 'simple') -> Dict[str, pd.DataFrame]:
        """
        Calculate returns for the loaded data.
        
        Parameters
        ----------
        symbols : List[str], optional
            List of symbols to calculate returns for, by default None (all symbols)
        period : int, optional
            Period for return calculation, by default 1
        method : str, optional
            Return calculation method ('simple' or 'log'), by default 'simple'
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of DataFrames with returns added
        """
        if symbols is None:
            symbols = list(self.data.keys())
            
        for symbol in symbols:
            if symbol not in self.data:
                print(f"Warning: No data loaded for symbol {symbol}")
                continue
                
            df = self.data[symbol].copy()
            
            if method.lower() == 'simple':
                df['return'] = df['close'].pct_change(period)
            elif method.lower() == 'log':
                df['return'] = np.log(df['close'] / df['close'].shift(period))
            else:
                raise ValueError(f"Unsupported return calculation method: {method}")
                
            self.data[symbol] = df
            
        return {symbol: self.data[symbol] for symbol in symbols}
    
    def get_data(self, symbol: str) -> pd.DataFrame:
        """
        Get data for a specific symbol.
        
        Parameters
        ----------
        symbol : str
            Ticker symbol
            
        Returns
        -------
        pd.DataFrame
            DataFrame with price data
        """
        if symbol not in self.data:
            raise KeyError(f"No data loaded for symbol {symbol}")
            
        return self.data[symbol]
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Get all loaded data.
        
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary of all loaded DataFrames
        """
        return self.data 