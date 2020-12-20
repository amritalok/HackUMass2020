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
    last_updated DATE)
    FOREIGN KEY (county_name, state) REFERENCES COUNTIES (county_name, state)
  """)
  conn.commit()

def create_reviews_table(cursor, conn):
  cursor.execute(""" CREATE TABLE IF NOT EXISTS REVIEWS (
      rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def insert_place(conn, cursor, place_id, address, name, latitude, longitude, county_name, state):
  cursor.execute(f"INSERT INTO PLACES VALUES (:place_id, :address, :name, :latitude, :longitude, :last_updated, :county_name, state)", {
    'place_id': place_id,
    'address': address,
    'name': name,
    'latitude': latitude, 
    'longitude': longitude, 
    'last_updated': date.today(),
    'county_name': county_name,
    'state': state
  })
  conn.commit()

def insert_county(conn, cursor, county_name, state, ):
  pass

def insert_reviews():
  pass

if __name__ == "__main__":
  conn, cursor = connect_database('../db/locations.db')
  create_places_table(cursor, conn)
  create_reviews_table(cursor, conn)
  create_counties_table(cursor, conn)
  conn.close()