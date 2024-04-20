# Search Engine for [react](https://react.dev/) website

## Abstract
The project aims to develop a web scraping and search engine system utilizing Scrapy for web scraping and Scikit-learn for implementing TF-IDF scoring. Two approaches are implemented for TF-IDF scoring: one using Scikit-learn and the other using custom code. The system allows users to perform web searches by providing a query through a POST API using Flask. The website already has search functionality. The results of the two methods are compared with the search option on the site.

## Overview
As we need to design an search engine and filter the results with TF-IDF scores, intially a web scrapper is built to crawl the website. Then the scrapped data is processed in two different ways. First way is by generating an index with TF-IDF scores and finding the cosine similarity of the given query using the scikit learn library. Second way is by the same process without the library. It's done by programmatically calculating the relevant scores. Two separate APIs are built for both methods to output the top 5 search results in json format. Both the results are compared to the results found through search functionality of the website.

## Design
1) The web scraper crawls the site and downloads the HTML content and metadata as JSON files for each page.
2) The JSON pages are processed, and an index with TF-IDF scores is created. It is done in two ways: one using Scikit-learn and the other by creating term frequencies and calculating the TF-IDF programmatically.
3) Once the Flask server is started, two POST APIs are available to get the top five search results based on either Scikit TF-IDF or programmatic TF-IDF.

## Architecture
There are 3 important steps and 2 modules in this project:
### 1) Web scrapper:
a) In this module, a **SPIDER, react_beauty_spider.py (add link)** is written with the name *react_beauty_dev*. Scrappy is used to crawl through *react.dev* by limiting the domain to react.dev and the depth to 2. This is enough to crawl through all the pages on the website. 
b) Once the pages are crawled, **BeautifulSoup** is used to retrieve the html content on the pages. 
c) Each page content is written to a json file with id(auto increatement by 1), title(h1 tag), url(web url of the page) and content(all scrapped content) as the keys.
d) This module gave 156 json files(add link) as the output. And the files are uploaded to this repository for easy reference.
### 2) Search processor:
**a) Content processor(add link)**: In this step the content from the json files is read and processed. First each file is tokenized and punctuations and stop words are removed. For the scikit learn search, the tokenized documents are passed to *TfidfVectorizer* and the transformed index is dumped into a pickle file *tf-idf.pkl*. For the programmatic search, a *term_frequency_index* is created with term as the key and a pair of doc-id and the frequency of that term in that document is added to the value array. This index is used to calculate the tf-idf values for all terms and documents. When we get the query, the queries IDF value is also calculated. Then the cosine similarity of query and documents is calculated. This is done by doing the dot product of the query vector and inverted index. This product is normalised and cosine similarity is calculated. By sorting these calues in ddeceeasing order, we can get the matched documents. Out of which, the top 5 documents are sent in the json format as the output.\
**b) Query processor(add link)**: In this step, we use flask to write two POST APIs. The APIs take the query as input and outputs a json response of top 5 results. Both the APIs take the query and do **spelling correction**. They check each word in the the k-gram dictionary and if it is available the same word is used. If not, the edit distance is calculated and the nearest word is automatically used to search. One API searches using the scikit learn tf-idf scoring and the other seraches using the tf-idf scoring done programmatically.\
**c) API requests:** For easy testing, two request files are written. In this POST call is made with a default query. Changing the variable and running the python file would make the POST call.

## Operation
To run the project the following commands are needed:\
**a) Initial setup**\
A python environment needs to be created and activated\
```python3 -m venv se-env```\
```source se-env/bin/activate```\
**b) Install libraries**\
All the necessary libraries are installed \
```
pip install Scrapy
pip install beautifulsoup4
pip install jsonlib
pip install pathlib
pip install nltk
pip install scikit-learn
pip install flask
pip install requests
```
**c) Web crawling**
This will crawl through the react.dev website and the output files are avaialble under *web_scrapper(add link)* folder.
```
cd web_scrapper
scrapy crawl react_beauty_dev
```
**d) Processor:**\
We then process the downloaded page content\
```
cd ../search-processor
python3 processor.py 
```
**e) Run the flask server***\
```
export FLASK_APP=query
Flask run
```
**f) Run scikit-learn API**\
To see the serach results of scikit-learn based algorithm, we need to change the query in the *scikit-request.py* and run it.\
```
python3 scikit-request.py
```
We can see the json output in the terminal.\
**g) Run manual API**\
To see the serach results of programmatic algorithm, we need to change the query in the *manual-request.py* and run it.\
```
python3 manual-request.py
```
We can see the json output in the terminal.
## Conclusion
From the project, we can see that both the APIs are giving relevant documents as the output. But the ranking of the documents is needs improvement. We also observed that the pragrammatic implementation is giving more accurate results close to the reuslts of the search option available on the website. The scikit-learn API is also giving relevant documents for all the queries. But the accuracy is low for some queries. For some other queries, results are same for all three cases.
## Test Cases


