# Project Scrape Sears Products

## Project Overview

- [Task](./task.md)
- [About Project](./about_project.md)
- [Quick Start with Docker (recommend)](./quick_start_docker.md)
- [Quick Start without Docker](./quick_start_without_docker.md)

## Accessing the Development Server and Features:

- Visit [add-products](http://127.0.0.1:8000/products/add-products/). And add product IDs for scraping
  from [site](https://www.sears.com/).
    - example Product ID:
        - `p-A093086676`
        - `p-SPM6458104507`
        - `p-SPM9463331817`
- On the page [products](http://127.0.0.1:8000/products/). You can see the products after scraping.
- On the page http://127.0.0.1:8000/products/detail-product/ `id-product`. You can see detailed information about
  the product and add product to cart.
- On the page [basket](http://127.0.0.1:8000/basket/). You can see all the products you ordered... Change their
  quantity, delete one product or empty the entire cart.
- On the page [task](http://127.0.0.1:8000/task/). You can read about the project task.
- On the page [admin-site](http://127.0.0.1:8000/admin/products/product/). You can select any product and change it.