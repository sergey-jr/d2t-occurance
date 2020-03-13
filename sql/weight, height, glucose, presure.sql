select * from measurement_result 
where 
(measurement_id in (8561, 59, 8542, 6641)) and (val1 is not null or val2 is not null)