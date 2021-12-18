# Car Rental Database
Created a GUI using Python to access a database with information for a Car Rental Company 

## Tools Used
- Python
- SQLite3
- Tkinter (For GUI)


## Loading Data into Database
Removed each header row in each .csv file with the data

<br/>

Commands used before running queries:
```
  .schema
  .read main.sql
  .mode csv
  .import CUSTOMER.csv CUSTOMER
  .import RATE.csv RATE
  .import RENTAL.csv RENTAL
  .import VEHICLE.csv VEHICLE
  .header on
  .mode column
```