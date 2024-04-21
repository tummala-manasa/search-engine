import json
import string
import nltk
import math
import numbers
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

stopwords = nltk.corpus.stopwords.words('english')
inverted_index = {} # {'term': [1,2,3,4]}
term_frequency_index = {} # {'term': [[1,10], [3,4], [4,2], [1,1]}
documents = []

def tokenize_document(document):
    translator = str.maketrans('', '', string.punctuation)
    document = document.translate(translator).lower()
    tokens = []
    for token in document.split():
        if (token not in stopwords) and len(token) > 1:
            tokens.append(token)
    return tokens

def create_inverted_index(tokenized_documents, doc_index):
    # Iterate through each document
    for document_tokens in enumerate(tokenized_documents):
        # Iterate through each token in the document
        for token in document_tokens:
            if isinstance(token, numbers.Integral):
                continue
            # If the token is not already in the inverted index, add it
            if token not in inverted_index:
                inverted_index[token] = [doc_index]
                term_frequency_index[token] = [[doc_index, 1]]
            else:
                # If the token is already in the inverted index, append the document index
                if (inverted_index[token][-1] != doc_index):
                    inverted_index[token].append(doc_index)
                if (term_frequency_index[token][-1][0] != doc_index):
                    term_frequency_index[token].append([doc_index, 1])
                else:
                    term_frequency_index[token][-1] = [doc_index, term_frequency_index[token][-1][1]+1]

    # Sort the document indices in the inverted index
    for postings_list in inverted_index.values():
        postings_list.sort()

    return inverted_index

def create_inverted_index_tfidf(term_frequency_index, total_docs):
    # Calculate tf-idf scores
    inverted_index_tfidf = {} # {'term': [(2, 3.7903434994926393), (4, 3.7903434994926393), (3, 3.7903434994926393)]
    for (key, postings_list) in term_frequency_index.items():
        idf = math.log(total_docs / len(postings_list))
        pl = map(lambda x: (x[0], x[1]*idf), postings_list)
        inverted_index_tfidf[key] = list(pl)

    return inverted_index_tfidf

# Step 1: Read the JSON file and load its content
for x in range(1, 157):
    with open(f"../web_scrapper/react-{x}.json", 'r') as f:
        data = json.load(f)
        tokens = tokenize_document(data['content'])
        documents.append(" ".join(tokens))

        # Step 2: tokenize the content
        processed_data = {
            "id": data['id'],
            "url": data['url'],
            "title": data['title'],
            "content": tokens,
        }

        create_inverted_index(tokens, x)

#tf-idf-scikit
vectorizer = TfidfVectorizer(stop_words='english')
tfs_docs = vectorizer.fit_transform(documents)
with open('tf-idf.pkl', 'wb') as f:
    pickle.dump(tfs_docs, f)

#tf-idf manually done
def create_query_vector(query_terms, inverted_index):
  query_vector = {}
  N = 156 #len(documents)
  for term in query_terms:
    if term in inverted_index:
      # Compute IDF score for the term
      idf = math.log(N / len(inverted_index[term]))
      query_vector[term] = idf

  return query_vector

def search(query_vector, inverted_index):
    scores = {}
    document_lengths = {}

    # Calculate dot product between query vector and document vectors
    for term, idf_query in query_vector.items():
        if term in inverted_index:
            for doc_id, tf_idf_score in inverted_index[term]:
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += idf_query * tf_idf_score

    # Normalize document vectors and calculate cosine similarity
    for term, postings in inverted_index.items():
        for doc_id, tf_idf_score in postings:
            if doc_id not in document_lengths:
                document_lengths[doc_id] = 0
            document_lengths[doc_id] += tf_idf_score ** 2

    for doc_id, score in scores.items():
        scores[doc_id] /= math.sqrt(document_lengths[doc_id])

    # Sort results based on cosine similarity scores
    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_results

for term in term_frequency_index:
    term_frequency_index[term].sort(key=lambda x: x[1], reverse=True)
inverted_index_tfidf = create_inverted_index_tfidf(term_frequency_index, 156)