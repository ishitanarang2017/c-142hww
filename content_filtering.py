import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# creating df
df = pd.read_csv('articles.csv')

# notna function maps exisitng elements with true and non exisiting elements to false
# this operation removes rows mapped to false
df = df[df['title'].notna()]

# creating matix / vector
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df['title'])

# similarity object : classifier
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# resetting index of dataframe
df = df.reset_index()
indices = pd.Series(df.index, index = df['contentId'])

def get_recommendations(contentId):
   idx = indices[contentId]
   sim_scores = list(enumerate(cosine_sim2[idx]))
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   sim_scores = sim_scores[1:11]
   movie_indices = [i[0] for i in sim_scores]

   return df[["url", "title", "text", "lang", "total_events"]].iloc[movie_indices]