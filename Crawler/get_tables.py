import requests
from bs4 import BeautifulSoup
import os
class fromURL:
    def __init__(self, url):
        self.url = url

    def download(self):
        count = 0
        if not os.path.exists("./html_tables/"):
            os.makedirs("./html_tables/")
        filename = self.url.split("uri=")[1]
        tobereplaced = [";",",",".",":"]
        for char in tobereplaced:
            filename = filename.replace(char, "_")
        soup = BeautifulSoup(requests.get(self.url).content, "lxml")
        tables = soup.find_all("table")
        for table in tables:
            count += 1
            if not os.path.exists(f"./html_tables/{filename}_table_{count}.html"):
                with open(f"./html_tables/{filename}_table_{count}.html", 'w', encoding="utf-8") as f:
                    f.write(table.prettify())
                    f.close