# Algorithmic Trading

Algorithmic trading is a method for automating trading instructions in the context of investment banks and hedge funds, in order to leverage the speed of computers relative to human traders.

The projects found in this repository are all related with different approaches of algorithmic trading using **Python**. The objective of this projects is to learn and become familiar with several APIs and libraries that allow this interaction between stock trading and data science.

## Equal-Weight S&P500 index fund

The S&P 500 is the world's most popular stock market index. 
This Python script accepts the value of a portfolio in USD from the terminal and calculates how many shares of each S&P 500 stock  should be purchased to get an equal-weight investment in the index fund.

The stock market data is extracted with [IEXCloud API](). It's important to note that the token ID currently introduced is a for the free sandbox API, that returns random data. In order to get meaningful values a real API license needs to be purchased.

In order to execute the script:
```
$> python3 eSP500.py
```

After that, a prompt will ask for a portfolio value (quantity to be invested) in USD. The output will be calculated and stored in a `.xsls` file, saved in the same directory.

```
$> Enter the value of your portfolio(USD$): 10000000
$> Saved. Data in recomendedTrades.xlsx
```

<p align="center">
  <img src='readme_img/eSP500.png'/ >
</p>
