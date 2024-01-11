## About Project

**Added Products Page:**

This page contains a text field in which the user can enter any number of product identifiers. After submitting the
form, a scraper is launched that collects product information from the Sears website using the entered identifiers.

**My Products Page:**

Here are all the products that are presented in the system, indicating the main parameters such as name and price.

**Detail-Product Page:**

Provides complete information about the selected product, name, price, ID, short description (in stock), brand, product,
image product, link to the product on the Sears website and other details.

**Basket Page:**

All products added by the user to the cart are presented here, indicating the main parameters, such as name, price,
quantity. On the page you can change the number of products, delete one of the products, and empty the entire cart of
products.

In addition, the scraping process runs in the background so as not to block the execution of the main thread.

This architecture allows the user to add and view products and get complete information about a particular product
without interrupting the main flow of the application.