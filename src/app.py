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

UPLOAD_FOLDER = './uploads'

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'} #, 'json'}
TRAINED_MODEL = ydf.load_model('./final_model.keras')

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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


@app.route('/show_db')
def showDatabase():
    conn = psycopg2.connect(database="heartdisease_db",
                        user='postgres', password='postgres', 
                        host='127.0.0.1', port='5858'
)
    conn.autocommit = True
    cursor = conn.cursor()

    #sql3 = '''select id,prediction from patient_details;'''
    #cursor.execute(sql3)
    #rowResults=cursor.fetchall()
    
    cursor.execute("SELECT * FROM patient_details")

    rows = cursor.fetchall()

    columns = ['id', 'age','sex','chest_pain_type','bp','cholesterol','fbs_over_120','ekg_results','max_hr','exercise_angina','st_depression','slope_of_st','number_of_vessels_fluro','thallium', 'prediction']    
    df = pd.DataFrame(rows, columns=columns)
    #print(df)
    df = df.drop('prediction', axis=1)
    
    replace_columns = ["id", "Age", "Sex", "Chest pain type", "BP", "Cholesterol", "FBS over 120", "EKG results", "Max HR", "Exercise angina", "ST depression", "Slope of ST", "Number of vessels fluro", "Thallium"]
    df = df.set_axis([replace_columns], axis=1)
    print("------------------------------------------------------------")
    print(df.columns)
    print(type(df.columns[0]))
    df.columns = df.columns.get_level_values(0)

    print("Starting to predict ....\n")
    predictions = TRAINED_MODEL.predict(df.loc[ : , df.columns != 'id'])
    print("Finsihed....\n")
    df['Prediction'] = predictions
    #If json convert to csv
    #predictions = TRAINED_MODEL.predict(uploaded_df)
    #uploaded_df['Prediction'] = predictions
    # Converting to html Table
    #uploaded_results_html = rowResults.to_html()
    uploaded_df_html = df[['id', 'Prediction']].to_html()

    df.columns.get_level_values(0)
    cursor.close()
    conn.close()
    return render_template('show_db_data.html',
                           data_var=uploaded_df_html)


if __name__ == '__main__':
    app.run(debug=True)