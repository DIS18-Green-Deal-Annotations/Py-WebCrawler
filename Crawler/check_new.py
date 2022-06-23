import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import get_links
import pandas as pd
from datetime import datetime
import regex as re
import urllib.request
import os

# This is the default landing page on which you should find all the EGD documents
linklist = get_links.fromURL(r"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents")

def check():
    num_newlinks = 0
    headers = ",Title,Link,Date of document,Download date,Downloaded language,Downloaded doctype,Author,Form,Subject matter"
    # Look for the base file
    if not os.path.exists("known_html_files.csv"):
        # If file doesnt exists then create it and add the needed headers
        with open("known_html_files.csv", 'w') as f:
            f.write(headers)
    # If file exists then check if the first row contains the needed headers -> if not then add them
    else:
        with open("known_html_files.csv", 'r+') as f:
            if not f.readline().rstrip() == headers:
                file_content = f.read()
                f.seek(0, 0)
                f.write(headers + "\n" + file_content)
    # Read in the file containing metadata
    known_html_files = pd.read_csv("known_html_files.csv", index_col=0)
    # Go through all files on the linklist page and see if there is one not indexed yet
    for link in linklist.get():
        # If it found a new/unknown file then add it to the known_html_files file
        if not link in known_html_files["Link"].tolist():
            num_newlinks += 1
            data = pd.DataFrame([get_document_metadata(link)])
            known_html_files = pd.concat([known_html_files, data], ignore_index=True)
            # Download the html content of the file
            downloader(link)
            print(f"Found and downloaded {num_newlinks} new document" + ("s" if num_newlinks > 1 or num_newlinks == 0 else ""), end="\r")
    else:
        print("\n")
    if num_newlinks == 0:
        print(f"Couldn't find any new documents.")
    print(f"There are currently {len(known_html_files)} files indexed")
    known_html_files.to_csv("known_html_files.csv")

def get_document_metadata(link):
    # Meta Stuff
    soup = BeautifulSoup(requests.get(link).content, "lxml")
    metacomment = str(soup.find("div", {"class": "content"}).find(string=lambda text: isinstance(text, Comment)))
    metalink = link.replace("/TXT/HTML/", "/ALL/")
    metasoup = BeautifulSoup(requests.get(metalink).content, "lxml")
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
    filename = link.split("uri=")[1]
    tobereplaced = [";",",",".",":"]
    for char in tobereplaced:
        filename = filename.replace(char, "_")
    # Download the html content if not already done
    if not os.path.exists("./html/" + filename + ".html"):
        response = urllib.request.urlopen(link)
        webContent = response.read().decode('UTF-8')
        with open(f'./html/{filename}.html', 'w', encoding="utf-8") as f:
            f.write(webContent)
            f.close