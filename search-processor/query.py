import os
import pickle
import json
from processor import vectorizer, inverted_index_tfidf, create_query_vector, search, tokenize_document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.metrics.distance import edit_distance
from flask import Flask, jsonify, request, abort

with open('tf-idf.pkl', 'rb') as f:
    docs_vector = pickle.load(f)

def generate_kgrams(word, k):
    # Initialize an empty list to store the k-grams
    kgrams = []
    # Appending $ at start and end to get boundaries of term
    word = '$'+word+'$'
    # Iterate over the characters in the word
    for i in range(len(word) - k + 1):
        # Create a k-gram by taking k consecutive characters
        kgram = word[i:i+k]
        # Append the k-gram to the list
        kgrams.append(kgram)
    return kgrams

def create_k_gram_dict(terms):
  kGramDict = {}
  for term in terms:
    twoGrams = generate_kgrams(term, 2)
    for gram in twoGrams:
      if gram not in kGramDict:
        kGramDict[gram] = [term]
      else:
        kGramDict[gram].append(term)
  return kGramDict

allTermDict = create_k_gram_dict(list(inverted_index_tfidf.keys()))

def min_distance_search(query):
  terms = list(inverted_index_tfidf.keys())
  # Correct query
  if query in terms:
    return query
  
  # mispelled
  twoGrams = generate_kgrams(query, 2)
  terms = []
  for gram in twoGrams:
     if not terms:
      terms = allTermDict[gram]
     else:
      x = allTermDict[gram]
      terms = list(set(terms + x))
  minDist = float('inf')
  ans = ''
  for term in terms:
    distance = edit_distance(query, term)
    # distorted
    if distance < minDist:
      minDist = distance
      ans = term
  return ans


# Flask application
app = Flask(__name__)

@app.route('/search-scikit', methods=['POST'])
def handle_scikit_search():
    # Extract data from the request
    data = request.json
    query = data['query']
    if not query:
        abort(400, 'Query is required')

    spellChecked_query = ""
    for term in tokenize_document(query):
        spellChecked_query += " " + min_distance_search(term)

    query_vector = vectorizer.transform([spellChecked_query])
    cosine_similarities = cosine_similarity(query_vector, docs_vector).flatten()
    k = min(5, len(cosine_similarities))
    top_k_indices = cosine_similarities.argsort()[-k:][::-1]
    output = []
    for i in top_k_indices:
        with open(f"../web_scrapper/react-{i+1}.json", 'r') as f:
            data = json.load(f)
            obj = {
                'title': data['title'],
                'url': data['url'],
                'cosine_similarity': cosine_similarities[i]
            }
            output.append(obj)

    # Return a response
    return jsonify(output), 200

@app.route('/search-manual', methods=['POST'])
def handle_manual_search():
    # Extract data from the request
    data = request.json
    query = data['query']
    if not query:
        abort(400, 'Query is required')

    spellChecked_list = []
    for term in tokenize_document(query):
        spellChecked_list.append(min_distance_search(term))

    output = []
    query_vector = create_query_vector(spellChecked_list, inverted_index_tfidf)
    results = search(query_vector, inverted_index_tfidf)
    for doc_id, score in results[:5]:
        with open(f"../web_scrapper/react-{doc_id}.json", 'r') as f:
            data = json.load(f)
            obj = {
                "title": data['title'],
                "url": data['url'],
                "cosine_similarity": score
            }
            output.append(obj)
    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True)

