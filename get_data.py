import pandas as pd
import psycopg2
import json
from datetime import datetime
import csv
import numpy as np
import re


def format_date(date_arr):
    d, m, y = date_arr
    if y is None or all([item is None for item in date_arr]):
        return None
    d = "1" if d is None else str(d)
    m = "1" if m is None else str(m)
    y = str(y)
    if len(m) == 1:
        m = "0" + m
    if len(d) == 1:
        d = "0" + d
    if len(y) == 3:
        y = "1" + y
    elif len(y) < 3:
        return None
    date_arr = [d, m, y]
    return datetime.strptime(".".join(date_arr), "%d.%m.%Y")


creds = json.load(open("credentials.json"))
conn = psycopg2.connect(**creds)
cursor = conn.cursor()
# query = open("SQL/weight, height, glucose, presure with patient.sql",
#              mode='r',
#              encoding='utf-8').read().replace("\n", " ")
query = """select mr.id, measurement_id, mrpl.patient_id, p.gender_id, p.birthday_year, p.birthday_month, p.birthday_day,
 mr.val1, mr.measure_time
from measurement_result mr 
inner join measurement_result_patient_link_old mrpl on mr.id = measurement_result_id 
inner join patient p on mrpl.patient_id = p.id
inner join measurement on mr.measurement_id = measurement.id
where 
(measurement_id in (27, 28, 29, 30, 128, 1581, 8542, 8561, 1582, 87)) and 
(mr.val1 is not null and mr.val1 != 0)
order by mrpl.patient_id, measure_time desc
"""

SQL = """
select patient_id, value_string, string_value
from anamnesis_item  
join anamnesis_item_type on anamnesis_type_id = anamnesis_item_type.id
join anamnesis on anamnesis_id = anamnesis.id
join strings on anamnesis_item_type.name_string_id = string_id
where upper(value_string) like upper('%диабет 2%') and language_id=1
order by patient_id desc, string_value desc
"""

cursor.execute(SQL)
records = cursor.fetchall()
patients = set()
for item in records:
    pid, value_string, string_value = item
    if len(re.findall(".*диабет 2.*", value_string)):
        patients.add(pid)

cursor.execute(query)
# pid, glucose blood, glucose urine, systolic bp, diastolic bp, weight, height, gender, age,  time_stamp
mid_keys = {8542: "w", 8561: "h", 1581: "sbp", 1582: "dbp", 27: "glb", 128: "glu", 87: "glg",
            28: "blb_g", 29: "blb_d", 30: "blb_id"}
start = datetime.now()
with open("data1.csv", mode="w", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=";")
    csv_writer.writerow(["res_id", "patient_id", "gender", "birthday", "age", "glucose_blood",
                         "glucose_urine", "HbA1C", "bilirubin_common", "bilirubin_direct", "bilirubin_indirect",
                         "systolic_bp", "diastolic_bp", "weight", "height", "real_target", "time_stamp"])
    while True:
        row = cursor.fetchone()
        if row is not None:
            res_id, mid, pid, gender, bd_y, bd_m, bd_d, val1, ts = row
            birthday = format_date([bd_d, bd_m, bd_y])
            age = None

            if birthday:
                age = (ts - birthday).total_seconds() / (365 * 24 * 60 * 60)

            # tmp = [res_id, m_type, pid, gender, birthday, age, val1, ts]
            tmp = {"res_id": res_id, "pid": pid, "gender": gender, "birthday": birthday, "age": age, "glb": np.nan,
                   "glu": np.nan, "glg": np.nan, "blb_g": np.nan, "blb_d": np.nan, "blb_id": np.nan, "sbp": np.nan,
                   "dbp": np.nan, "w": np.nan, "h": np.nan, "target": int(pid in patients), "ts": ts}

            tmp[mid_keys[mid]] = val1

            csv_writer.writerow(list(tmp.values()))
        else:
            break
timeout = (datetime.now() - start).total_seconds()
print("end fetching in {} minutes ({} seconds)".format(timeout / 60, timeout))
