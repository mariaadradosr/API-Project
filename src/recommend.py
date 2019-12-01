import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np

def getUserRecommendation(user_id, coll, users_coll):

    col = {}
    for e in list(users_coll.find({})):
        col[str(e['_id'])]=e['name']
        
    col_re = {v: k for k, v in col.items()}
    
    docs = {}
    for e in list(coll.find({})):
        docs[e['author_id']]=''

    for e in list(coll.find({})):
        for i in docs.keys():
            if i == e['author_id']:
                docs[i]+=' '+(e['markdown'].encode('latin-1').decode('utf-8'))
    
    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    
    doc_term_matrix = sparse_matrix.todense()
    
    # Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    df = pd.DataFrame(doc_term_matrix, 
                      columns=count_vectorizer.get_feature_names(), 
                      index=docs.keys())

    df.index = df.index.to_series().apply(lambda x: col[x])
    
    # Compute Cosine Similarity matrix (or selected distance)
    similarity_matrix = distance(df, df)
    
    sim_df = pd.DataFrame(similarity_matrix, columns=df.index, index=df.index)
    
    # Max similarities of related documents
    
    np.fill_diagonal(sim_df.values, 0) # Remove diagonal max values and set those to 0
    out = sim_df.idxmax()
    name = col[user_id]
    result = out[name]
    friend_id = col_re[result]
    return f'{name} ({user_id}) friend recommedation -----> {result} ({friend_id})'
