# Health Check
Get health status of the API
/api/health-check/

# Book
Get book list /api/book/
Get,put,patch,delete book
+ Get - list all book
+ Post Create book

## specific book by id
Only owner of the book is allowed to edit the object
anon can view the book
+ Get view details of book
+ Put/patch - update book
+ Delete - delete book

### Upload image
endpoint at /upload-image/
+ support POST

dependencies: Pillow for python
+ zlib,zlib-dec
+ jpeg-dev

post image /api/book/isbn/

# Schema
get API schema
/api/schema/

# User

/api/user/create/
/api/user/token/
/api/user/me/



