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

## How to Run GUI
To run the graphical user interface for the Car Rental Database, type in:

```
python3 gui.py
```

into the terminal and ensure 
- Python and Tkinter are installed on your machine
- the code is being ran in the same directory as the CarRental2019.db

## Task 1: Execute Queries on the CarRental2019 Database Tables

### Query 1:

```
--Add an extra column ‘Returned’ to the RENTAL table. Values will be 0-for non-returned cars, and 1-for returned. Then update the ‘Returned’ column with '1' for all records that they have a payment date and with '0' for those that they do not have a payment date.

ALTER TABLE RENTAL ADD COLUMN Returned INTEGER DEFAULT 0;
UPDATE RENTAL
SET Returned = 1
WHERE PaymentDate <> 'NULL';

```

Output:

![](screenshots/task1.png)

