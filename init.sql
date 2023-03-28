CREATE DATABASE IF NOT EXISTS hotels;

USE hotels;

DROP TABLE IF EXISTS hotel_reviews;

CREATE TABLE hotel_reviews (
  id INT,
  name VARCHAR(255),
  hotel_class FLOAT,
  region VARCHAR(255),
  street_address VARCHAR(255),
  postal_code VARCHAR(10),
  locality VARCHAR(255),
  service FLOAT,
  cleanliness FLOAT,
  value FLOAT,
  review_text TEXT
); 

-- not using this anymore, see insert_data_from_json() in MySQLDatabaseHandler.py for inserting values into table
-- LOAD DATA INFILE 'relevant_reviews.json'
--     INTO TABLE hotel_reviews
--     LINES TERMINATED BY '\n'
--     (@json)
--     SET 
--         id = JSON_EXTRACT(@json, '$.id'),
--         hotel_class = JSON_EXTRACT(@json, '$.hotel_class'),
--         region = JSON_EXTRACT(@json, '$.region'),
--         street_address = JSON_EXTRACT(@json, '$."street-address"'),
--         postal_code = JSON_EXTRACT(@json, '$."postal-code"'),
--         locality = JSON_EXTRACT(@json, '$.locality'),
--         service = JSON_EXTRACT(@json, '$.service'),
--         cleanliness = JSON_EXTRACT(@json, '$.cleanliness'),
--         value = JSON_EXTRACT(@json, '$.value'),
--         review_text = JSON_EXTRACT(@json, '$.text');


