import requests
from bs4 import BeautifulSoup
class fromURL:
    def __init__(self, url):
        self.url = url

    def get(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")
        document_list = soup.find(id = "documents")
        document_links = []
        for documents in document_list.find_all("div", class_ = "field field-name-field-core-legacy-link field--field-core-legacy-link"):
            link = documents.find("div", class_ = "file").a["href"]
            link = link.replace("nl/", "en/").replace("%3A", ":")
            link = link.replace("ga/", "de/").replace("%3A", ":")
            # Check if link contains qid
            if link.rfind("qid=") != -1:
                # Removing non-necessary qid part
                link = link[:link.rfind("qid=") -1] 
            html = link.rfind("TXT/")
            link = link[:html + 4] + "HTML/?" + link[html + 5:]
            document_links.append(link)
        return document_links