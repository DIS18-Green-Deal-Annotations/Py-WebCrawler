import requests
from bs4 import BeautifulSoup
import re
class fromURL:
    def __init__(self, url):
        self.url = url

    def get(self):
        soup = BeautifulSoup(requests.get(self.url).content, "lxml")
        document_list = soup.find(id = "documents")
        document_links = []
        for documents in document_list.find_all("div", class_ = "field field-name-field-core-legacy-link field--field-core-legacy-link"):
            link = documents.find("div", class_ = "file").a["href"]
            content_page_link = BeautifulSoup(requests.get(link).content, "lxml")
            link = re.sub("nl/", "en/", link, flags=re.IGNORECASE).replace("%3A", ":")
            if content_page_link.find(id="format_language_table_HTML_EN", class_ = "disabled"):
                link = re.sub("en/", "de/", link, flags=re.IGNORECASE)
                # Check if link contains qid
            elif content_page_link.find(id="format_language_table_HTML_DE", class_ = "disabled"):
                print("Skipped document with following link as no known language could be found!\n", link)
            if link.rfind("qid=") != -1:
                # Removing non-necessary qid part
                link = link[:link.rfind("qid=") -1]
            html = link.rfind("TXT/")
            link = link[:html + 4] + "HTML/?" + link[html + 5:]
            document_links.append(link)
        return document_links

if __name__ == "__main__":
    print(fromURL(r"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents").get())