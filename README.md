# Demo Portfolio Project: Django API Tech Store

## **Project Overview**
The **Django API Tech Store** is a project built using Django.  
It is a RESTful API that enables users to interact with the store in different ways based on their roles : Customers, Vendor and store Manager.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## **Key Features**
- ### **Unauthenticated Customers**: 
  - Can view product listings and retrieve essential product details, such as name, category, description, and price.
- ### **Vendors**: 
  - Have access to product details along with additional information like SKU, stock quantity, and the ability to view inactive products.
- ### **Store Manager**: 
  - Has full access to all product information, including managing product data and stock.
- ### **Order Management**:
  - Vendor can place orders for products and view their own orders.
  - The Manager has visibility over all orders.
- ### **Product Management**:
  - Both Vendor and the Manager can create new products.
- ### **Out-of-Stock Products**: 
  - The list of out-of-stock products is reserved exclusively for the store team.
- ### **Query Filters**: 
  - Users can filter product listings using various criteria like name, category, and SKU. Custom filters can be added, and pagination is enabled to avoid excessive data loading.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## **Installation Guide**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sundayz-hunter/DjangoREST-TechStore
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environement file**: 
- Rename `.env-dist` to `.env` without making any modifications to use the basic SQLite3 database, or adapt it according to your specific database information.

4. **Database Setup**:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
5. **Populate Database**:
     ```bash
     python manage.py populate_db
     ```
6. **Start Server**:
     ```bash
     python manage.py runserver
     ```
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Users 

- Two users are automatically created when populating the database:

#### Manager creds:
```
manager:manager
```

#### Vendor creds:
  ```
  vendor:vendor
  ```

Customers have access to the public API to view products in stock at the store.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Login & Authentication

- For simplicity, authentication is handled via sessions when using this project through a browser.  
For Manager and Vendor you can login on home page (http://127.0.0.1:8000/) or use admin page (http://127.0.0.1:8000/admin/login/)

- Alternatively, you can use token authentication if you prefer using Postman or any other API client.  
Token expiration hasn’t been implemented for ease of use.  
In a real production environment, it’s recommended to use JWT for authentication.

### Token via API:
- Do a POST request with the Manager or Vendor creds at : http://127.0.0.1:8000/api/v1/auth/get-token

The original token authentication method of Django has been customized to pass a standard header in your requests like :
```
Authorization: Bearer b3b80815206a81fae18f50a8e26ecc95c1b46dd8
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## API Documentation:
- Swagger: http://127.0.0.1:8000/api/schema/swagger-ui
- Redoc: http://127.0.0.1:8000/api/schema/redoc
- Postman Collection: json Postman collection file is available (api-v1.postman_collection.json)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Additional Tool:

### Django Silk:
- Django Silk provides performance monitoring and profiling for your Django application, helping to analyze database queries and measure application performance.
- Find it at : http://127.0.0.1:8000/silk/


