from distutils.log import debug
from fileinput import filename
from flask import Flask, request, redirect, render_template, flash, url_for, session
from markupsafe import escape
import pandas as pd
import os
from werkzeug.utils import secure_filename
import ydf
import psycopg2 
from sqlalchemy import create_engine, text


print(f"Working with:\nPOSTGRES DB: {os.environ.get('POSTGRES_DB')}")
print(f"POSTGRES HOST:PORT: {os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}")
UPLOAD_FOLDER = './uploads'

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'} #, 'json'}
TRAINED_MODEL = ydf.load_model('./final_model.keras')

input_db_columns = ['id', 'age','sex','chest_pain_type','bp','cholesterol','fbs_over_120','ekg_results','max_hr','exercise_angina','st_depression','slope_of_st','number_of_vessels_fluro','thallium']    
db_columns = ['id', 'age','sex','chest_pain_type','bp','cholesterol','fbs_over_120','ekg_results','max_hr','exercise_angina','st_depression','slope_of_st','number_of_vessels_fluro','thallium', 'prediction']    
df_columns = ["id", "Age", "Sex", "Chest pain type", "BP", "Cholesterol", "FBS over 120", "EKG results", "Max HR", "Exercise angina", "ST depression", "Slope of ST", "Number of vessels fluro", "Thallium"]

def set_db():
    conn = psycopg2.connect(database=os.getenv('POSTGRES_DB'),
                        user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'), 
                        host=os.getenv('POSTGRES_HOST'), port=os.getenv('POSTGRES_PORT'))
    conn.autocommit = True
    cursor = conn.cursor()

    return conn, cursor

def close_db(conn, cursor):
    cursor.close()
    conn.close()

app = Flask(__name__)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'This is your secret key to utilize session in Flask'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            conn, cursor = set_db()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            
            csv_output_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(csv_output_file, 'r') as f:
            # Notice that we don't need the csv module.
                next(f) # Skip the header row.
                cursor.copy_from(f, 'patient_details', columns=input_db_columns, sep=',')
            close_db(conn, cursor)
            return render_template('index2.html')  
              
    return render_template("index.html")


@app.route('/show_prediction')
def showPrediction():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    
    #If json convert to csv
    predictions = TRAINED_MODEL.predict(uploaded_df)
    uploaded_df['Prediction'] = predictions
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()

    return render_template('show_csv_data.html',
                           data_var=uploaded_df_html)


@app.route('/show_db', methods=['GET', 'POST'])
@app.route('/show_db/<patient_id>', methods=['GET'])
def showDatabase(patient_id=None):
    conn, cursor = set_db()
    
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        print(f"Request method POST:\Patient ID:{patient_id}")

    if not patient_id:
        cursor.execute("SELECT * FROM patient_details")
    else:
        cursor.execute("SELECT * FROM patient_details WHERE id = (%s)", (patient_id,))

    rows = cursor.fetchall()
    #print(f"Rows:\n{rows}")
    
    df = pd.DataFrame(rows, columns=db_columns)
    #print(df)
    df = df.drop('prediction', axis=1)
    
    
    df = df.set_axis([df_columns], axis=1)
    print("------------------------------------------------------------")
    df.columns = df.columns.get_level_values(0)

    print("Starting to predict ....\n")
    predictions = TRAINED_MODEL.predict(df.loc[ : , df.columns != 'id'])
    print("Finsihed....\n")
    df['Prediction'] = predictions
    
    uploaded_df_html = df[['id', 'Prediction']].drop_duplicates().to_html(index=False)

    
    close_db(conn, cursor)
    return render_template('show_db_data.html',
                           data_var=uploaded_df_html)


if __name__ == '__main__':
    app.run(debug=True)