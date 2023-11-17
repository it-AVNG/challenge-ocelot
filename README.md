# Code Challenge: Python API Development
Develop a RESTful API using Django or FastAPI framework that manages a simple "Bookstore". Your API will provide endpoints to create, read, update, and delete books in the store. Include functionality to handle user authentication to allow only registered users to modify the bookstore content.

## Requirements:

### Documentation:
- Live website links at : [amazon_site](http://ec2-54-254-200-121.ap-southeast-1.compute.amazonaws.com/api/docs/)
- Instructions on how to set up and run the application locally [install_localy.md](https://github.com/it-AVNG/challenge-ocelot/blob/main/install_locally.md)

#### API Functionality:

- Books model with fields: title, author, publish_date, ISBN, and price.
- CRUD operations for the Books model for authorized user, including uploading images.
- Implement user authentication: Users should register with at least an email and password
- Token authentication is applied
- All users (authenticated or not) can list and read information about the books, filtered field: author.

### Deployment:

- Deploy your application to a free hosting provider (e.g., Heroku, PythonAnywhere, or any other).
- Provide a URL to the live API.

### Bonus features implemented:
- Can upload an image with the book cover.
- Implement rate limiting for your API.
- Filtering books by author.
- Setup CI for GitHub actions.

## Application system architecture

Tech Stack:
- Django Rest Framework with Tokenauthentication
- Customed User Model using AbstractBaseUser
- Browseable API doc using with SwaggerUI
- Database PostgreSQL
- Proxy: NginX and uWSGI
- Deployed on AWS EC2 instance

System architechture diagram:
![[system_architecture.png]]
