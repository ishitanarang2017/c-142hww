from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd


articles_data = pd.read_csv('articles.csv')

app = Flask(__name__)

# extracting important information from dataframe
all_articles = articles_data[["url" , "title", "text" , "lang" , "total_events"]]

# variables to store data
likedarticles = []
dislikedarticles= []


# method to fetch data from database
def assignval():
  mdata = {
      "url": all_articles.iloc[0,0],
      "title":  all_articles.iloc[0,1],
      "text" : all_articles.iloc[0,2] or "n/a",
      "lang" :  all_articles.iloc[0,3],
      "total_events" :  all_articles.iloc[0,4]/2
  }
  return mdata 


# /articles api
@app.route("/articles")
def getarticles():
  articledata = assignval()
  return jsonify({
      "data":articledata,
      "status": "success"
  })

# /like api
@app.route("/like",methods = ["POST"])
def likedarticle():
  global all_articles
  articledata = assignval()
  likedarticles.append(articledata)
  all_articles.drop([0],inplace = True)
  all_articles = all_articles.reset_index(drop = True)
  return jsonify({
      "status":"success"
  })

# /dislike api
@app.route("/dislike",methods = ["POST"])
def dislikedarticle():
  global all_articles
  articledata = assignval()
  dislikedarticles.append(articledata)
  all_articles.drop([0],inplace = True)
  all_articles = all_articles.reset_index(drop = True)
  return jsonify({
      "status":"success"
  })
# api to return list of popular articles
@app.route("/popular_articles")
def popular_articles():
    popularmd = []
    for i,r in output.iterrows():
        _p = {
            "url": r["url"],
            "title": r["title"],
            "text": r["text"]or "na",
            "lang": r["lang"],
            "total_events": r["total_events"]/2
        }
        popularmd.append(_p)
    return jsonify({
        "data": popularmd,
        "status": "success"
    })
                                      



# api to return list of recommended articles
@app.route("/rec_articles")
def rec_articles():
    global liked_articles
    columnnames = ["url", "title", "text", "lang", "total_events"]
    all_rec = pd.DataFrame(columns=columnnames)
    for l in liked_articles:
        output = get_recommendations(l["url"])
        all_rec=all_rec.append(output)
    all_rec.drop_duplicates(subset=["url"],inplace = True)
    recmd = []
    for i,r in all_rec.iterrows():
        _p = {
            "url": r["url"],
            "title": r["title"],
            "text": r["text"] or "na",
            "lang": r["lang"],
            "total_events": r["total_events"]/2
        }
        recmd.append(_p)
    return jsonify({
        "data": recmd,
        "status": "success"
    })


if __name__ == "__main__":
  app.run()