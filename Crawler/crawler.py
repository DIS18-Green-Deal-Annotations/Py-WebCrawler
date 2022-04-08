from bs4 import BeautifulSoup
import get_links
import get_tables
import check_new
linklist = get_links.fromURL(r"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents")


# print(len(linklist.get())) # Printing number of links
# print(*linklist.get(), sep="\n") # Printing all links to the documents

# for link in linklist.get():
#     tables = get_tables.fromURL(link)
#     print(tables.get())

check_new.check()
