select * from measurement_result 
where 
(measurement_id in [8561, 6664, 8542]) and (val1 is not null or val2 is not null) limit 100
