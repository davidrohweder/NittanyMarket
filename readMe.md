# Nittany Market
David Rohweder 
431w Submission
4-25-2022

## This is my Nittany Market submission.

### Usage

To start run:

```batch
C:/Users/<username>/AppData/Local/Microsoft/WindowsApps/python3.10.exe C:\Users\<username>\<folder>\NittanyMarket\app.py
```

Example

```batch
C:/Users/david/AppData/Local/Microsoft/WindowsApps/python3.10.exe C:\Users\david\Desktop\NittanyMarket\app.py
```

After, you will be presented with the local host start page. Or at address: http://127.0.0.1:5000/

By default, all website users are visitors until they authenticate by either logging in or creating an account. All visitors can view certain information by default without having to authenticate. These such things include prodcuts, products per category, searched products, individual product listings, and seller information. 

Users can find products by either locating the default first 12 on the homepage, browsing by parent categories or child categories, searching for products, or clicking individual product cards on the homepage to find more information.

Once a user has found a desired product they have the ability to view the product by clicking the product card on the homepage. Once the card is loaded the user has access to the most important product information.

A product card lists the category, name, and title of product as well as a selection combo box of the range from 1 to stock of quanity. This information is listed in a main feautered style box and below more information is listed. Directly below the featured box users can find a link to a seller profile as well as an aggegate average seller rating from all of the ratings buyers made of the seller. Below the seller information is a product description. In the next section of the product page, product reviews are shown, which are reviews made of the product from users and what they wrote about the product.

If users want the product they can add it to their cart. However, once a user adds the quanity of the desired product to the cart they must be logged in. If the prospective buyer is not authenticated, they will be rediected to login before purchasing. Once the user is authenticated they have the ability to add products to their cart. 

When a product is added to a cart the quanity is reflected and removed from the total available in the homepage (if the remainer is zero the product is made inactive and not displayed anymore). Users can as many products as they want to their cart before checking out. In the cart page users are privy to several options and information sources. First, buyers have the option to remove all items from their cart which will then be sent back to the total quanity available in the product listing. Or users have the option to remove individual items from their cart which will then be returned to the product listing quanity. Furthurmore, buyers have access to the total number of products and a sub total of the amount owed in their cart. 

Once a buyer wishes to checkout the items in their cart, all of the products in the cart will become orders in the buyers order history. Previous buyer orders can be viewed at any time, along with the current cart contents for any authenticated user when they click on orders or cart in the navigation bar. Once the buyer is on the orders page they have the ability to review the purchased product once or rate the seller (once per day)

Moreover, the nav bar is dynamic in the sense that visitors, buyers, and sellers have different navigation bars as they have different functionalities available to them.

When a seller logs in, they share the same functionalities as buyers; however, they also have access to a seller menu. On this menu they have the option to view their current listings or create new listings. 

The seller listing page shows all active seller listings on the market. The seller has the option to remove any or all listings from the market if they choose. The seller publish product page is simplicitic but gives sellers the ability to publish required product information. 

All buyers or sellers have the option to view their information or reset their password on under the account tab in the navigation bar.

## Bugs and Issues

### Current
None at the moment

### Contact

If any bugs arise please contact djr6005@psu.edu for assistance
