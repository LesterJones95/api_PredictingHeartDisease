import psycopg2

csv_input_file = './csv_input_file.csv'
csv_output_file = './init_data.csv'

with open(csv_input_file, 'r', encoding='utf-8') as file:
    data = file.readlines()

data[0] = data[0].replace(" ", "_").lower()

with open(csv_output_file, 'w', encoding='utf-8') as file:
    file.writelines(data)

print(f"Output file: {csv_output_file} created...")


conn = psycopg2.connect(database="heartdisease_db",
                        user='postgres', password='postgres', 
                        host='127.0.0.1', port='5858'
)

conn.autocommit = True
cursor = conn.cursor()

columns = ['id', 'age','sex','chest_pain_type','bp','cholesterol','fbs_over_120','ekg_results','max_hr','exercise_angina','st_depression','slope_of_st','number_of_vessels_fluro','thallium' ]

with open(csv_output_file, 'r') as f:
    # Notice that we don't need the csv module.
    next(f) # Skip the header row.
    cursor.copy_from(f, 'patient_details', columns=columns, sep=',')

conn.commit()

sql3 = '''select * from patient_details;'''
cursor.execute(sql3)
for i in cursor.fetchall():
    print(i)

conn.commit()
conn.close()