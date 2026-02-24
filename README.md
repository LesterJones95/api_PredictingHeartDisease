# Result
A simple WebApp that:
- Shows a prepopulated set of patient IDs and their respective prediction for the presence of heart disease.
- Expects a dataset a .csv file. (With the same columns and their datatypes as the Kaggle dataset) 
- Predicts the presence of a heart disease for the observations in this .csv file using a pretrained GradientBoostedTrees ML model (see: [GitHub repo](https://github.com/LesterJones95/Predicting-Heart-Disease)).
- Check the prediction for a specific Patient ID

![api_heartdisease gif](./api_heartdisease.gif)

### Prerequisites
- Docker
- Python

### Technologies
- Flask
- Postgres
- HTML
- Machine Learning

## Introduction
This repo contains an out of the box setup to create the simple WebApp shown above. This setup is not meant to win a beauty contest or mimic a professional production environment. <br/> Rather, it gives the reader some idea of what is possible once you have trained a Machine Learning model. In [this](https://github.com/LesterJones95/Predicting-Heart-Disease) repo I have previously trained and saved a Machine Learning model using TensorFlow. This ML model is copied in this repo as folder ```./final_model.keras```. 
<br/>
A simple diagram of the setup is displayed below:
<br/><br/>
![api_setup svg](./api_setup.svg)

It is recommended to clone this repo, and follow the commands below. These actions will:
- Start the Postgres database
- Populate the database
- Start the Flask WebApp

After this is done you can visit the url: ```http://localhost:5000``` and see how uploading new .csv files will generate predictions for the presence of a heart disease for new observations.

# Set up
On your local machine

```bash
    cd /path/to/repo
    git clone https://github.com/LesterJones95/api_PredictingHeartDisease.git
    cd api_PredictingHeartDisease
```
## Create and activate venv (windows)
```bash
    py -3 -m venv .api_flask
    source ./.api_flask/Scripts/activate
    pip install -r requirements.txt
``` 

## Run and intialize db
```bash
    cd db
    docker-compose -f docker-compose.yaml up #-d for detached
    
    #only necessary once
    python ./init_fill_db.py
```

## Run webapp 
```bash
    # From root
    flask --app ./src/app.py run #--debug --host=0.0.0.0
```

## Containerize Flask App [optional]
```bash
    # From root
    pip freeze > requirements-freeze.txt

    # In Docker: Settings>Resources>Network> enable host networking = checked
    docker build -t heart-disease-gui .
    docker run -p 5000:5000 --network=host heart-disease-gui

    #v2
    docker build -t heart-disease-gui:v2 .
    docker run -p 5000:5000 --env-file .env --network=host heart-disease-gui:v2    
```

## Containerize Database [optional]
```bash
    # From root
    pip freeze > requirements-freeze.txt

    # In Docker: Settings>Resources>Network> enable host networking = checked
    docker build -t heart-disease-db -f Dockerfile_db .
    docker run heart-disease-db
```



#### Inspiration
- https://flask.palletsprojects.com/en/stable/quickstart/ 
- https://www.geeksforgeeks.org/python/uploading-and-reading-a-csv-file-in-flask/ 

- https://www.geeksforgeeks.org/python/python-import-csv-into-postgresql/
- https://medium.com/@vinod.chelladuraiv/postgresql-pgadmin-and-python-inside-docker-e1b9bbc5b617 