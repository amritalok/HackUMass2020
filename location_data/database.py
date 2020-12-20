import sqlite3
from datetime import date

def connect_database(database_name):
  conn = sqlite3.connect(database_name)
  conn.execute("PRAGMA foreign_keys = 1")
  c = conn.cursor()
  return (conn, c)

def create_places_table(cursor, conn):
  cursor.execute(""" CREATE TABLE IF NOT EXISTS PLACES (
    place_id TEXT PRIMARY KEY, 
    address TEXT, 
    name TEXT,
    latitude REAL,
    longitude REAL,
    last_updated DATE,
    county_name TEXT,
    state TEXT,
    city TEXT, 
    FOREIGN KEY (county_name, state) REFERENCES COUNTIES (county_name, state))
  """)
  conn.commit()

def create_reviews_table(cursor, conn):
  cursor.execute(""" CREATE TABLE IF NOT EXISTS REVIEWS (
      place_id TEXT,
      review_text TEXT,
      FOREIGN KEY (place_id) REFERENCES PLACES (place_id))
      """)
  conn.commit()

def create_counties_table(cursor, conn):
  cursor.execute(""" CREATE TABLE IF NOT EXISTS COUNTIES (
        county_name TEXT,
        state TEXT,
        covid_cases INTEGER,
        covid_deaths INTEGER, 
        last_updated DATE, 
        PRIMARY KEY (county_name, state))
        """)
  conn.commit()

def insert_place(conn, cursor, place_id, address, name, latitude, longitude, county_name, city, state):
  cursor.execute(f"INSERT INTO PLACES VALUES (:place_id, :address, :name, :latitude, :longitude, :last_updated, :county_name, :city, :state)", {
    'place_id': place_id,
    'address': address,
    'name': name,
    'latitude': latitude, 
    'longitude': longitude, 
    'last_updated': date.today(),
    'county_name': county_name,
    'city': city,
    'state': state
  })
  conn.commit()

def insert_county(conn, cursor, county_name, state, num_cases, num_deaths):
  cursor.execute(f"INSERT INTO COUNTIES VALUES (:county_name, :state, :covid_cases, :covid_deaths, :last_updated)",{
    'county_name': county_name,
    'state': state,
    'covid_cases': num_cases,
    'covid_deaths': num_deaths,
    'last_updated': date.today()
  })
  conn.commit()


def insert_review(conn, cursor, place_id, review_text):
  cursor.execute(f"INSERT INTO REVIEWS VALUES (:place_id, :review_text)",{
    'place_id': place_id,
    'review_text': review_text
  })
  conn.commit()

if __name__ == "__main__":
  conn, cursor = connect_database('locations.db')
  cursor.execute("SELECT * FROM COUNTIES")
  print(cursor.fetchall())
  cursor.execute("SELECT * FROM PLACES")

  # print(cursor.fetchall())
  # create_places_table(cursor, conn)
  # create_reviews_table(cursor, conn)
  # create_counties_table(cursor, conn)
  conn.close()