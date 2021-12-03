Removed each header row in each .csv file with the data
Used .import FILE TABLE commands to store values to tables

Commands used before running queries:
  .schema
  .read main.sql
  .mode csv
  .import CUSTOMER.csv CUSTOMER
  .import RATE.csv RATE
  .import RENTAL.csv RENTAL
  .import VEHICLE.csv VEHICLE
  .header on
  .mode column
  
