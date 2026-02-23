FROM python:3.11-slim

WORKDIR /app  
COPY ./src /app/src
COPY ./final_model.keras /app/final_model.keras
COPY ./requirements-freeze.txt /app/requirements.txt

# install tools required by 'pip install'
RUN python -m pip install --upgrade pip
#RUN pip install --upgrade wheel
#RUN pip install --upgrade setuptools

# necassary for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

RUN pip install -r requirements.txt

EXPOSE 5000 

CMD ["flask", "--app", "./src/app.py", "run", "--host=0.0.0.0"]