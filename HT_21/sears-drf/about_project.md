## About Project

**Added Products Page:**

***Note:*** This page is accessible only to administrators.

This page contains a text field in which the user can enter any number of product identifiers. After submitting the
form, a scraper is launched that collects product information from the Sears website using the entered identifiers.

In addition, the scraping process runs in the background so as not to block the execution of the main thread.

This architecture allows the user to add and view products and get complete information about a particular product
without interrupting the main flow of the application.

**My Products Page:**

This page presents all the products presented in the system, indicating the main parameters, such as name and price.

**Detail-Product Page:**

Provides complete information about the selected product, name, price, ID, short description (in stock), brand, product,
image product, link to the product on the Sears website and other details.

**Change Product Page:**

***Note:*** This page is accessible only to administrators.

This page allows administrators to modify the details of a product in the system. Administrators can update information
such as the product's name, price, category, brand, and other relevant details.

**Basket Page:**

***Note:***  This page is accessible only to authenticated users.

All products added by the user to the cart are presented here, indicating the main parameters, such as name, price,
quantity. On the page you can change the number of products, delete one of the products, and empty the entire cart of
products.

**Categories Page:**

This page displays a list of available product categories. Clicking on a specific category will show a page with
products only from that category.

**Sign in Page:**

The sign-in page allows users to log in to their accounts.

**Sign up Page:**

The sign-up page is used for creating new user accounts.

**User Profile Page:**

The user profile page provides information and settings related to a user's account.

**Change Password Page:**

The change password page allows users to update their account passwords.