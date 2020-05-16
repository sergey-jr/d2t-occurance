select mr.id, measurement_id, mrpl.patient_id, p.gender_id, p.birthday_year, p.birthday_month, p.birthday_day,
 mr.val1, mr.measure_time
from measurement_result mr 
inner join measurement_result_patient_link mrpl on mr.id = measurement_result_id 
inner join patient p on mrpl.patient_id = p.id
inner join measurement on mr.measurement_id = measurement.id
inner join strings on measurement.name_string_id = strings.string_id
where 
(measurement_id in (27, 128, 1581, 8542, 8561, 1581, 1582, 87, 203, 28, 29, 30, 35)) and 
(mr.val1 is not null and mr.val1 != 0)
and language_id = 1

