# *************************************** SETUP GLOBAL

from binascii import Error
from re import T
import string
from unittest import result
from flask import Flask, redirect, render_template, request, url_for
import sqlite3 as sql
import csv
import hashlib
from session import Session
from datetime import date


# *************************************** DEF GLOBAL VARS

 # -- authentication status
session = Session(0, 0, 0, 0)

# *************************************** END GLOBAL VARS

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'

@app.context_processor 
def inject_dict_for_all_templates():

    # Build the Navigation Bar
    if session.returnIsBuyer() == 0: # user is neither buyer or seller
        nav = [
        {"text": "Home", "url": url_for('index')},
        {"text": "Login", "url": url_for('login')},
        {
           "text": "More",
           "sublinks": [
                {"text": "Create Account", "url": url_for('create_account')},
                {"text": "Reset Password", "url": url_for('password')},
            ],
        },
        ]
    elif session.returnIsSeller() == 1: # user is a buyer and seller
        nav = [
        {"text": "Home", "url": url_for('index')},
        {
           "text": "Seller Menu",
           "sublinks": [
                {"text": "Listings", "url": url_for('listings')},
                {"text": "New Product", "url": url_for('publishproduct')},
            ],
        },
            {
            "text": "Account",
            "sublinks": [
                {"text": "Profile", "url": url_for('account')},
                {"text": "Recent Orders", "url": url_for('orders')},
                {"text": "Reset Password", "url": url_for('password')},
                {"text": "Logout", "url": url_for('logout')},
            ], 
        },
        {"text": "Cart", "url": url_for('cart')},
        ]
    else: # user is a buyer not seller NO OPTION TO LIST 
        nav = [
        {"text": "Home", "url": url_for('index')},
        {
           "text": "Account",
           "sublinks": [
                {"text": "Profile", "url": url_for('account')},
                {"text": "Recent Orders", "url": url_for('orders')},
                {"text": "Reset Password", "url": url_for('password')},
                {"text": "Logout", "url": url_for('logout')},
            ],
        },
        {"text": "Cart", "url": url_for('cart')},
        ]
    return dict(navbar = nav)



# *************************************** END SETUP


# default intructions: on host url return default index
@app.route('/')
def index():
    
    if session.returnIsReady() == 0:
        initDB() # when starting up re-gen DB 
        session.setIsReady(1)

    #categoriesHierarchy()
    #generateNav()

    products = homeProductListing()

    return render_template('index.html', products=products)


def homeProductListing():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Product_Listings WHERE active <> 0 LIMIT 12;')
    return cursor.fetchall()


def categoriesHierarchy():
    return render_template('index.html') # todo


def generateNav():
    return render_template('index.html') # todo


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
    connection.execute('CREATE TABLE IF NOT EXISTS Product_Listings(seller_email TEXT NOT NULL, listing_id INTEGER NOT NULL, category TEXT NOT NULL, title TEXT NOT NULL, product_name TEXT NOT NULL, product_description TEXT NOT NULL, price REAL NOT NULL, quanity INT NOT NULL, active INT NOT NULL, posted TEXT NOT NULL, ended TEXT, PRIMARY KEY (seller_email, listing_id) FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (category) REFERENCES Categories (category_name) );')
    file = open('data/Product_Listing.csv')
    contents = csv.reader(file)
    next(contents)
    insert_records = "INSERT INTO Product_Listings(seller_email, listing_id, category, title, product_name, product_description, price, quanity, active, posted, ended) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 1, date('now'), NULL)"
    cursor.executemany(insert_records, contents)


    # Orders
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, seller_email TEXT NOT NULL, listing_id INT NOT NULL, buyer_email TEXT NOT NULL, date TEXT NOT NULL, quanity INT NOT NULL, payment INT NOT NULL, cart INT NOT NULL, cancelled INT NOT NULL, FOREIGN KEY (seller_email) REFERENCES Sellers (email), FOREIGN KEY (buyer_email) REFERENCES Buyers (email), FOREIGN KEY (listing_id) REFERENCES Product_Listings (listing_id), FOREIGN KEY (payment) REFERENCES Credit_Cards (credit_card_num) );')
    insert_records = "INSERT INTO Orders(seller_email, listing_id, buyer_email, date, quanity, payment, cart, cancelled) VALUES(?, ?, ?, ?, ?, ?, 0, 0)"
    
    with open('data/Orders.csv') as file:
        contents = csv.reader(file)
        next(contents) # skip header row
        
        params = [(row[1], row[2], row[3], row[4], row[5], row[6]) for row in contents]
        cursor.executemany(insert_records, params)

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

        # give user vendor rights if they are an approved vendor
        vendorResult = isvendor_request(email,password)
        if vendorResult:
            session.setIsVendor(1)
            session.setIsBuyer(1)
            session.setIsSeller(1)
            session.setUserID(email)
            session.setHashedPassword(password)
            return redirect('/')

        # give user seller rights if they are an approved seller
        sellerResult = isseller_request(email, password)
        if sellerResult:
            session.setIsBuyer(1)
            session.setIsSeller(1)
            session.setUserID(email)
            session.setHashedPassword(password)
            return redirect('/')

        # authenticate buyer if account exists
        buyerResult = login_request(email, password)
        if buyerResult:
            session.setIsBuyer(1)
            session.setUserID(email)
            session.setHashedPassword(password)
            return redirect('/')
        else:
            error = 'Invalid Input: Email or Password Is Incorrect! Please try again.'

    return render_template('login.html', error=error)


def login_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Users JOIN Buyers ON Buyers.email = Users.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def isseller_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Users INNER JOIN Buyers ON Buyers.email = Users.email INNER JOIN Sellers ON Buyers.email = Sellers.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


def isvendor_request(emailaddress, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Users INNER JOIN Local_Vendors ON Local_Vendors.email = Users.email WHERE Users.email =''?'' AND Users.password =''?'';', (emailaddress, password))
    return cursor.fetchall()


# ****** END LOGINs


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = ""    

    if request.method == 'POST':

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
    connection.close()


def createaccount_request(email, password, first_name, last_name, gender, age, homeaddr, billaddr):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Users(email, password ) VALUES(?, ?)', (email, password) )
    connection.execute('INSERT INTO Buyers(email, first_name, last_name, gender, age, home_address_id, billing_address_id) VALUES(?, ?, ?, ?, ?, ?, ?)', (email, first_name, last_name, gender, age, homeaddr, billaddr))
    connection.commit()
    connection.close()


@app.route('/account', methods=['GET', 'POST'])
def account():
    
    if session.returnIsVendor() == 1:
        return redirect('/') # todo

    if session.returnIsBuyer() == 1:
        personal = personalDetails_request(session.returnUserID(), session.returnHashedPassword())
        billing = billingAddrDetails_request(session.returnUserID(), session.returnHashedPassword())
        home = homeAddrDetails_request(session.returnUserID(), session.returnHashedPassword())
        payments = paymentDetails_request(session.returnUserID(), session.returnHashedPassword())
        return render_template('account.html', personal=personal, billing=billing,home=home, payments=payments)
    return redirect('/')
 

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
        password = request.form['PasswordOld']
        password = hashlib.sha256(password.encode()).hexdigest()
        newpassword = request.form['Password']
        newpassword = hashlib.sha256(newpassword.encode()).hexdigest()
        result = verifyPassword_request(email, password)
        if result:
            changePassword_request(newpassword, email)
            return redirect('/login')
        else: 
            error = "Error: Wrong username of password, please try again." # todo -- not working 
            return render_template('password.html', error=error)
 
    return render_template('password.html', error=error)

def verifyPassword_request(email, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Buyers.email FROM Buyers LEFT JOIN Users ON Users.email =''?'' AND Users.password =''?'';', (email, password))
    return cursor.fetchall()


def changePassword_request(newpassword, email):
    connection = sql.connect('database.db')
    connection.execute('UPDATE Users SET password = ''?'' WHERE Users.email =''?'';', (newpassword, email))
    connection.commit()
    connection.close()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.setHashedPassword("NULL")
    session.setIsBuyer(0)
    session.setIsSeller(0)
    session.setUserID("NULL")
    return redirect('/')


@app.route('/product', methods=['GET', 'POST'])
def product():
    
    if request.method == 'POST':
        seller_email = request.form['SellerEmail-1']
        listingID = request.form['ListingID']
        product = selectedProduct_request(seller_email, listingID)
        sellerinfo = sellerinfo_request(seller_email)
        reviews = productReview_request(seller_email, listingID)
        return render_template('product.html', product=product, len=product[7] + 1, sellerinfo=sellerinfo, reviews=reviews)    
    return render_template('product.html')


def productReview_request(email, listingID):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Reviews WHERE Reviews.listing_id = ''?'' AND Reviews.seller_email = ''?'';', (listingID, email))
    return cursor.fetchmany() 

def sellerinfo_request(email):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT avg(Ratings.rating) FROM Ratings WHERE Ratings.seller_email = ''?'';', (email,))
    return cursor.fetchone() 


def selectedProduct_request(email, listingID):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Product_Listings WHERE Product_Listings.listing_id = ''?'' AND Product_Listings.seller_email = ''?'';', (listingID, email))
    return cursor.fetchone() 


@app.route('/publishproduct', methods=['GET', 'POST'])
def publishproduct():

    if session.returnIsSeller() == 0:
        return redirect('/')

    if request.method == 'POST':
        producttitle = request.form['ProductTitle']
        productname = request.form['ProductName']
        productdescription = request.form['ProductDescription']
        productprice = request.form['ProductPrice']
        productquanity = request.form['ProductQuanity']
        productcategory = request.form['ProductCategory']

        publishproduct(session.returnUserID(), producttitle, productname, productdescription, productprice, productquanity, productcategory)
        product = newProduct_request()
        return redirect('/product', product=product)

    if session.returnIsSeller() == 1:
        categories = categoryType_request()
        return render_template('publishproduct.html', categories=categories)

    return redirect('/')


def newProduct_request(email, title, name, desc, price, quanity, category):
    connection = sql.connect('database.db')
    connection.execute("INSERT INTO Product_Listings(seller_email, listing_id, category, title, product_name, product_description, price, quanity, active, posted, ended) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'), NULL)", (email, title, name, desc, price, quanity, category))
    connection.commit()
    connection.close() 


def publishProduct_request():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Categories.category_name FROM Categories')
    return cursor.fetchall()  


def categoryType_request():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Categories.category_name FROM Categories')
    return cursor.fetchall()    


@app.route('/listings', methods=['GET', 'POST'])
def listings():
    # return listings of current user

    if session.returnIsSeller() == 1:
        listings = allSellerListings_request(session.returnUserID())
        return render_template('listings.html', listings=listings)

    return redirect('/')


def allSellerListings_request(email):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Categories.category_name FROM Categories')
    return cursor.fetchall()      


@app.route('/cart', methods=['GET', 'POST'])
def cart():

    if session.returnIsBuyer() == 0:
        return redirect('/login')

    if request.method == 'POST':
        

        seller_email = request.form['SellerEmail']
        listingID = request.form['ListingID-1']
        quanity = int(request.form['SelectedQuanity'])
        prevMax = int(request.form['ProductMax'])
        price = request.form['ProductsPrice']
        price = int(price[1:])
        today = date.today()
        today = today.strftime("%m/%d/%y")

        total = quanity * price
        active = 1
        ended = "NULL"

        if (prevMax - quanity) == 0:
            active = 0
            today = date.today()
            ended = today
        
        updateProductListing_request(ended, active, prevMax - quanity, seller_email, listingID)
        addToCart_request(session.returnUserID(), seller_email, listingID, today, quanity, total)

    totalItems = totalCartItems_request(session.returnUserID())
    totalCost = cartTotalPrice_request(session.returnUserID())
    cart = unfinishedOrders_request(session.returnUserID())
    return render_template('cart.html', cart=cart, totalItems=totalItems, totalCost=totalCost)


def totalCartItems_request(buyer_email):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT count(Orders.transaction_id) FROM Orders WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1;', (buyer_email,))
    return cursor.fetchone() 


def cartTotalPrice_request(buyer_email):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT sum(Orders.payment) FROM Orders WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1;', (buyer_email,))
    return cursor.fetchone() 


def updateProductListing_request(ended, active, quanity, email, listingID):
    connection = sql.connect('database.db')
    connection.execute('Update Product_Listings SET ended = ''?'', active = ''?'', quanity = ''?'' WHERE Product_Listings.seller_email = ''?'' AND Product_Listings.listing_id = ''?'';', (ended, active, quanity, email, listingID))
    connection.commit()
    connection.close()      


def addToCart_request(buyer, seller, listing_id, orderdate, quanity, total):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Orders (seller_email, listing_id, buyer_email, date, quanity, payment, cart, cancelled) VALUES(?, ?, ?, ?, ?, ?, 1, 0)', (seller, listing_id, buyer, orderdate, quanity, total))
    connection.commit()
    connection.close()


def unfinishedOrders_request(buyer_email):
    connection = sql.connect('database.db')
    # cursor = connection.execute('SELECT * FROM Orders LEFT JOIN Product_Listings ON Orders.buyer_email = ''?'' AND Orders.cart = 1 AND Orders.listing_id = Product_Listings.listing_id AND Product_Listings.seller_email = Orders.seller_email;', (buyer_email, ))
    cursor = connection.execute('SELECT * FROM Orders WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1 AND Orders.cancelled = 0;', (buyer_email, ))
    return cursor.fetchall()   


# ******* REGION EMPTY CART
@app.route('/emptycart', methods=['GET', 'POST'])
def emptycart():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    cart = unfinishedOrders_request(session.returnUserID())

    for item in cart:
        returnItemsToListing_request(item)

    updateOrdersCartCancellFull_request()
    return redirect('/')


@app.route('/removeitem', methods=['GET', 'POST'])
def removeitem():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    if request.method == 'POST':
        transaction_id = request.form['TransactionID']
        listing = findOrderCancel_request(transaction_id)
        returnItemsToListing_request(listing)
        updateOrdersCartCancellSingle_request(transaction_id)
    
    totalItems = totalCartItems_request(session.returnUserID())
    totalCost = cartTotalPrice_request(session.returnUserID())
    cart = unfinishedOrders_request(session.returnUserID())
    return render_template('cart.html', cart=cart, totalItems=totalItems, totalCost=totalCost)


def findOrderCancel_request(transaction_id):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Orders WHERE Orders.transaction_id = ''?''', (transaction_id,))
    return cursor.fetchone()     


def findCancelledItem_request():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Orders WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1;', (session.returnUserID(),))
    return cursor.fetchone()  


def returnItemsToListing_request(item):
    quanity = item[5]
    seller_email = item[1]
    listing_id = item[2]
    listing = returnItemListingCurrentQuanity_request(seller_email, listing_id)
    currentquanity = listing[0]
    newquanity = currentquanity + quanity
    connection = sql.connect('database.db')
    connection.execute('Update Product_Listings SET quanity = ''?'', active = 1 WHERE Product_Listings.seller_email = ''?'' AND Product_Listings.listing_id = ''?'';', (newquanity, seller_email, listing_id))
    connection.commit()
    connection.close()  


def returnItemListingCurrentQuanity_request(email, listingID):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Product_Listings.quanity FROM Product_Listings WHERE Product_Listings.seller_email = ''?'' AND Product_Listings.listing_id = ''?'';', (email, listingID))
    return cursor.fetchone()    


def updateOrdersCartCancellSingle_request(transaction_id):
    connection = sql.connect('database.db')
    connection.execute('UPDATE Orders SET cart = 0, cancelled = 1 WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1 AND Orders.transaction_id = ''?'';', (session.returnUserID(), transaction_id))
    connection.commit()
    connection.close()


def updateOrdersCartCancellFull_request():
    connection = sql.connect('database.db')
    connection.execute('UPDATE Orders SET cart = 0, cancelled = 1 WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1;', (session.returnUserID(), ))
    connection.commit()
    connection.close()

# ***** END REGION EMPTY CART


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    checkoutCart_request()
    orders = finishedOrders_request()
    return render_template('orders.html', orders=orders) #cart = 0, cancelled = 0


def checkoutCart_request():
    connection = sql.connect('database.db')
    connection.execute('UPDATE Orders SET cart = 0, cancelled = 0 WHERE Orders.buyer_email = ''?'' AND Orders.cart = 1;', (session.returnUserID(), ))
    connection.commit()
    connection.close()    


@app.route('/orders', methods=['GET', 'POST'])
def orders():

    if session.returnIsBuyer() == 0:
        return redirect('/')
        
    orders = finishedOrders_request()
    return render_template('orders.html', orders=orders)


def finishedOrders_request():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Orders WHERE Orders.buyer_email = ''?'' AND Orders.cart = 0 AND Orders.cancelled = 0 ORDER BY date(date,"yyyy-mm-dd") DESC;', (session.returnUserID(),))
    return cursor.fetchall()       


@app.route('/rateseller', methods=['GET', 'POST'])
def rateseller():
    
    if session.returnIsBuyer() == 0:
        return redirect('/')

    if request.method == 'POST':    
        return render_template('rateseller.html', transaction_id=request.form['TransactionID'])


@app.route('/ratesellerhandle', methods=['GET', 'POST'])
def ratesellerhandle():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    ratingDesc = ['Awesome', 'Not Bad', 'Bad']
    
    if request.method == 'POST':
        transaction_id = request.form['TransactionID']
        
        today = date.today()
        today = today.strftime("%m/%d/%y")
        info = transactionSeller_request(transaction_id)
        seller = info[0]
        rateSeller_request()


def transactionSeller_request(transaction_id):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT Orders.seller_email, Orders.listing_id FROM Orders WHERE AND Orders.transaction_id = ''?'';', (transaction_id,))
    return cursor.fetchone()     


def rateSeller_request(buyer_email, seller_email, date, rating, rating_desc):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Ratings(buyer_email, seller_email, date, rating, rating_desc) VALUES(?, ?, ?, ?)', (buyer_email, seller_email, date, rating, rating_desc))
    connection.commit()
    connection.close()


@app.route('/reviewproduct', methods=['GET', 'POST'])
def reviewproduct():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    if request.method == 'POST':    
        return render_template('reviewproduct.html', transaction_id=request.form['TransactionID'])


@app.route('/reviewproducthandle', methods=['GET', 'POST'])
def reviewproducthandle():

    if session.returnIsBuyer() == 0:
        return redirect('/')

    if request.method == 'POST':

        transaction_id = request.form['TransactionID']
        reviewedBefore = transactionSeller_request(transaction_id)

        if reviewedBefore:
            info = transactionSeller_request(transaction_id)
            seller = info[0]
            print(seller)
            listingID = info[1]
            print(listingID)
            review = request.form['ProductReview']
            reviewProduct_request(session.returnUserID(), seller, listingID, review)
    
    orders = finishedOrders_request()
    return render_template('orders.html', orders=orders)

def findPreviousReview_request(transaction_id, ):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Reviews LEFT JOIN Orders ON Orders.transaction_id = ''?'' AND Orders.buyer_email = Reviews.buyer_email AND Orders.seller_email = Reviews.seller_email AND Orders.listing_id = Reviews.listing_id;', (transaction_id,))
    return cursor.fetchone()     


def reviewProduct_request(buyer_email, seller_email, listing_id, review_desc):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Ratings(buyer_email, seller_email, date, rating, rating_desc) VALUES(?, ?, ?, ?)', (buyer_email, seller_email, listing_id, review_desc))
    connection.commit()
    connection.close()


# default instructions
if __name__ == "__main__":
    app.run()