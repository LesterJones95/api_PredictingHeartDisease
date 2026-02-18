create schema heartdisease_db;

create table patient_details (
    id integer not null,
    age integer not null,
    sex boolean not null,
    chest_pain_type integer not null,
    bp integer not null,
    cholesterol integer not null ,
    fbs_over_120 boolean not null,
    ekg_results integer not null,
    max_hr integer not null,
    exercise_angina boolean not null,
    st_depression float not null,
    slope_of_st integer not null,
    number_of_vessels_fluro integer not null,
    thallium integer not null,
    prediction float 
);