# *************************************** SETUP GLOBAL

from binascii import Error
import string
from unittest import result
from flask import Flask, redirect, render_template, request, url_for
import sqlite3 as sql
import csv
import hashlib
from session import Session


# *************************************** DEF GLOBAL VARS

 # -- authentication status
session = Session(0, 0)

# *************************************** END GLOBAL VARS

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'

@app.context_processor 
def inject_dict_for_all_templates():

    # Build the Navigation Bar
    if session.returnIsBuyer() == 0:
        nav = [
        {"text": "Home", "url": url_for('index')},
        {"text": "Login", "url": url_for('login')},
        {
           "text": "More",
           "sublinks": [
                {"text": "Create Account", "url": url_for('create_account')},
                {"text": "Reset Password", "url": url_for('password')},
                {"text": "Logout", "url": url_for('logout')},
            ],
        },
        ]
    else: 
        nav = [
        {"text": "Home", "url": url_for('index')},
        {
           "text": "Account",
           "sublinks": [
                {"text": "Profile", "url": url_for('account')},
                {"text": "Reset Password", "url": url_for('password')},
                {"text": "Logout", "url": url_for('logout')},
            ],
        },
        ]
        
    return dict(navbar = nav)



# *************************************** END SETUP


# default intructions: on host url return default index
@app.route('/')
def index():
    initDB()
    #categoriesHierarchy()
    #generateNav()
    #result = allProductListing()
    #return render_template('index.html', result=result)
    return render_template('index.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')



def allProductListing():
    return render_template('index.html')

def categoriesHierarchy():
    return render_template('index.html')


def generateNav():
    return render_template('index.html')


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
    insert_records = "INSERT INTO Users(email, password) VALUES(?, ?)"

    with open('data/Users.csv') as file:
        contents = csv.reader(file)
        next(contents) # skip header row
        
        params = [(row[0], hashlib.sha256(row[1].encode()).hexdigest()) for row in contents]
        cursor.executemany(insert_records, params)

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
    connection.execute('CREATE TABLE IF NOT EXISTS Address(address_id TEXT NOT NULL PRIMARY KEY, zipcode INT NOT NULL, street_num INT NOT NULL, street_name TEXT NOT NULL, FOREIGN KEY (zipcode) REFERENCES Zipcode_Info (zipcode) );')
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


        email = request.form['EmailAddress']
        # hash sent password
        password = request.form['Password']
        
        password = hashlib.sha256(password.encode()).hexdigest()

        # give user seller rights if they are an approved seller
        sellerResult = isseller_request(email, password)
        if sellerResult:
            session.setIsBuyer(1)
            session.setIsSeller(1)
            session.setUserID(email)
            session.setHashedPassword(password)
            return render_template('login.html', error=Error) # future redirect to home page, but as auth user w/ acct type. Ex: isSeller, isBuyer

        # authenticate buyer if account exists
        buyerResult = login_request(email, password)
        if buyerResult:
            session.setIsBuyer(1)
            session.setUserID(email)
            session.setHashedPassword(password)
            return render_template('index.html', error=error) # future redirect to home page, but as auth user w/ acct type. Ex: isSeller, isBuyer
        else:
            error = 'Invalid Input: Email or Password Is Incorrect! Please try again.'

    return render_template('login.html', error=error)


def login_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.email FROM Users JOIN Buyers ON Buyers.email = Users.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def isseller_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.email FROM Users INNER JOIN Buyers ON Buyers.email = Users.email INNER JOIN Sellers ON Buyers.email = Sellers.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


# ****** END LOGINs


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = ""    

    if request.method == 'POST':
        
        # Data validation

        email = request.form['EmailAddress'] # todo add format validation like @xxx.xxx

        password = request.form['Password']
        r_password = request.form['repeat_Password']

        if (password == r_password):
            password = hashlib.sha256(password.encode()).hexdigest()
        else:
           error = 'Error: Form passwords do not match.'
           return render_template('create_account.html', error=error)

        firstname = request.form['FirstName']
        lastname = request.form['LastName']

        gender = request.form['Gender'] # combo box todo

        age = request.form['Age'] # combo box todo

        # create billing and home address

        #hash = random.getrandbits(128)
        address_id = 'billy'
        addrBill = address_id
        addrHome = address_id
        createaddress_request(address_id, request.form['ZipCode'], request.form['StreetNumber'], request.form['StreetName'])
        
        # for now home addr = bill addr untill a same as checkbox is implemented
        #addrBill = createaddress(request.form['Zipcode'], request.form['street_num'], request.form['street_name'])

        createaccount_request(email, password, firstname, lastname, gender, age, addrHome, addrBill)
        return redirect('/login')
    return render_template('create_account.html', error=error)


def createaddress_request(address_id, zipcode, street_num, street_name):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Address(address_id, zipcode, street_num, street_name) VALUES(?, ?, ?, ?)', (address_id, zipcode, street_num, street_name))
    connection.commit()


def createaccount_request(email, password, first_name, last_name, gender, age, homeaddr, billaddr):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Users(email, password ) VALUES(?, ?)', (email, password) )
    connection.execute('INSERT INTO Buyers(email, first_name, last_name, gender, age, home_address_id, billing_address_id) VALUES(?, ?, ?, ?, ?, ?, ?)', (email, first_name, last_name, gender, age, homeaddr, billaddr))
    connection.commit()


@app.route('/account', methods=['GET', 'POST'])
def account():
    error = "Error... No account detected"    
    
    if session.returnIsBuyer() == 1:
        personal = personalDetails_request(session.returnUserID(), session.returnHashedPassword())
        billing = billingAddrDetails_request(session.returnUserID(), session.returnHashedPassword())
        home = homeAddrDetails_request(session.returnUserID(), session.returnHashedPassword())
        payments = paymentDetails_request(session.returnUserID(), session.returnHashedPassword())
        return render_template('account.html', personal=personal, billing=billing,home=home, payments=payments)
    return render_template('account.html', error=error)
 

def personalDetails_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.email, Buyers.first_name, Buyers.last_name, Buyers.age, Buyers.gender FROM Users JOIN Buyers ON Buyers.email = Users.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def billingAddrDetails_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Address.street_name, Address.street_num, Zipcode_Info.city, Zipcode_Info.state_id, Address.zipcode FROM Users LEFT JOIN Buyers ON Buyers.email = Users.email LEFT JOIN Address ON Buyers.billing_address_id = Address.address_ID LEFT JOIN Zipcode_Info ON Zipcode_Info.zipcode = Address.zipcode WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def homeAddrDetails_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Address.street_name, Address.street_num, Zipcode_Info.city, Zipcode_Info.state_id, Address.zipcode FROM Users LEFT JOIN Buyers ON Buyers.email = Users.email LEFT JOIN Address ON Buyers.billing_address_id = Address.address_ID LEFT JOIN Zipcode_Info ON Zipcode_Info.zipcode = Address.zipcode WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()

def paymentDetails_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT substr(Credit_Cards.credit_card_num, 16,4) FROM Users LEFT JOIN Buyers ON Buyers.email = Users.email LEFT JOIN Credit_Cards ON Credit_Cards.owner_email = Buyers.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchone()


@app.route('/password', methods=['GET', 'POST'])
def password():
    error = "Please enter user account and new password."            

    if request.method == 'POST':
        email = request.form['EmailAddress']
        password = request.form['Password']
        password = hashlib.sha256(password.encode()).hexdigest()
        result = verifyPassword_request(email, password)
        if result: 

            return redirect('/login')
        else: 
            error = "Error invalid username or password, please try again"
            return render_template('password.html', error=error)
    return render_template('password.html', error=error)

def verifyPassword_request(email, password):



def changePassword_request(email, password):



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.setHashedPassword("NULL")
    session.setIsBuyer(0)
    session.setIsSeller(0)
    session.setUserID("NULL")
    return render_template('index.html')

# default instructions
if __name__ == "__main__":
    app.run()