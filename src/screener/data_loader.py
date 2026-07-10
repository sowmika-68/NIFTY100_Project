import pandas as pd


class DataLoader:
    """
    Loads all datasets required for the Screener Engine.
    """

    def __init__(self):

        self.financial_ratios = "data/financial_ratios.xlsx"
        self.market_cap = "data/market_cap.xlsx"
        self.profit_loss = "data/profitandloss.xlsx"
        self.analysis = "data/analysis.xlsx"
        self.sectors = "data/sectors.xlsx"

    def load_financial_ratios(self):

        return pd.read_excel(self.financial_ratios)

    def load_market_cap(self):

        return pd.read_excel(self.market_cap)

    def load_profit_loss(self):

        return pd.read_excel(
            self.profit_loss,
            header=1
        )

    def load_analysis(self):

        return pd.read_excel(
            self.analysis,
            header=1
        )

    def load_sectors(self):

        return pd.read_excel(self.sectors)

    def load_all(self):

        return {
            "financial_ratios": self.load_financial_ratios(),
            "market_cap": self.load_market_cap(),
            "profit_loss": self.load_profit_loss(),
            "analysis": self.load_analysis(),
            "sectors": self.load_sectors()
        }


if __name__ == "__main__":

    loader = DataLoader()

    datasets = loader.load_all()

    for name, df in datasets.items():

        print("=" * 60)

        print(name)

        print(df.head())

        print(df.shape)