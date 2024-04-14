# Food Order Management API
## About the Service
This is a FastAPI Python microservice written in Python 3.10. The API is a (very simple!) food order management API for a restaurant.

It exposes 3 main endpoints

/customers - endpoint for customers to make/add to orders

/restaurant - endpoint for restaurant to accept/reject and view placed orders

/internal/refunds - endpoint to view all refunds to be processed

The service makes use of the Python [apscheduler package](https://apscheduler.readthedocs.io/en/3.x/index.html) which allows it to automatically reject orders that have
been waiting for 5 minutes or longer to be processed.

## CICD via GitHub Actions
CICD has been created for this project using GitHub actions. The actions workflow file can be viewed inside the `.github\workflows` folder.

The build job will install all dependencies using pip, lint the code and then run the tests using PyTest. 

### Snyk Code Scanning

Inside of `src/ordermgmt/demo/insecure_demo.py` there are some insecure code examples to demonstrate Snyk code scanning via GitHub Actions. These are not used anywhere in the application and have been introduced specifically for this demo.

The `snyk` job will setup Snyk CLI. Then, using Snyk CLI the action will run `snyk code test` to run a SAST security scan on the source code.
 
Next, it builds the docker image for the service, runs container and SCA analysis on the image.

Finally, it will upload the `snyk.sarif` file to GitHub Code Scanning. This step is very powerful as it enables code insights on the vulnerable code. 
This empowers developers to remediate the vulnerabilities themselves, providing rich help documentation and adding annotations
around the exact line of code the vulnerability was detected on, helping to shift security left into CICD processes and resolve these issues before releasing to production.

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
