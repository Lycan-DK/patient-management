### Description
Project displays how to use sererless for deployment for microservices based project.
The project uses AWS services like Lambda, App Sync and Dynamo DB for creating GraphQL APIs at the backend.

The project also shows how to setup env for local and testing on local for developed functionalities.

### Techonologies used
- GraphQL
- AWS

### Used following AWS services :
 - AWS App Sync
 - AWS Lambda
 - AWS DynamoDB
 
##### Deployment :
 - Serverless.yml

### 1. How to Deploy
- You have to configure IAM user from our AWS account to use aws service and deployment
    - create new user with programattic access 
    - attached existing policy to the user & set administrator access

- Configure serverless in root directory of folder
    ```bash
    cd backend
    serverless config credentials --provider aws --key xxx --secret yyy --profile zzz
    ```
  
- Now you have to update serverless.yml file for below configurations
    - region: '********' # add region
    - profile: '************' # add user profile name here
    
- Next, we'll run the deploy command to create the services in our account:
    ```bash
    serverless deploy
    ```
### 2. Local setup for testing

- install serverless
    ```bash
    npm i serverless -g
    ```
- create virtual env in root directory
    On macOS and Linux:
    ```bash
    python3 -m venv env
    ```
    
    On Windows:
    ```bash
    py -m venv env
    ```
- activate virtual env in terminal

    On macOS and Linux:
    ```bash
    source env/bin/activate
    ```
    
    On Windows:
    ```bash
    .\env\Scripts\activate
    ```
  
- Install requirements using 
    ```bash
    pip install local_requirements.txt
    ```
  
- Go to compose folder and run docker-compose in daemon mode
    ```bash
    docker-compose up -d
    ```

- Go to root directory and run unittest cases using cmd
    ```bash
    python -m unittest
    ```