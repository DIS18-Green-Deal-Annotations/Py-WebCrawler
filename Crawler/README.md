# HTML Crawler explanation

## Files explanation

The crawler consists of 4 individual files:

### crawler.py

This file is supposed to be the baseline. From this file all scripts should be started as required.

### get_links.py

Here all the links from the [European Green Deal landingpage](https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/delivering-european-green-deal_en#documents) are getting crawled. Currently only HTML files are crawled as they can be simply parsed with bs4.

### get_tables.py

This is only relevant for the Table-Extraction group as this script automatically extracts the Tables out of all HTML files for further use.

### check_new.py

This is the most important file. It contains three functions that work together to check if there are any new files that havent been indexed before, extract metadata and downloads them if they havent been before. All downloaded HTML files can be [found here](./html)

## Script usage

Make sure to install the required packages first with the following command: `pip install -r requirements.txt`.  
You can also create a virtual environment beforehand. The documentation for creating venvs in native python can be [found here](https://docs.python.org/3/library/venv.html).
In its current state the [crawler.py](crawler.py) can simply be called with `py crawler.py`. This will try to find and download new files.  
The [known_html_files](known_html_files.csv) file contains some metadata of the documents and will also be updated as the [crawler.py](crawler.py) is executed.
