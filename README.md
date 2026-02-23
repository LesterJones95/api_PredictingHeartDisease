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
```





#### Inspiration
- https://flask.palletsprojects.com/en/stable/quickstart/ 
- https://www.geeksforgeeks.org/python/uploading-and-reading-a-csv-file-in-flask/ 

- https://www.geeksforgeeks.org/python/python-import-csv-into-postgresql/
- https://medium.com/@vinod.chelladuraiv/postgresql-pgadmin-and-python-inside-docker-e1b9bbc5b617 

# Appendix A <br/>
```bash
    2.743 Collecting psycopg2==2.9.11 (from -r requirements.txt (line 13))
    2.758   Downloading psycopg2-2.9.11.tar.gz (379 kB)
    2.882   Installing build dependencies: started
    3.601   Installing build dependencies: finished with status 'done'
    3.602   Getting requirements to build wheel: started
    3.966   Getting requirements to build wheel: finished with status 'error'
    3.973   error: subprocess-exited-with-error
    3.973
    3.973   × Getting requirements to build wheel did not run successfully.
    3.973   │ exit code: 1
    3.973   ╰─> [34 lines of output]
    3.973       /tmp/pip-build-env-7ots07te/overlay/lib/python3.11/site-packages/setuptools/dist.py:765: SetuptoolsDeprecationWarning: License classifiers are deprecated.  
    3.973       !!
    3.973
    3.973               ********************************************************************************
    3.973               Please consider removing the following classifiers in favor of a SPDX license expression:
    3.973
    3.973               License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
    3.973
    3.973               See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
    3.973               ********************************************************************************
    3.973
    3.973       !!
    3.973         self._finalize_license_expression()
    3.973       running egg_info
    3.973       writing psycopg2.egg-info/PKG-INFO
    3.973       writing dependency_links to psycopg2.egg-info/dependency_links.txt
    3.973       writing top-level names to psycopg2.egg-info/top_level.txt
    3.973
    3.973       Error: pg_config executable not found.
    3.973
    3.973       pg_config is required to build psycopg2 from source.  Please add the directory
    3.973       containing pg_config to the $PATH or specify the full executable path with the
    3.973       option:
    3.973
    3.973           python setup.py build_ext --pg-config /path/to/pg_config build ...
    3.973
    3.973       or with the pg_config option in 'setup.cfg'.
    3.973
    3.973       If you prefer to avoid building psycopg2 from source, please install the PyPI
    3.973       'psycopg2-binary' package instead.
    3.973
    3.973       For further information please check the 'doc/src/install.rst' file (also at
    3.973       <https://www.psycopg.org/docs/install.html>).
    3.973
    3.973       [end of output]
    3.973
    3.973   note: This error originates from a subprocess, and is likely not a problem with pip.
    3.977 ERROR: Failed to build 'psycopg2' when getting requirements to build wheel
```
