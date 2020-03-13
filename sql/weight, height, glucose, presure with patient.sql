select mr.id, mrpl.patient_id, birthday_year, birthday_month, birthday_day, mr.measurement_id, mr.val1, mr.measure_time
from measurement_result mr 
inner join measurement_result_patient_link mrpl on mr.id = measurement_result_id 
inner join patient on mrpl.patient_id = patient.id
where 
(measurement_id in (27, 128, 1581, 8542, 8561)) and (mr.val1 is not null and mr.val1 != 0)
order by mrpl.patient_id, mr.measurement_id
