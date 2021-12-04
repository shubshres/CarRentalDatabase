#Mohammed Ahmed
#Hoang Ho
#Shubhayu Shrestha
#CSE 3330-004 Project 2 Part 3
#November 29, 2021

# create tkinter window
from tkinter import *
import sqlite3
import os

# window for handling returning a rental
def return_rental_win():
  #Toplevel object treated as new window
  window = Toplevel(root)
  window.title("Return Rental")
  window.geometry("400x200")
  
  #frames to contain query input and output separately
  query_frame = Frame(window)
  output_frame = Frame(window)

  #labels and textboxes for queries
  cust_name_label = Label(query_frame, text='Customer Name: ')
  cust_name_tb = Entry(query_frame, width=30)
  cust_name_label.grid(row=0, column=0)
  cust_name_tb.grid(row=0, column=1)

  return_date_label = Label(query_frame, text='Return Date:')
  return_date_label.grid(row=1, column=0)
  return_date_tb = Entry(query_frame, width=30)
  return_date_tb.grid(row=1, column=1)
  
  VIN_label = Label(query_frame, text='VIN: ')
  VIN_tb = Entry(query_frame, width=30)
  VIN_label.grid(row=2, column=0)
  VIN_tb.grid(row=2, column=1)

  #confirmation/submit query button
  submit_btn = Button(query_frame, text='Submit', command=lambda: return_rental(output_frame, return_date_tb.get(), cust_name_tb.get(), VIN_tb.get()))
  submit_btn.grid(row=7, column=1, sticky=E)

  #attach frames to window and text to output frame
  query_frame.grid(row=0, column=0)
  output_frame.grid(row=1, column=0)

# retrieves a rental by return date, customer name, vehicle vehicle_info
# handles transaction to return a vehicle by printing total customer payment due for the rental, enter it in the database, and update returned attribute accordingly
# frame - frame to place outputs in
# return_date - when the rental needs to be returned
# cust_name - customer name for the rental information
# vehicle_info - vehicle id/vin that is rented
def return_rental(frame, return_date, cust_name, vehicle_info):
  #ensure connection to database
  db_conn = sqlite3.connect(os.getcwd() + '/CarRental2019.db')
  db_cur = db_conn.cursor()
  
  #retrieves the customer id, the amount due for the rental given the rental information
  query = "SELECT R.CustID, R.TotalAmount FROM RENTAL AS R JOIN CUSTOMER AS C ON R.CustID = C.CustID WHERE R.ReturnDate = '" + return_date + "' AND C.CustName = '" + cust_name + "' AND R.VehicleID = '" + vehicle_info + "'"

  print(query)

  db_cur.execute(query)

  #stores result of inner_query
  result = db_cur.fetchall()

  print(result)

  #displays total customer payment due
  output_label = Label(frame, text='Total Customer Payment Due: $' + str(result[0][1]))
  output_label.grid(row=0, column=0, columnspan=2, sticky=W)

  #updates the returned attribute in rental table for the rental being returned
  #updates the payment date if it is NULL also
  db_cur.execute("UPDATE RENTAL SET Returned = 1, PaymentDate = CASE WHEN PaymentDate = 'NULL' THEN '" + return_date + "' END WHERE CustID = " + str(result[0][0]) + " AND ReturnDate = '" + return_date + "' AND VehicleID = '" + vehicle_info + "'")
  
  db_conn.commit()
  db_conn.close()

# for inserting adding info about a new customer
# frame - frame to place outputs in
# cust_name - name of the customer being added to the database
# phone - phone number of the customer being added to the database
def add_new_cust(frame, cust_name, phone):
  new_cust_conn = sqlite3.connect(
      os.getcwd() + '/CarRental2019.db')  # ensure connection
  new_cust_cur = new_cust_conn.cursor()
  new_cust_cur.execute(
      "INSERT INTO CUSTOMER VALUES(NULL, ?, ?)", (cust_name, phone))
  #using parameterized queries here

  new_cust_cur.execute("SELECT CustID FROM CUSTOMER WHERE CustName = ? AND Phone = ?", (cust_name, phone))
  #displays total customer payment due
  result = new_cust_cur.fetchall()
  output_label = Label(frame, text='Added new customer: ' + str(result[0][0]) + ', ' + cust_name + ', ' + phone + ' (1 new row)')
  output_label.grid(row=0, column=0, columnspan=2, sticky=W)

  #commit changes - so any changes seen by other connections of db
  new_cust_conn.commit()
  #close connection
  new_cust_conn.close()

# window for inserting info about a new customer
def new_cust_win():
  #Toplevel object treated as new window
  window = Toplevel(root)
  window.title("Add New Customer")
  window.geometry("400x200")

  #frames to contain query input and output separately
  query_frame = Frame(window)
  output_frame = Frame(window)

  #labels and text boxes
  cust_name_label = Label(query_frame, text='Customer Name: ')
  cust_name_tb = Entry(query_frame, width=30)
  cust_name_label.grid(row=0, column=0)
  cust_name_tb.grid(row=0, column=1)

  phone_label = Label(query_frame, text='Phone Number: ')
  phone_tb = Entry(query_frame, width=30)
  phone_label.grid(row=1, column=0)
  phone_tb.grid(row=1, column=1)

  add_cust_btn = Button(query_frame, text='Add Customer', command=lambda: add_new_cust(output_frame, cust_name_tb.get(
  ), phone_tb.get()))  # using lambda to execute function utilizing the textbox entries
  #get() grabs whatevers in that text box on the gui components
  add_cust_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

  #attach frames to window and text to output frame
  query_frame.grid(row=0, column=0)
  output_frame.grid(row=1, column=0)

# define the input query structure
# creating a function called add_new_vehicle using this function
# to insert values into the database
def add_new_vehicle(VIN, vehicle_description, vehicle_year, vehicle_type, vehicle_category):
  # connecting to the database
  new_vehicle_connect = sqlite3.connect('CarRental2019.db')  # ensure connection

  # linking to the db
  new_vehicle_cursor = new_vehicle_connect.cursor()

  new_vehicle_cursor.execute("INSERT INTO VEHICLE VALUES(?, ?, ?, ?, ?)", (
      VIN, vehicle_description, vehicle_year, vehicle_type, vehicle_category))

  # commit changes
  new_vehicle_connect.commit()
  # close connection
  new_vehicle_connect.close()

# input for new vehicle
def new_vehicle_win():
  # creating a new tkinter window for window vehicle
  windowVehicle = Toplevel(root)

  # giving the vehicle window a title
  windowVehicle.title("Add New Vehicle")

  # setting the dimensions for the vehicle window
  windowVehicle.geometry("400x200")

  #labels and text boxes
  # entering the component of the text box
  VIN = Entry(windowVehicle, width=30)
  # placing the entry in a position
  VIN.grid(row=0, column=1)
  # creating a label for the entry box
  VIN_label = Label(windowVehicle, text='VIN: ')
  # placing the label
  VIN_label.grid(row=0, column=0)

  # entering the component of the text box
  vehicle_description = Entry(windowVehicle, width=30)
  # placing the entry in a position
  vehicle_description.grid(row=1, column=1)
  # creating a label for the entry box
  vehicle_description_label = Label(windowVehicle, text='Description: ')
  # placing the label
  vehicle_description_label.grid(row=1, column=0)

  # entering the component of the text box
  vehicle_year = Entry(windowVehicle, width=30)
  # placing the entry in a position
  vehicle_year.grid(row=2, column=1)
  # creating a label for the entry box
  vehicle_year_label = Label(windowVehicle, text='Year: ')
  # placing the label
  vehicle_year_label.grid(row=2, column=0)

  # entering the component of the text box
  vehicle_type = Entry(windowVehicle, width=30)
  # placing the entry in a position
  vehicle_type.grid(row=3, column=1)
  # creating a label for the entry box
  vehicle_type_label = Label(windowVehicle, text='Type: ')
  # placing the label
  vehicle_type_label.grid(row=3, column=0)

  # entering the component of the text box
  vehicle_category = Entry(windowVehicle, width=30)
  # placing the entry in a position
  vehicle_category.grid(row=4, column=1)
  # creating a label for the entry box
  vehicle_category_label = Label(windowVehicle, text='Category: ')
  # placing the label
  vehicle_category_label.grid(row=4, column=0)

  # Creating Buttons
  # Where the text box connects with the submit function
  add_vehicle_button = Button(windowVehicle, text='Add Vehicle', command=lambda: add_new_vehicle(
      VIN.get(), vehicle_description.get(), vehicle_year.get(), vehicle_type.get(), vehicle_category.get()))
  add_vehicle_button.grid(row=7, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=100)

# creating a function called add_new_reservation using this function
# to insert values into the database
def add_new_reservation(CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, ReturnStatus):
  # connecting to the sqlite database
  rental_reservation_connect = sqlite3.connect('CarRental2019.db')

  # cursor to access to connection
  rental_reservation_cur = rental_reservation_connect.cursor()

  # execute
  rental_reservation_cur.execute(
      "INSERT INTO RENTAL VALUES(?,?,?,?,?,?,?,?,?,?)", (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, ReturnStatus))

  # commit changes
  rental_reservation_connect.commit()

  # close connection
  rental_reservation_connect.close()

# input for new rental

def new_rental_win():
  # creating new window for rental
  rentalWindow = Toplevel(root)

  # set the window title
  rentalWindow.title("Add New Rental")

  # set the dimensions
  rentalWindow.geometry("500x300")

  # CustID
  # Making the Text Boxes and labels
  # entering the component in the text box
  CustID = Entry(rentalWindow, width=30)
  # place the box
  CustID.grid(row=0, column=1)
  # creating the label for the entry box
  CustID_label = Label(rentalWindow, text='CustID: ')
  # placing the label
  CustID_label.grid(row=0, column=0)

  # VehicleID
  # Making the Text Boxes and labels
  # entering the component in the text box
  VehicleID = Entry(rentalWindow, width=30)
  # place the box
  VehicleID.grid(row=1, column=1)
  # creating the label for the entry box
  VehicleID_label = Label(rentalWindow, text='VIN: ')
  # placing the label
  VehicleID_label.grid(row=1, column=0)

  # StartDate
  # Making the Text Boxes and labels
  # entering the component in the text box
  StartDate = Entry(rentalWindow, width=30)
  # place the box
  StartDate.grid(row=2, column=1)
  # creating the label for the entry box
  StartDate_label = Label(rentalWindow, text='Start Date (MM-DD-YYYY): ')
  # placing the label
  StartDate_label.grid(row=2, column=0)

  # OrderDate
  # Making the Text Boxes and labels
  # entering the component in the text box
  OrderDate = Entry(rentalWindow, width=30)
  # place the box
  OrderDate.grid(row=3, column=1)
  # creating the label for the entry box
  OrderDate_label = Label(rentalWindow, text='Order Date (MM-DD-YYYY): ')
  # placing the label
  OrderDate_label.grid(row=3, column=0)

  # RentalType
  # Making the Text Boxes and labels
  # entering the component in the text box
  RentalType = Entry(rentalWindow, width=30)
  # place the box
  RentalType.grid(row=4, column=1)
  # creating the label for the entry box
  RentalType_label = Label(rentalWindow, text='Rental Type: ')
  # placing the label
  RentalType_label.grid(row=4, column=0)

  # Qty
  # Making the Text Boxes and labels
  # entering the component in the text box
  Qty = Entry(rentalWindow, width=30)
  # place the box
  Qty.grid(row=5, column=1)
  # creating the label for the entry box
  Qty_label = Label(rentalWindow, text='Quantity: ')
  # placing the label
  Qty_label.grid(row=5, column=0)

  # ReturnDate
  # Making the Text Boxes and labels
  # entering the component in the text box
  ReturnDate = Entry(rentalWindow, width=30)
  # place the box
  ReturnDate.grid(row=6, column=1)
  # creating the label for the entry box
  ReturnDate_label = Label(rentalWindow, text='Return Date (MM-DD-YYYY): ')
  # placing the label
  ReturnDate_label.grid(row=6, column=0)

  # TotalAmount
  # Making the Text Boxes and labels
  # entering the component in the text box
  TotalAmount = Entry(rentalWindow, width=30)
  # place the box
  TotalAmount.grid(row=7, column=1)
  # creating the label for the entry box
  TotalAmount_label = Label(rentalWindow, text='Total Amount: ')
  # placing the label
  TotalAmount_label.grid(row=7, column=0)

  # PaymentDate
  # Making the Text Boxes and labels
  # entering the component in the text box
  PaymentDate = Entry(rentalWindow, width=30)
  # place the box
  PaymentDate.grid(row=8, column=1)
  # creating the label for the entry box
  PaymentDate_label = Label(rentalWindow, text='Payment Date: (MM-DD-YYYY)')
  # placing the label
  PaymentDate_label.grid(row=8, column=0)

  # Creating Buttons
  # Where the text box connects with the submit function
  add_reservation_button = Button(rentalWindow, text='Add Reservation', command=lambda: add_new_reservation(
      CustID.get(), VehicleID.get(), StartDate.get(), OrderDate.get(), RentalType.get(), Qty.get(), ReturnDate.get(), TotalAmount.get(), PaymentDate.get(), 0))
  add_reservation_button.grid(row=9, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=100)



# Q5A
# Retrieving Customer information
def retrieve_cust_info(retrieve_custWindow, CustID, CustName):

  # connecting to the sqlite database
  retrieve_cust_connect = sqlite3.connect('CarRental2019.db')

  # cursor to access to connection
  retrieve_cust_cursor = retrieve_cust_connect.cursor()
  
  
  # New Version
  if CustID != '':
    retrieve_cust_cursor.execute(
        "SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo WHERE CustomerID LIKE ? AND CustomerName LIKE ? GROUP BY CustomerID ORDER BY COUNT(RentalBalance) DESC", (('%'+CustID+'%'), ('%'+CustName+'%'),))
  elif CustName != '':
    retrieve_cust_cursor.execute("SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo WHERE CustomerName LIKE ? GROUP BY CustomerName ORDER BY COUNT(RentalBalance) DESC", ('%'+CustName+'%',))
  else:
    retrieve_cust_cursor.execute("SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo GROUP BY CustomerName ORDER BY COUNT(RentalBalance) DESC")
    
  cust_out_result = retrieve_cust_cursor.fetchall()
  
  print(cust_out_result)
  
  print_cust = ''
  
  rowCount = 0

  for cust_position in cust_out_result:
      print_cust += str((str(cust_position[0])) + " | " + str(cust_position[1]) + " | $" + str(cust_position[2]) + ".00\n")
      rowCount+=1

  print("Count: " + str(rowCount))

  print(print_cust)

  retrieve_cust_label = Label(retrieve_custWindow, text=("Customer ID | Customer Name | Remaining Balance\n\n")+print_cust+("\nCount: " + str(rowCount)))
  retrieve_cust_label.grid(row=3, column=0, columnspan=2)

# retrieve customer information
def retrieve_customer_win():
  # make retrieve customer window
  retrieve_custWindow = Toplevel(root)

  # set the window title
  retrieve_custWindow.title("Retrieve Customer Information")

  # set the dimensions
  retrieve_custWindow.geometry("500x500")

  # Making the Text Boxes and labels for customer ID
  # entering the component in the text box
  CustID_retrieve = Entry(retrieve_custWindow, width=30)
  # place the box
  CustID_retrieve.grid(row=0, column=1)
  # creating the label for the entry box
  CustID_retrieve_label = Label(retrieve_custWindow, text='CustID: ')
  # placing the label
  CustID_retrieve_label.grid(row=0, column=0)

  # Making the Text Boxes and labels for Customer Name
  # entering the component in the text box
  CustName_retrieve = Entry(retrieve_custWindow, width=30)
  # place the box
  CustName_retrieve.grid(row=1, column=1)
  # creating the label for the entry box
  CustName_retrieve_label = Label(retrieve_custWindow, text='Customer Name: ')
  # placing the label
  CustName_retrieve_label.grid(row=1, column=0)

  find_customer_button = Button(retrieve_custWindow, text='Find Customer', command=lambda: retrieve_cust_info(
      retrieve_custWindow, CustID_retrieve.get(), CustName_retrieve.get()))
  find_customer_button.grid(
      row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)



# Q5B
# This is the function that retrieves the vehicle information (5b)
def retrieve_vehicle_info(retrieve_vehicleWindow, VehicleID, CarDescription):
  # connecting to the sqlite database
  retrieve_vehicle_connect = sqlite3.connect('CarRental2019.db')

  # cursor to access to connection
  retrieve_vehicle_cursor = retrieve_vehicle_connect.cursor()

  print("Retrieving vehicle information")
# SELECT VIN, Vehicle, ROUND(CAST(OrderAmount AS float)/TotalDays, 2) AS AverageDailyPrice FROM vRentalInfo ORDER BY (OrderAmount/TotalDays);

  if VehicleID != '':
    retrieve_vehicle_cursor.execute(
        "SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo WHERE VIN LIKE ? AND Vehicle LIKE ? GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC", (('%'+VehicleID+'%'),('%'+CarDescription+'%'),))
  elif CarDescription != '':
    retrieve_vehicle_cursor.execute(
        "SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo WHERE Vehicle LIKE ? GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC", (('%'+CarDescription+'%'),))
  else:
    retrieve_vehicle_cursor.execute(
        "SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC")


  cust_out_result = retrieve_vehicle_cursor.fetchall()

  print(cust_out_result)

  print_cust = ''
  rowCount = 0
  for cust_position in cust_out_result:
      print_cust += str((str(cust_position[0])) + "  |  " + str(cust_position[1]) + "  |  $" + str(cust_position[2])+"\n")
      rowCount+=1
  
  print("Count: " + str(rowCount))
  
  retrieve_cust_label = Label(retrieve_vehicleWindow, text=(
      "VIN # | Vehicle Description  |  Daily Rate \n\n") + print_cust+("\nCount: " + str(rowCount)))
  retrieve_cust_label.grid(row=9, column=0, columnspan=2)


# This is the function that displays the window for retrieving vehicle information (5b)
def retrieve_vehicle_win():
  # make retrieve vehicle window
  retrieve_vehicleWindow = Toplevel(root)

  # set the window title
  retrieve_vehicleWindow.title("Retrieve Vehicle Information")

  # set the dimensions
  retrieve_vehicleWindow.geometry("500x500")

  # Making the Text Boxes and labels for VIN Number
  # entering the component in the text box
  VIN_retrieve = Entry(retrieve_vehicleWindow, width=30)
  # place the box
  VIN_retrieve.grid(row=0, column=1)
  # creating the label for the entry box
  VIN_retrieve_label = Label(retrieve_vehicleWindow, text='VIN #: ')
  # placing the label
  VIN_retrieve_label.grid(row=0, column=0)

  # Making the Text Boxes and labels for Vehicle Description
  # entering the component in the text box
  description_retrieve = Entry(retrieve_vehicleWindow, width=30)
  # place the box
  description_retrieve.grid(row=1, column=1)
  # creating the label for the entry box
  description_retrieve_label = Label(
      retrieve_vehicleWindow, text='Vehicle Description: ')
  # placing the label
  description_retrieve_label.grid(row=1, column=0)

  find_vehicle_button = Button(retrieve_vehicleWindow, text='Find Vehicle', command=lambda: retrieve_vehicle_info(
      retrieve_vehicleWindow, VIN_retrieve.get(), description_retrieve.get()))
  find_vehicle_button.grid(
      row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# This is the function that will display a list of all available vehicles
def view_vehicle_info(view_vehicleWindow):

  # connecting to the sqlite database
  view_vehicle_connect = sqlite3.connect('CarRental2019.db')

  # cursor to access to connection
  view_vehicle_cursor = view_vehicle_connect.cursor()

  # cursor to access to connection
  view_vehicle_cursor2 = view_vehicle_connect.cursor()

  print("Viewing Available Vehicles")

  # List all available vehicles
  view_vehicle_cursor.execute(
      "SELECT V.CarDescription FROM VEHICLE AS V, RENTAL AS R WHERE R.VehicleID = V.VehicleID AND R.Returned = 1 GROUP BY V.CarDescription",)

  print_list = ''

  list_result = view_vehicle_cursor.fetchall()

  #print(list_result)

  rowCount = 0

  for cust_position in list_result:
      print_list += str((str(cust_position[0])) + "\n")
      rowCount += 1

  list_label = Label(view_vehicleWindow, text=(
      "List of all Vehicles \n\n") + print_list + "\n\nCount: " + str(rowCount))
  list_label.grid(row=9, column=0, columnspan=2)


# This is the function that will display the window for a list of all available vehicles
def view_vehicle_win():
  # make retrieve vehicle window
  view_vehicleWindow = Toplevel(root)

  # set the window title
  view_vehicleWindow.title("View Available Vehicles")

  # set the dimensions
  view_vehicleWindow.geometry("500x500")

  # Button to output all available vehicles
  view_vehicle_button = Button(view_vehicleWindow, text='View Available Vehicles',
                               command=lambda: view_vehicle_info(view_vehicleWindow))
  view_vehicle_button.grid(row=2, column=0, columnspan=2,
                           pady=10, padx=10, ipadx=100)





# connect to sqlite database
root = Tk()
root.title('Car Rental Database')

# setting the size of the window
root.geometry("350x400")

# connecting to the sqlite database
car_rental_connect = sqlite3.connect(os.getcwd() + '/CarRental2019.db')
# cursor to access to connection
car_rental_cur = car_rental_connect.cursor()

# building gui components
title = Label(root, text='Car Rental Database', font='50')
title.grid(row=0, column=0, columnspan=2, pady=10, ipadx=100)

# create buttons
return_rental_btn = Button(root, text='Return Rental', command=return_rental_win)
return_rental_btn.grid(row=1, column=0, columnspan=2, pady=10, ipadx=100)

new_cust_btn = Button(root, text='Add New Customer', command=new_cust_win)
new_cust_btn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=100)

new_vhcl_btn = Button(root, text='Add New Vehicle', command=new_vehicle_win)
new_vhcl_btn.grid(row=3, column=0, columnspan=2, pady=10, ipadx=100)

new_rsrv_btn = Button(root, text='Add New Reservation', command=new_rental_win)
new_rsrv_btn.grid(row=4, column=0, columnspan=2, pady=10, ipadx=100)

get_cust_btn = Button(root, text='Retrieve Customer Info',
                      command=retrieve_customer_win)
get_cust_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=100)

get_vhcl_btn = Button(root, text='Retrieve Vehicle Info',
                      command=retrieve_vehicle_win)
get_vhcl_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=100)


view_vhcl_btn = Button(root, text='View Available Vehicles',
                       command=view_vehicle_win)
view_vhcl_btn.grid(row=7, column=0, columnspan=2, pady=10, ipadx=100)


# execute the tkinter components
root.mainloop()
