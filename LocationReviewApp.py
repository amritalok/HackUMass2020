#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Implement flask
import json
from flask import Flask, request
from flask_cors import CORS
import sqlite3
import pandas as pd
from location_data.test import run_procedure
from src.vaccine_data.reviewAnalysis import ReviewAnalysis
CovidVaccineApp = Flask(__name__)
cors = CORS(CovidVaccineApp, resources={r"/api/*": {"origins": "*"}})
# CovidVaccineApp.debug = True
@CovidVaccineApp.route('/')
def status():
    return "Yaaas! the server's running"
@CovidVaccineApp.route('/api/search', methods=['GET'])
def search_query():
    state = request.args.get("state")
    try:
        conn = sqlite3.connect('db/covid_vaccine.db')
        query = "select sentiment, count(*) as count from covid_vaccine_result where sentiment is not null group by state, sentiment having state ='" +state+ "';"
        result = pd.read_sql(query, conn)
#         print(result)
        output = dict(zip(result['sentiment'], result['count']))
#         print(output)
    except:
        return "Failed!"
    return json.dumps(output, indent = 4) 
@CovidVaccineApp.route('/api/summarize', methods=['GET'])
def summearize_text():
    place = request.args.get("place")
    state = request.args.get("state")
    city = request.args.get("city")
#     print(place, city, state)
    location_data = run_procedure(place, city, state)
    reviews = location_data['reviews']
    ra = ReviewAnalysis()
    ra.getReviews(reviews)
    sentiment = ra.OutputSentimentScore()
    if(sentiment<50):
        polarity = 'NEGATIVE'
    else:
        polarity = 'POSITIVE'
    input_text = '.'.join(reviews)
    summaries = ra.outputSummaries(input_text)
    return {'summaries': summaries, 'polarity': polarity}
if __name__ == '__main__':
    CovidVaccineApp.run()


# In[ ]:




