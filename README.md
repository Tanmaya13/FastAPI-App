# FastAPI CRUD MongoDB Project

## About
A backend application built using FastAPI to perform CRUD operations using MongoDB. The application is hosted using Render.
try it: https://fastapi-app-i2fq.onrender.com/docs
NOTE:- The server will be started automatically once request is made for the first time. Please allow sometime for the API response.

## Functionalities & Features
1. User can perform CRUD operations on items and clock-in collections.
2. The "items" colection contains name(str), email(str), item_name(str), quantity(str), expiry_date (str yyyy-mm-dd) fields.
3. The "clock_in_records" collection contains email(str), location(str) fields.
4. The user filter records based on the filtering parameters.
5. Aggregation API can be used to count no. of items for each email.
6. Validations are added for the payload to check for valid email, name, dates etc.
7. Standard HTTP methods and status codes are implemented for all the APIs.
8. Documentation of API using FastAPI's integrated Swagger UI.

## Tech Stack
* Python (3.11.8)
* FastAPI
* MongoDB

## API Documentation
1. /Root :- A sample guide to access the APIs.
2. /items :- used to insert item details into the DB. Payload structure:
   {
      "name": "user name",
      "email": "user email address",
      "item_name": "name of the item",
      "quantity": no. of items,
      "expiry_date": "expiry date of item in yyyy-mm-dd format"
    }
3. /items/filter :- fetch item records based on filtering conditions like email, quantity, expiry_date, insert_date.
   NOTE:- The response will be based on values greater than the provided parameters. For example, if insert_date is 2024-10-11, then those records will be fetched whose insert_date is greater than 2024-10-11.
4. /items/aggregate :- it will return the count of items for each email (grouped by email).
5. /items/{item_id} :- the GET method will return the details of the item_id provided. If invalid ID is provided, then it will generate error response.
6. /items/{item_id} :- the PUT method is used to update the item details based on the item ID provided.
7. /items/{item_id} :- the DELETE method is used to delete the record from the DB containing id as the provided item_id.
8. /clock-in :- the POST method is used to create a clock-in record in the DB. Payload structure:
    {
      "email": "email address of the user",
      "location": "location of the user"
    }
9. /clock-in/filter :- this is used to fetch records based on the filtering parameters.
10. /clock-in/{clock_in_record_id} :- this GET method is used to fetch the clock-in records for the provided clock-in record ID.
11. /clock-in/{clock_in_record_id} :- this DELETE method is used to delete the clock-in record details from the DB having ID as provided by the user.
12. /clock-in/{clock_in_record_id} :- this PUT method is used to update the clock-in record details in the DB.

## Manual Steps for Local Setup

1. Download Python in your system. (version used 3.11.8)
2. Create a folder for your project.
3. Create a virtual environment in your folder. (an optional step, run the command in your folder directory in the command prompt to create virtual env e.g.,: python -m venv venv)
4. Activate the virtual environment. (command: venv/Scripts/activate.bat)
5. Clone or download this repo into your project directory. NOTE:- under your root project directory there should be two folder: one is the virtual env (venv) and the other one containing all the files this repo contains.
6. Install all the libraries by running the command in your cmd: pip install -r requirements.txt
7. Install MongoDB in your machine: https://www.mongodb.com/try/download/community (directly download and run the msi file).
8. Open your Mongo Compass and create connection. Then create a Database "MyDB" (you can provide your preferable name). The guide for this MongoDB setup is present in below Reference section.
9. Now start the server: uvicorn main:app
10. Use the URL: http://127.0.0.1:8000/docs to access your API.
11. Tada! you are done with your local setup. Do your experiments with the APIs.

## References & Links
* Download Python: https://www.python.org/downloads/
* MongoDB setup: https://www.geeksforgeeks.org/how-to-install-mongodb-on-windows/
* Refer the documentation to deploy your App and make MongoDB cloud connections for free: https://testdriven.io/blog/fastapi-mongo/#deployment
* Deploy FastAPI in Render for free: https://docs.render.com/deploy-fastapi
* You can setup your default python version: https://docs.render.com/python-version#:~:text=Specify%20a%20different%20Python%20version,0%20onward.

## Snaps of project and User Guide
![image](https://github.com/user-attachments/assets/da506d41-93ba-45c9-ba12-9b8fecc31898)

creating a sample item
![image](https://github.com/user-attachments/assets/e5274f41-f3af-44e2-9f88-59667bf92dcf)

corresponding response of the API
![image](https://github.com/user-attachments/assets/602c1166-2db5-47d9-86cd-e0a6b8b4e629)

the GET API response, provided the ID of the created item.
![image](https://github.com/user-attachments/assets/2afc5a1d-fccd-4465-b2cf-1ae5c357429c)

DB records
![image](https://github.com/user-attachments/assets/ea391a1a-aa1d-41df-8950-38f9892b084d)

Folder structure reference and commands
![image](https://github.com/user-attachments/assets/c12c4ac3-21d3-408d-9edc-af1feb8cecec)

## Thanks
For queries mail to: tanmayanayak1305@gmail.com.
Happy Learning!
