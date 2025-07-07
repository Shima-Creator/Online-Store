## Overview

This project is a basic online store built using Django. It provides a foundation for creating an e-commerce platform, including user authentication (buyers and sellers), product management, and order processing.

## Features

•   **User Authentication:**
    •   Separate profiles for buyers (address) and sellers (legal information, contact details, profile picture).
•   **Product Management:**
    •   Adding, editing, viewing products by seller.
    •   Products have a name, description, price, and image.
•   **Order Management:** 
    •   Order features here, like placing orders, order statuses.
•   **Comments:** Users can leave comments on products.
•   **User Orders:**  Keeps track of user orders and their statuses.
•   **Extensible Architecture:** The project is designed with Django's modular architecture, making it easy to add new features and customize existing ones.

## Technologies Used

•   **Python:** Programming language.
•   **Django:** Web framework.
•   **HTML:** Structure of web pages.
•   **CSS:** Styling of web pages.
•   **Database:** PostgreSQL.

## Setup Instructions

1.  **Clone the repository:**

```
    git clone https://github.com/Shima-Creator/Online-Store.git
    cd Online-Store
```

2. Create a virtual environment:
 ``` 
    python -m venv venv
```

3. Activate the virtual environment:

  •  Linux/macOS:

    
```
    source venv/bin/activate
```

  •  Windows:

    
```
    .\venv\Scripts\activate
```

4. Install dependencies:

  
```
  pip install -r requirements.txt
```

5. Configure the database:

  •  Set up your database (PostgreSQL).

6. Run migrations:

  
```
  python manage.py makemigrations
  python manage.py migrate
```

7. Create a superuser:

  
```
  python manage.py createsuperuser
```


8. Start the development server:

  
```
  python manage.py runserver
```

9. Access the application:

  Open your web browser and go to http://127.0.0.1:8000/ (or the address shown in your terminal).

10. Access the Django Admin:
  Open your web browser and go to http://127.0.0.1:8000/admin/ and login with the superuser created in step 7.

▌Models

•  User: Extends Django's AbstractUser with is_seller field.

•  Buyer: One-to-one relationship with User, stores buyer-specific information like address.

•  Seller: One-to-one relationship with User, stores seller-specific information like upd, legal_name, profile_pic, and social media links.

•  Category: Category's name, description.

•  Subcategory: ForeignKey relationship with Category, subcategory's name, description.

•  Basket: ForeignKey relationship with User, ForeignKey relationship with Product, quantity, active.

•  Shop: ForeignKey relationship with Seller, ForeignKey relationship with Category, shop_name, country, description.

•  Product: Product's name, photo, description, price, ForeignKey relationship with Subcategory, ForeignKey relationship with Shop, stock.

•  UserOrder: ForeignKey relationship with User, One-to-one relationship with Product, quantity, status.

•  Comments: ForeignKey relationship with Product, ForeignKey relationship with User, comment.


## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Write tests for your changes.
5.  Submit a pull request.

## Author

Ilya Shimanko

## Contact

shima.228@mail.ru

---
