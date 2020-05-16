import pandas as pd
import psycopg2
import json
import re

creds = json.load(open('credentials.json'))
conn = psycopg2.connect(**creds)
cursor = conn.cursor()

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


