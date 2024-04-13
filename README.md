# Food Order Management API
## About the Service
This is a FastAPI Python microservice written in Python 3.10.

Inside the directory /src/ordermgmt/demo there are some insecure code examples to demonstrate Snyk code scanning via GitHub Actions. These are not used anywhere in the application and have been introduced specifically for this demo.


Snyk scanning has also been enabled for the libraries installed via pip, as well as the docker image for the API.


The API is a (very simple!) food order management API for a restaurant.

It exposes 3 main endpoints

/customers - endpoint for customers to make/add to orders


/restaurant - endpoint for restaurant to accept/reject and view placed orders


/internal/refunds - endpoint to view all refunds to be processed


The service makes use of the Python [apscheduler package](https://apscheduler.readthedocs.io/en/3.x/index.html) which allows it to automatically reject orders that have
been waiting for 5 minutes or longer to be processed.

## Running the Service Locally
### Windows
```commandline
    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    cd .\src
    py ordermgmt\app.py
```
#### To run unit tests
```commandline
    # first cd to the project's root dir, then run the following commands
    pip install -r test-requirements.txt
    cd .\src\
    pytest .\ordermgmt\tests
```

### Linux
```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    cd src/
    python ordermgmt/app.py
```

#### To run unit tests
```commandline
    # first cd to the project's root dir, then run the following commands
    pip install -r test-requirements.txt
    cd src/
    pytest ordermgmt/tests
```

### To build docker image
```commandline
    docker build . -t ordermgmt-api:3.11.8
```

Browse to http://localhost:8000/ to view the Swagger API docs for the service
