import googlemaps
from pprint import pprint
from location_data.config import creds
import requests
from datetime import datetime
from datetime import date
import sqlite3
import os
# from database import insert_place, insert_county, insert_review, connect_database


# class PlaceData:
#     def __init__(self, place, city, state):
#         self.place = place
#         self.city = city
#         self.state = state

#         self.lat = None
#         self.lng = None
#         self.county = None
#         self.state = None
#         self.covid_cases = None
#         self.covid_deaths = None
#         self.reviews = None

#         self.conn = None
#         self.cursor = None
    
#     def connect_database():
#         pass

#     def insert_database(self):
#         insert_place()
#         insert_county()
#         insert_reviews()

#     def insert_place(self):
#         pass

#     def insert_county(self):
#         pass

#     def insert_reviews():
#         pass




def geo_information(gmaps, city, state):
    ''' return long, lat and county '''
    
    try:
        geocode_response = gmaps.geocode(address = city + ',' + state)[0]
    except:
        return 
    
    #you can loop through here to be more safe for area_level_2 
    address_components = geocode_response['address_components']
    county = address_components[1]['long_name']
    county = county.replace('County', '')
    
    
    location = geocode_response['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    

    return {'county': county, 'lat': lat, 'lng':lng}


def covid_stats(county, state):
    county = county.strip()
    state = state.strip()
    
    #default values 
    num_cases = None
    num_deaths = None

    query_string = f'https://covidti.com/api/public/us/timeseries/{state}/{county}'
    response = requests.get(query_string)

    if response.status_code == 200:
        #perform some action

        payload = response.json()['response'][0]
        try:
            timeseries_data = payload['data'][0]['timeseries']
            dates = list(timeseries_data.keys())
            recent_date = max(dates, key = lambda d: datetime.strptime(d,'%m/%d/%y'))
            num_cases = timeseries_data[recent_date]['cases']
            num_deaths = timeseries_data[recent_date]['deaths']
        except KeyError:
            #TODO: throw error or do something
            pass
    
    return {'cases': num_cases, 'deaths': num_deaths}

def place_search(gmaps,search_query, lat, lng):
    ''' 
    returns formatted_address, name, place_id
    '''
    place_info = gmaps.find_place(
        input = search_query,
        input_type = 'textquery',
        fields = ['place_id', 'formatted_address', 'name', 'icon'],
        location_bias = f'circle:5@{lat},{lng}',
        language='en'
    )

    try:
        return place_info['candidates'][0]
    except IndexError:
        return None

def extract_google_reviews(place_id):
    wextractor_api_key = creds.get_wextractor_key()
    offset = 0
    date_format = '%Y-%m-%d'
    RECENCY_TRESHOLD = 40


    current_date = date.today()
    within_last_month = True

    recent_reviews = []

    while(within_last_month):
        reviews_url = f'https://wextractor.com/api/v1/reviews?id={place_id}&auth_token={wextractor_api_key}&offset={offset}'
        response = requests.get(reviews_url)
        reviews = response.json()['reviews']

        if(len(reviews) > 0):
            for review in reviews:
                review_date = review['datetime'].split('T')[0]
                review_date = datetime.strptime(review_date, date_format).date()
                delta = (current_date - review_date).days

                if(delta < RECENCY_TRESHOLD):
                    if(review['text']):
                        recent_reviews.append(review['text'])
                else:
                    within_last_month = False
                    break
            
        offset+=10
    return recent_reviews

def extract_yelp_reviews(name, address, lat, lng):
    search_url='https://api.yelp.com/v3/businesses/search'
    yelp_api_key = creds.get_yelp_key()

    headers = {'Authorization': 'Bearer %s' % yelp_api_key}
    params = {'term': name,'location': address, 'latitude': lat, 'longitude': lng, 'limit': 1}

    response = requests.get(search_url, params=params, headers=headers)
    if(response.status_code == 200):
        try:
            business_data = response.json()['businesses'][0]
            if(business_data['name'] == name):
                url = business_data['url']
        except IndexError:
            return None
    
    # plain url without any query parameters (passed into wextractor)
    base_url = url.split('?')[0]
    id = base_url.split('/')[-1]

    offset = 0
    wextractor_api_key = creds.get_wextractor_key()

    # returns 20 reviews (default)
    # TODO: get within the last month (if time)
    wextractor_url = f'https://wextractor.com/api/v1/reviews/yelp?id={id}&auth_token={wextractor_api_key}&offset={offset}'

    response = requests.get(wextractor_url)
    reviews = response.json()['reviews']
    yelp_reviews = []

    if(len(reviews) > 0):
        for review in reviews[:10]:
            if(review['text']):
                yelp_reviews.append(review['text'])
    else:
        return None

    return yelp_reviews

def run_procedure(place, city, state):
    API_KEY = creds.get_google_key()
    gmaps = googlemaps.Client(key=API_KEY)
    county, lat, lng = geo_information(gmaps, city, state).values()
    num_cases, num_deaths = covid_stats(county,state).values()

    place_metadata = place_search(gmaps, place, lat, lng)
    
    if(place_metadata is not None):
        place_id = place_metadata['place_id']
        google_reviews = extract_google_reviews(place_id)

    yelp_reviews = extract_yelp_reviews(place_metadata['name'], place_metadata['formatted_address'], lat, lng)

    reviews =  google_reviews + yelp_reviews

    # conn, cursor = connect_database('locations.db')
    # cursor.execute(""" SELECT county_name, state FROM 
    #     COUNTIES WHERE county_name=:county_name AND state=:state""",
    #     {
    #         'county_name': county,
    #         'state': state
    #     })
    # if(len(cursor.fetchall()) == 0):
    #     insert_county(conn, cursor, county, state, num_cases, num_deaths)

    # insert_place(conn, cursor,place_metadata['place_id'], place_metadata['formatted_address'], place_metadata['name'], lat, lng, county, city, state)

    return {'num_cases': num_cases, 'num_deaths': num_deaths, 'reviews': reviews}



if __name__ == "__main__":
    place = 'Hugs Cafe'
    city = 'Mckinney'
    state = 'Texas'

   
    data = run_procedure(place, city, state)
    # reviews = data['reviews']

    # for review in reviews:
    #     print(review)

    # print(f'County: {county}')
    # print(f'number cases: {num_cases} ')
    # print(f'number deaths: {num_deaths}')

