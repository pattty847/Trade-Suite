import pandas as pd

class Stats():
    def __init__(self) -> None:

        self.URL = 'https://coinalyze.net/'
        self.stats = pd.read_html(self.URL)[0][["Coin", "Price", "Chg 24H", "Vol 24H", "Open Interest", "OI Chg 24H", "OI Share", "OI / VOL24H", "FR AVG", "PFR AVG", "Liqs. 24H"]]
        
        try:
            with open("CSV\\previous_stats.csv", "r"):
                self.previous_stats = pd.read_csv("CSV\\previous_stats.csv")
        except FileNotFoundError as e:
            self.stats.to_csv(f"previous_stats.csv", index=False)
            self.previous_stats = None


    def get_stats(self):
        return self.stats