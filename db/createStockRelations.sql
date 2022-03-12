
CREATE TABLE Stocks(
    ticker VARCHAR(20) NOT NULL,
    name VARCHAR(300),
    sector VARCHAR(300),
    PRIMARY KEY (ticker)
);

CREATE TABLE TimeData (
    ticker VARCHAR(20) NOT NULL REFERENCES Stocks(ticker),
    period DATE NOT NULL,
    closePrice DECIMAL(12,2),
    highPrice DECIMAL(12,2),
    lowPrice DECIMAL(12,2),
    transactionCount int,
    openPrice DECIMAL(12,2),
    tradingVolume DECIMAL(12,2),
    volumeWeightedAveragePrice DECIMAL(12,2),
    PRIMARY KEY (ticker,period)

);