import googlemaps
from pprint import pprint
from config import creds
import requests
from datetime import datetime
from datetime import date


def geo_information(gmaps, city, state):
    ''' return long, lat and county '''
    
    try:
        geocode_response = gmaps.geocode(address = city + ',' + state)[0]
    except:
        
        #TODO: write a descriptive error message 

        pass
    
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
    num_cases = -1
    num_deaths = -1
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

    # photos = place_info['candidates'][0]['photos'][0]['photo_reference']
    # print(gmaps.places_photo(photo_reference = photos, max_width=200, max_height = 200))
    # print(photos)


    return place_info['candidates'][0]


def extract_reviews(place_id):
    wextractor_api_key = creds.get_wextractor_key()
    offset = 0 
    date_format = '%Y-%m-%d'
    RECENCY_TRESHOLD = 50

    reviews_url = f'https://wextractor.com/api/v1/reviews?id={place_id}&auth_token={wextractor_api_key}&offset={offset}'

    current_date = date.today()
    within_last_month = True

    recent_reviews = []

    while(within_last_month):
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


def run_procedure(place, city, state):
    API_KEY = creds.get_google_key()
    gmaps = googlemaps.Client(key=API_KEY)
    county, lat, lng = geo_information(gmaps, city, state).values()
    num_cases, num_deaths = covid_stats(county,state).values()
    place_metadata = place_search(gmaps, place, lat, lng)
    place_id = place_metadata['place_id']

    reviews = extract_reviews(place_id)
    return reviews


if __name__ == "__main__":
    place = 'Firo Pizza'
    city = 'Mckinney'
    state = 'Texas'


    API_KEY = creds.get_google_key()
    gmaps = googlemaps.Client(key=API_KEY)
    county, lat, lng = geo_information(gmaps, city, state).values()
    num_cases, num_deaths = covid_stats(county,state).values()
    place_metadata = place_search(gmaps, place, lat, lng)
    place_id = place_metadata['place_id']

    extract_reviews(place_id)

    print(f'County: {county}')
    print(f'number cases: {num_cases} ')
    print(f'number deaths: {num_deaths}')

