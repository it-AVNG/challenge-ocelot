# Code Challenge: Python API Development

**Objective:**

Develop a RESTful API using Django or FastAPI framework that manages a simple "Bookstore". Your API will provide endpoints to create, read, update, and delete books in the store. Include functionality to handle user authentication to allow only registered users to modify the bookstore content.

## Requirements:

### Documentation:

- Provide a README file that includes:
  - Live website links at : URL
  - Instructions on how to set up and run the application locally [[install_localy.md]]

#### API Functionality:

- Books model with fields: title, author, publish_date, ISBN, and price.
- CRUD operations for the Books model for authorized user, including uploading images.
- Implement user authentication: Users should register with at least an email and password
- Token authentication is applied
- All users (authenticated or not) can list and read information about the books, filtered field: author.

### System Diagram:

- Provide a system architecture diagram showing the API, database, and any other components of your system.

### Deployment:

- Deploy your application to a free hosting provider (e.g., Heroku, PythonAnywhere, or any other).
- Provide a URL to the live API.

### Bonus (optional):

- The API needs to support a volume of 1000 requests per second in a stress test in both write and read operations.
- Can upload an image with the book cover.
- Implement rate limiting for your API.
- Add filters to list endpoints, such as filtering books by author or publish_date.
- Setup CI/CD
