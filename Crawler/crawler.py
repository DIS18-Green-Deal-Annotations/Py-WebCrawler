import get_links
import get_tables
import check_new
linklist = get_links.fromURL(r"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents")

done = False
while done is False:
    try:
        if __name__ == "__main__":
            print("Checking for new documents ...")
            check_new.check()
            print("Done!")
        
        download_tables = input("Would you like to download the tables of each document to './html_tables' ? [y/n]: ").lower()
        if download_tables == "y":
            count = 0
            for link in linklist.get():
                count += 1
                tables = get_tables.fromURL(link)
                tables.download()
                print(f"Downloaded tables from {count} document" + ("s" if count > 1 or count == 0 else ""), end="\r")
            print("\n")
        
        done = True
    except AttributeError:
        print("Error. Trying again ...")
        pass