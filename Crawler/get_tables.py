from cmath import nan
import pandas as pd
class fromURL:
    def __init__(self, url):
        self.url = url

    def get(self):
        try:
            pd.read_html(self.url)
            tables = pd.read_html(self.url)
            return tables
        except ValueError:
            return pd.NA
