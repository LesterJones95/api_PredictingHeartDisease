## Run src
```bash
    flask --app ./src/app.py run --debug #--host=0.0.0.0
```

## Run and intialize db
```bash
    docker-compose -f docker-compose.yaml up
    
    #only necessary once we have a volumn
    python ./init_fill_db.py
```

## Create and activate venv (windows)
```bash
    py -3 -m venv .api_flask
    source ./.api_flask/Scripts/activate
``` 

## Install dependencies
```bash 
    pip install Flask
    pip install pandas
```


#### Inspiration
- https://flask.palletsprojects.com/en/stable/quickstart/ 
- https://www.geeksforgeeks.org/python/uploading-and-reading-a-csv-file-in-flask/ 

- https://www.geeksforgeeks.org/python/python-import-csv-into-postgresql/
- https://medium.com/@vinod.chelladuraiv/postgresql-pgadmin-and-python-inside-docker-e1b9bbc5b617 
- https://dev.to/effylh/display-recent-queries-on-web-page-from-postgresql-database-with-flaskpsycopg2bootstrap-3of4