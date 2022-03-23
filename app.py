# *************************************** SETUP GLOBAL

import string
from flask import Flask, redirect, render_template, request
import sqlite3 as sql
import csv
import hashlib

app = Flask(__name__)



host = 'http://127.0.0.1:5000/'

# *************************************** END SETUP


# *************************************** DEF GLOBAL VARS

 # -- authentication status
isSeller = 0
isBuyer = 0

# *************************************** END GLOBAL VARS


# default intructions: on host url return default index
@app.route('/')
def index():
    initDB()
    result = showUsers()
    return render_template('index.html', result=result)


def showUsers():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Users;')
    return cursor.fetchall()



# Create user schema and insert data into users table
def initDB():
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    # Clean DB
    cursor.execute('DROP TABLE IF EXISTS Sellers;')
    cursor.execute('DROP TABLE IF EXISTS Buyers;')
    cursor.execute('DROP TABLE IF EXISTS Users;')
    cursor.execute('DROP TABLE IF EXISTS Credit_Cards;')
    cursor.execute('DROP TABLE IF EXISTS Zipcode_Info;')   
    cursor.execute('DROP TABLE IF EXISTS Address;')
    cursor.execute('DROP TABLE IF EXISTS Local_Vendors;')
    cursor.execute('DROP TABLE IF EXISTS Categories;')
    cursor.execute('DROP TABLE IF EXISTS Product_Listings;')
    cursor.execute('DROP TABLE IF EXISTS Orders;')
    cursor.execute('DROP TABLE IF EXISTS Reviews;')
    cursor.execute('DROP TABLE IF EXISTS Ratings;')

    # Users
    cursor.execute('CREATE TABLE IF NOT EXISTS Users(email TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL);')
    file = open('data/Users.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Users(email, password) VALUES(?, ?)"
    cursor.executemany(insert_records, contents)

    # Buyers
    connection.execute('CREATE TABLE IF NOT EXISTS Buyers(email TEXT NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, gender TEXT NOT NULL, age INT NOT NULL, home_address_id INT NOT NULL, billing_address_id INT NOT NULL, FOREIGN KEY (email) REFERENCES Users (email) );')
    file = open('data/Buyers.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Buyers(email, first_name, last_name, gender, age, home_address_id, billing_address_id) VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Sellers 
    connection.execute('CREATE TABLE IF NOT EXISTS Sellers(email TEXT NOT NULL PRIMARY KEY, routing_number TEXT NOT NULL, account_number TEXT NOT NULL, balance REAL NOT NULL, FOREIGN KEY (email) REFERENCES Buyers (email) );')
    file = open('data/Sellers.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Sellers(email, routing_number, account_number, balance) VALUES(?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Credit Card
    connection.execute('CREATE TABLE IF NOT EXISTS Credit_Cards(credit_card_num INT NOT NULL PRIMARY KEY, card_code INT NOT NULL, expire_month INT NOT NULL, expire_year INT NOT NULL, card_type TEXT NOT NULL, owner_email TEXT NOT NULL, FOREIGN KEY (owner_email) REFERENCES Buyers (email) );')
    file = open('data/Credit_Cards.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Credit_Cards(credit_card_num, card_code, expire_month, expire_year, card_type, owner_email) VALUES(?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Zip Code
    connection.execute('CREATE TABLE IF NOT EXISTS Zipcode_Info(zipcode INT NOT NULL PRIMARY KEY, city TEXT NOT NULL, state_id INT NOT NULL, population INT NOT NULL, density INT NOT NULL, county_name TEXT NOT NULL, timezone TEXT NOT NULL);')
    file = open('data/Zipcode_Info.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Zipcode_Info(zipcode, city, state_id, population, density, county_name, timezone) VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)   

    # Address
    connection.execute('CREATE TABLE IF NOT EXISTS Address(address_id INT NOT NULL PRIMARY KEY, zipcode INT NOT NULL, street_num INT NOT NULL, street_name TEXT NOT NULL, FOREIGN KEY (zipcode) REFERENCES Zipcode_Info (zipcode) );')
    file = open('data/Address.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Address(address_id, zipcode, street_num, street_name) VALUES(?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Local Vendors
    connection.execute('CREATE TABLE IF NOT EXISTS Local_Vendors(email TEXT NOT NULL PRIMARY KEY, buisness_name TEXT NOT NULL, buisness_address_id INT NOT NULL, customer_service_number INT NOT NULL, FOREIGN KEY (email) REFERENCES Sellers (email) );')
    file = open('data/Local_Vendors.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Local_Vendors(email, buisness_name, buisness_address_id, customer_service_number) VALUES(?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Categories
    connection.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category TEXT NOT NULL, category_name TEXT NOT NULL PRIMARY KEY, FOREIGN KEY (parent_category) REFERENCES Categories (category_name) );')
    file = open('data/Categories.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Categories(parent_category, category_name) VALUES(?, ?)"
    cursor.executemany(insert_records, contents)

    # Product Listings
    connection.execute('CREATE TABLE IF NOT EXISTS Product_Listings(seller_email TEXT NOT NULL, listing_id INT NOT NULL, category TEXT NOT NULL, title TEXT NOT NULL, product_name TEXT NOT NULL, product_description TEXT NOT NULL, price REAL NOT NULL, quanity INT NOT NULL, PRIMARY KEY (seller_email, listing_id), FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (category) REFERENCES Categories (category_name) );')
    file = open('data/Product_Listing.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Product_Listings(seller_email, listing_id, category, title, product_name, product_description, price, quanity) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Orders
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(transaction_id INT NOT NULL PRIMARY KEY, seller_email TEXT NOT NULL, listing_id INT NOT NULL, buyer_email TEXT NOT NULL, date TEXT NOT NULL, quanity INT NOT NULL, payment INT NOT NULL, FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (buyer_email) REFERENCES Buyers (email), FOREIGN KEY (listing_id) REFERENCES Product_Listings (listing_id), FOREIGN KEY (payment) REFERENCES Credit_Cards (credit_card_num) );')
    file = open('data/Orders.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Orders(transaction_id, seller_email, listing_id, buyer_email, date, quanity, payment) VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Reviews 
    connection.execute('CREATE TABLE IF NOT EXISTS Reviews(buyer_email TEXT NOT NULL, seller_email TEXT NOT NULL, listing_id INT NOT NULL, review_desc TEXT NOT NULL, PRIMARY KEY (buyer_email, seller_email, listing_id), FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (buyer_email) REFERENCES Buyers (email), FOREIGN KEY (listing_id) REFERENCES Product_Listings (listing_id) );')
    file = open('data/Reviews.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Reviews(buyer_email, seller_email, listing_id, review_desc) VALUES(?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # Ratings
    connection.execute('CREATE TABLE IF NOT EXISTS Ratings(buyer_email TEXT NOT NULL, seller_email TEXT NOT NULL, date TEXT NOT NULL, rating INT NOT NULL, rating_desc TEXT NOT NULL, PRIMARY KEY (buyer_email, seller_email, date), FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (buyer_email) REFERENCES Buyers (email) );')
    file = open('data/Ratings.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Ratings(buyer_email, seller_email, date, rating, rating_desc) VALUES(?, ?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    connection.commit()
    connection.close()


# ****** START LOGINs


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ""
    if request.method == 'POST':

        # hash sent password
        password = request.form['Password']
        #password = hashlib.md5(password.encode())

        # give user seller rights if they are an approved seller
        sellerResult = isseller_request(request.form['EmailAddress'], password)
        if sellerResult:
            isSeller = True
            isBuyer = True 
            error = 'User is a seller and authenticated'
            return render_template('login.html', error=error, result=sellerResult) # future redirect to home page, but as auth user w/ acct type. Ex: isSeller, isBuyer

        # authenticate buyer if account exists
        buyerResult = login_request(request.form['EmailAddress'], password)
        if buyerResult:
            isBuyer = True
            error = 'User is a buyer, but not a seller'
            return render_template('login.html', error=error, result=buyerResult) # future redirect to home page, but as auth user w/ acct type. Ex: isSeller, isBuyer
        else:
            error = 'Invalid Input: Email or Password Is Incorrect! Please try again.'

    return render_template('login.html', error=error)


def login_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.first_name, Buyers.last_name FROM Users JOIN Buyers ON Buyers.email = Users.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def isseller_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.first_name, Buyers.last_name FROM Users INNER JOIN Buyers ON Buyers.email = Users.email INNER JOIN Sellers ON Buyers.email = Sellers.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


# ****** END LOGINs

# on delete (POST: AMBIGUOUS INSTRUCTIONS so delete pid to delete user on pid) on default load table with all results from users if delete reprint new table on no action return page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = ""    

    if request.method == 'POST':

        # Data validation

        email = request.form['Email'] # todo add format validation like @xxx.xxx

        password = request.form['Password']
        r_password = request.form['repeat_Password']


        firstname = request.form['FirstName']
        lastname = request.form['LastName']

        gender = request.form['Gender'] # combo box todo

        age = request.form['Age'] # combo box todo

        # create billing and home address


        address_id = ""
        addrHome = createaddress(address_id, request.form['Zipcode'], request.form['street_num'], request.form['street_name'])
        addrBill = addrHome
        
        # for now home addr = bill addr untill a same as checkbox is implemented
        #addrBill = createaddress(request.form['Zipcode'], request.form['street_num'], request.form['street_name'])

        createaccount_request(email, password, firstname, lastname, gender, age, addrHome, addrBill)
        redirect('/login')
    return render_template('create_account.html', error=error)


def createaddress(address_id, zipcode, street_num, street_name):
    connection = sql.connect('database.db')
    connection.execute('insert_records = "INSERT INTO Address(address_id, password) VALUES(?, ?, ?, ?)', (address_id, zipcode, street_num, street_name))
    connection.commit()


def createaccount_request(email, password, first_name, last_name, gender, age, homeaddr, billaddr):
    connection = sql.connect('database.db')
    connection.execute('insert_records = "INSERT INTO Users(email, password) VALUES(?, ?, ?, ?, ?, ?, ?)', (email, password, first_name, last_name, gender, age, homeaddr, billaddr))
    connection.commit()


# default instructions
if __name__ == "__main__":
    app.run()