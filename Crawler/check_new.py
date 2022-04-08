import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import get_links
import pandas as pd
from datetime import datetime
import regex as re

linklist = get_links.fromURL(r"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents")

def check():
    num_newlinks = 0
    known_html_files = pd.read_csv("known_html_files.csv", index_col=0)
    for link in linklist.get():
        if not link in known_html_files["Link"].tolist():
            num_newlinks += 1
            data = pd.DataFrame([get_document_metadata(link)])
            known_html_files = pd.concat([known_html_files, data], ignore_index=True)
    # Creating a unique ID
    # known_html_files["UID"] = known_html_files.groupby("Link").ngroup()
    known_html_files.to_csv("known_html_files.csv")

def get_document_metadata(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "lxml")
    metacomment = str(soup.find("div", {"class": "content"}).find(string=lambda text: isinstance(text, Comment)))
    # Meta Stuff
    metalink = link.replace("/TXT/HTML/", "/ALL/")
    metapage = requests.get(metalink)
    metasoup = BeautifulSoup(metapage.content, "lxml")
    dataframe_dict = {}
    dataframe_dict["Title"] = soup.find("p", {"class": "Titreobjet_cp"}).text.replace('\n','')
    dataframe_dict["Link"] = link
    dataframe_dict["Date of document"] = soup.find("p", {"class": "Emission"}).text.split(",")[1].strip()
    dataframe_dict["Download date"] = datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")
    dataframe_dict["Downloaded language"] = re.findall(r"""name=LW_LANGUE;value=\"(.+?(?=\"))""", metacomment)[0]
    dataframe_dict["Downloaded doctype"] = "HTML"
    dataframe_dict["Author"] = metasoup.find(id="PPMisc_Contents").dl.find_all("dd")[0].text.strip()
    dataframe_dict["Form"] = metasoup.find(id="PPMisc_Contents").dl.find_all("dd")[2].text.strip()
    dataframe_dict["Subject matter"] = metasoup.find(id="PPClass_Contents").dl.find_all("dd")[0].text.strip().replace('\n\n','').replace('\n',';')
    return dataframe_dict

def downloader(link):
    return