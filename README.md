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
### 1) Query: custom hooks
a) Search option on website:
<img width="1440" alt="Screenshot 2024-04-20 at 10 31 21 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/9615264c-94e2-4e91-ba50-50f2bcc03f92">

b) Scikit -learn search:
<img width="1440" alt="Screenshot 2024-04-20 at 10 32 29 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/2d1b3139-04ce-49c2-aa42-281be66c49d6">
Formatted output
<img width="1039" alt="Screenshot 2024-04-20 at 10 34 38 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/e587daaf-7e8f-48c4-8aac-df0de8a8cac2">

c) Programmatical tf-idf:
<img width="1440" alt="Screenshot 2024-04-20 at 10 37 11 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/006122bd-5a8f-4b7d-83fa-cfcbbf6c5234">
Formatted output:
<img width="1048" alt="Screenshot 2024-04-20 at 10 38 18 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/cd2f7a8f-1499-418f-9f42-35df57f910e4">

### 2) Query: component logic
a) Search option on website:
<img width="1428" alt="Screenshot 2024-04-20 at 10 39 20 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/fedd0a7d-0fb9-4770-99f4-32aa32b97206">

b) Scikit -learn search:
<img width="1440" alt="Screenshot 2024-04-20 at 10 40 18 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/bff0c79f-8fb3-4a56-a3be-c1a2fdbe5a68">
Formatted output
<img width="1057" alt="Screenshot 2024-04-20 at 10 40 46 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/fa68d7b4-76c0-44de-83d0-b972ed3ea444">

c) Programmatical tf-idf:
<img width="1437" alt="Screenshot 2024-04-20 at 10 41 19 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/5f43da5c-2d66-451e-b439-e710d0aec09d">
Formatted output:
<img width="1054" alt="Screenshot 2024-04-20 at 10 41 46 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/02f26481-c918-4f8c-87c3-2b9a49845f42">

### 3) Spelling correction - Query: componet lokic
a) Search option on website:
<img width="1428" alt="Screenshot 2024-04-20 at 10 46 35 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/67d9acf5-8fe1-4815-85d5-402587c7d131">

b) Scikit -learn search:
<img width="1440" alt="Screenshot 2024-04-20 at 10 49 29 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/ef8635f0-12ca-4811-81ad-50fa027e0fc6">
Formatted output
<img width="1054" alt="Screenshot 2024-04-20 at 10 50 03 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/bd2b1356-21ce-4543-8cb6-12cbb09a64ec">

c) Programmatical tf-idf:
<img width="1440" alt="Screenshot 2024-04-20 at 10 48 43 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/7d249fd3-5999-42bd-b211-378873a8ef99">
Formatted output:
<img width="1054" alt="Screenshot 2024-04-20 at 10 49 11 PM" src="https://github.com/tummala-manasa/search-engine/assets/51014362/9b22b82a-a94b-4eec-baa9-e496553d18dd">


