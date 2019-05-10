## Metastorm
Metastorm has been released using a microservice architecture. Details about the microservices can be found in the docker-compose.yml file. 

### How to start

    docker-compose build
    docker-compose up -d

This will expose the ports from the different microservices:

* **15001: for the backend (Flask API)**: This is the endpoint to the main API. It was developed using Flask, see ./app/ for details
* **17001: for the plupload microservice**: This microservice uploads raw reads to MetaStorm server and then moves it to the high computing cluster efficiently.
* **16001: Administration interface for MetaStorm**: This endpoint contains the admin interface for the database of MetaStorm. 


## Requirements to run MetaStorm
backend and plupload need access to the high performance computing cluster. Therefore, you need to provide a valid .ssh key, that will automatically access the cluster without the need to login with password. 

The key has to be placed under ./ssh/ before doing the docker-compose or docker-up commands
Then allow only reading permissions to www-data from plupload
    
    chmod -R 444 *

## Frontend requirements
If you are running a local copy of MetaStorm. You need to modify two lines in the login.js and prod.js files. These are the links to the endpoints, if you are in local use / if you are in a cluster, use the proxy link you setup. For instance /MetaStorm/

## Cluster computing requirements
Most of the tools used by MetaStorm are under the ./bin/ directory. However, there will be multiple python modules that will need to be installed in the cluster. Test few examples and check the logs to see what modules are missing. 