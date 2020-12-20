#Implement flask
from flask import Flask, request
import sqlite3
import pandas as pd
CovidVaccineApp = Flask(__name__)
@CovidVaccineApp.route('/')
def status():
    return "Yaaas! the server's running"
@app_532.route('/search', methods=['GET'])
def search_query():
    conn = sqlite3.connect('covid_vaccine.db')
    args = request.args.get("query").split(" ")
    "select state, sentiment, count(*) from covid_vaccine_result where sentiment is not null group by state, sentiment having state = " + args";"
    pd.read_sql('select * from covid_vaccine_result', conn)
    for word in args:
        try:
            query = "select state, sentiment, count(*) from covid_vaccine_result where sentiment is not null group by state, sentiment having state = " +word";"
            result = pd.read_sql(query, conn)
        except:
            if len(urls)<=0:
                urls.append('No results')
    
    return result.to_json(orient="records")