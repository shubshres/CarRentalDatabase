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

To run the graphical user interface for the Car Rental Database, run gui.py and ensure Python code can be ran on your machine and the code is being ran in the same directory as the CarRental2019.db

You can run the gui.py by opening it up in the IDLE for Python and selecting Run > Run Module.
