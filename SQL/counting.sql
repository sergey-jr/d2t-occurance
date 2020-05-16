select measurement_id, string_value, count(*) as measures, count(distinct(patient_id)) as patients_distinct
from measurement_result mr 
inner join measurement_result_patient_link_old mrpl on mr.id = measurement_result_id 
inner join patient p on mrpl.patient_id = p.id
inner join measurement on mr.measurement_id = measurement.id
inner join strings on measurement.name_string_id = strings.string_id
where 
(measurement_id in (27, 128, 1581, 8542, 8561, 1581, 1582, 87, 203, 28, 29, 30, 35)) and 
(mr.val1 is not null and mr.val1 != 0)
and language_id = 1
group by measurement_id, string_value
order by measures Desc
